# -*- coding: UTF-8 -*-

from __future__ import print_function

import sys
import json
from datetime import datetime
from collections import namedtuple, defaultdict

# Python 2/3 hack.
try:
    from ConfigParser import SafeConfigParser as ConfigParser
except:
    from configparser import ConfigParser

from elasticsearch import Elasticsearch, NotFoundError, TransportError, RequestError

# Some of these imports are part of the public API...
from partycrasher.crash import Crash, Stacktrace, Stackframe
from partycrasher.es_crash import ESCrash
from partycrasher.es_crash import ReportNotFoundError
from partycrasher.bucketer import MLTCamelCase
from partycrasher.threshold import Threshold


__version__ = u'0.1.0'

DEFAULT_THRESHOLDS = ('1.0', '2.0', '3.0',
                      '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0')


class BucketNotFoundError(KeyError):
    """
    When a particular bucket cannot be found.
    """


class Bucket(namedtuple('Bucket', 'id project threshold total top_reports first_seen')):
    """
    Data class for buckets. Contains two identifiers:
     - id: The bucket's ID;
     - total: how many reports are currently in the bucket.
    """

    def to_dict(self, *args, **kwargs):
        """
        Converts the current object into a dictionary;
        Any arguments are treated as in the `dict` constructor.
        """
        kwargs.update(self._asdict())
        for arg in args:
            kwargs.update(arg)

        # HACK: remove empty top_reports, first_seen.
        if kwargs['top_reports'] is None:
            del kwargs['top_reports']

        if kwargs['first_seen'] is None:
            del kwargs['first_seen']

        return kwargs


class Project(namedtuple('Project', 'name')):
    """
    Metadata about a project.
    """



class PartyCrasher(object):
    def __init__(self, config_file=None, thresholds=DEFAULT_THRESHOLDS):
        self.config = ConfigParser(default_config())
        self.thresholds = thresholds
        self._checked_index_exists = False

        # TODO: Abstract config out.
        if config_file is not None:
            self.config.readfp(config_file)

        # self.es and self.bucketer are lazy properties.
        self._es = None
        self._bucketer = None
        self._checked_index_exists = False

    @property
    def es_servers(self):
        """
        Configured ES server list
        """
        return self.config.get('partycrasher.elastic', 'hosts').split()

    @property
    def allow_delete_all(self):
        """
        Whether or not the instance should allow all data to be deleted at once
        """
        return self.config.getboolean('partycrasher.elastic', 'allow_delete_all')

    @property
    def es(self):
        """
        ElasticSearch instance.

        """
        if not self._es:
            self._connect_to_elasticsearch()
        return self._es

    @property
    def bucketer(self):
        """
        Bucketer instance.
        """
        if not self._bucketer:
            self._connect_to_elasticsearch()
        return self._bucketer

    @property
    def default_threshold(self):
        """
        Default threshould to use if none are provided.
        """
        # TODO: determine from static/dynamic configuration
        return Threshold(4.0)

    def delete_and_recreate_index(self):
        """
        Deletes the entire index and recreates it. This destroys all of the
        reports.
        """
        assert self.allow_delete_all
        self.es.indices.delete(index='crashes')
        self.es.cluster.health(wait_for_status='yellow')
        self._bucketer.create_index()
        self.es.cluster.health(wait_for_status='yellow')


    def _connect_to_elasticsearch(self):
        """
        Establishes a connection to ElasticSearch. given configuration.
        """
        self._es = Elasticsearch(self.es_servers)

        # XXX: Monkey-patch our instance to the global.
        ESCrash.es = self._es

        self._bucketer = MLTCamelCase(name="buckets",
                                      thresholds=self.thresholds,
                                      lowercase=False, only_stack=False,
                                      index='crashes', elasticsearch=self.es)
        if not self._checked_index_exists:
            if self._es.indices.exists('crashes'):
                self._checked_index_exists = True
            else:
                self._bucketer.create_index()
        self.es.cluster.health(wait_for_status='yellow')
        return self._es

    def ingest(self, crash, dryrun=False):
        """
        Ingest a crash; the Crash may be a simple dictionary, or a
        pre-existing Crash instance.

        :return: the saved crash
        :rtype Crash:
        :raises IdenticalReportError:
        """
        true_crash = Crash(crash)
        if 'stacktrace' in true_crash:
	  assert isinstance(true_crash['stacktrace'], Stacktrace)
	  assert isinstance(true_crash['stacktrace'][0], Stackframe)
	  if 'address' in true_crash['stacktrace'][0]:
	    assert isinstance(true_crash['stacktrace'][0]['address'], basestring)
	  

        if dryrun:
            true_crash['buckets'] = self.bucketer.assign_buckets(true_crash)
            return true_crash
        else:
            return self.bucketer.assign_save_buckets(true_crash)

    def get_bucket(self, threshold, bucket_id, 
                   project=None, from_=None, size=None):
        """
        Returns information for the given bucket.
        """
        # Coerce to a Threshold object.
        threshold = Threshold(threshold)

        query = {
            "filter": {
                "term": {
                    "buckets." + threshold.to_elasticsearch(): bucket_id
                }
            },
            "sort": { "date": { "order": "desc" }}
        }
                
        if from_ is not None:
            query["from"] = from_;
            query["size"] = size;

        response = self.es.search(body=query, index='crashes')
        reports_found = response['hits']['total']

        # Since no reports were found, assume the bucket does not exist (at
        # least for this project).
        if reports_found < 1:
            raise BucketNotFoundError(bucket_id)

        reports = get_reports_by_bucket(response, threshold).get(bucket_id)
        assert reports

        return Bucket(id=bucket_id,
                      project=project,
                      threshold=threshold,
                      total=reports_found,
                      top_reports=reports,
                      first_seen=None)

    def top_buckets(self, lower_bound, threshold=None, project=None, 
                    from_=None, size=None):
        """
        Given a datetime lower_bound (from date), calculates the top buckets
        in the given timeframe for the given threshold (automatically
        determined if not given). The results can be tailed for a specific
        project if needed.

        Returns a list of {'doc_count': int, 'key': id} dictionaries.
        """

        if not isinstance(lower_bound, datetime):
            raise TypeError('The lower bound MUST be a datetime object.')

        # Get the default threshold.
        if threshold is None:
            threshold = self.default_threshold
        if not isinstance(threshold, Threshold):
            threshold = Threshold(threshold)

        # Filters by lower-bound by default;
        filters = [{
            "range": {
                "date": {
                    "gt": lower_bound.isoformat()
                }
            }
        }]

        # May filter optionally by project name.
        if project is not None:
            filters.append({
                "term": {
                    "project": project
                }
            })

        # Oh, ElasticSearch! You and your verbose query "syntax"!
        query = {
            # Read this inside out:
            "aggs": {
                "top_buckets_filtered": {
                    # Filter the top buckets by date, and maybe by project.
                    "filter": {
                        "bool": { "must": filters }
                    },
                    # Get the top buckets in descending order of size.
                    "aggs": {
                        "top_buckets": {
                            "terms": {
                                "field": "buckets." + threshold.to_elasticsearch(),
                                "order": { "_count": "desc" },
                            },
                            # Get the date of the latest crash per bucket.
                            "aggs": {
                                "first_seen": {
                                    "min": {
                                        "field": "date"
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # Do not send any hits back!
            "size": 0
        }
                                    
        if size is None:
          size = 10
        
        actual_size = size
        
        if from_ is not None:
            assert from_ >= 0
            actual_size = actual_size + from_
        if size is not None:
            assert size >= 0
            (query["aggs"]["top_buckets_filtered"]["aggs"]
                  ["top_buckets"]["terms"]["size"]) = actual_size
        
        try:
            response = self.es.search(body=query, index='crashes')
        except RequestError as e:
            print(e.error, file=sys.stderr)
            raise e

        # Oh, ElasticSearch! You and your verbose responses!
        top_buckets = (response['aggregations']
                       ['top_buckets_filtered']
                       ['top_buckets']
                       ['buckets'])
        
        if from_ is not None:
            top_buckets = top_buckets[from_:]

        return [Bucket(id=bucket['key'], project=project, threshold=threshold,
                       total=bucket['doc_count'],
                       first_seen=bucket['first_seen']['value_as_string'],
                       top_reports=None)
                for bucket in top_buckets]

    def get_crash(self, database_id, project):
        self._connect_to_elasticsearch()

        try:
            return ESCrash(database_id, index='crashes')
        except NotFoundError as e:
            raise KeyError(database_id)

    def get_summary(self, database_id, project):
        self._connect_to_elasticsearch()

        try:
            return self.bucketer.bucket_explain(database_id, index='crashes')
        except NotFoundError as e:
            raise KeyError(database_id)

    def get_projects(self):
        """
        Returns the list of all projects found in Elasticsearch.
        """

        query = {
            "aggs": {
                "projects": {
                    "terms": {
                        "field":"project"
                    }
                }
            }
        }

        try:
            results = self.es.search(body=query, index='crashes')
        except TransportError:
            # Occurs when the index has just been freshly created.
            return None

        raw_projects = results['aggregations']['projects']['buckets']
        return [Project(project['key']) for project in raw_projects]

    def ensure_index_created(self):
        """
        Ensure that the index exists.
        """
        self._connect_to_elasticsearch()
        return self
      
    def search(self, query_string, project=None, from_=None, size=None):
        es_query = {
            "query": {
                "bool": { "must": [
                    { "query_string": {
                          "query": query_string,
                      }},
                ]}
            }};
        if project is not None:
            es_query['query']['bool']['must'].append({
                "term": {
                    "project": project
                }
            });
        if from_ is not None:
            es_query["from"] = from_;
        if size is not None:
            es_query["size"] = size;
        try:
            r = self._es.search(index='crashes', body=es_query)
        except RequestError as e:
            print(e.info, file=sys.stderr)
            raise
        raw_hits = r['hits']['hits']
        print(json.dumps(raw_hits, indent=2), file=sys.stderr)
        
        results = []

        for hit in raw_hits:
            report = hit['_source']
            crash = Crash(report)
            results.append(crash)

        return results
      


def get_reports_by_bucket(response, threshold):
    """
    Returns a dictionary mapping bucket_id => reports, from the ElasticSearch response.
    """
    buckets = defaultdict(list)

    raw_hits = response['hits']['hits']

    for hit in raw_hits:
        report = hit['_source']
        crash = Crash(report)
        bucket_id = crash.get_bucket_id(threshold)
        buckets[bucket_id].append(crash)

    return dict(buckets)


def default_config():
    return {
        'partycrasher.http': {
            'prefix': '/'
        },
        'partycrasher.elastic': {
            'primary': 'localhost:9200'
        },
        'partycrasher': {
            'allow_delete_all': False,
        },
    }
