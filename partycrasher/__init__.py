# -*- coding: UTF-8 -*-

from datetime import datetime
from collections import namedtuple, defaultdict

# Python 2/3 hack.
try:
    from ConfigParser import SafeConfigParser as ConfigParser
except:
    from configparser import ConfigParser

from elasticsearch import Elasticsearch, NotFoundError, TransportError

# Some of these imports are part of the public API...
from partycrasher.crash import Crash
from partycrasher.es_crash import ESCrash
from partycrasher.es_crash import ReportNotFoundError
from partycrasher.bucketer import MLTCamelCase
from partycrasher.threshold import Threshold


__version__ = u'0.1.0'

DEFAULT_THRESHOLDS = ('1.0', '1.5', '2.0', '2.75', '3.0', '3.25', '3.5',
                      '3.75', '4.0', '4.5', '5.0', '5.5', '6.0', '7.0')


class BucketNotFoundError(KeyError):
    """
    When a particular bucket cannot be found.
    """


class Bucket(namedtuple('Bucket', 'id project threshold total top_reports')):
    """
    Data class for buckets. Contains two identifiers:
     - id: The bucket's ID;
     - total: how many reports are currently in the bucket.
    """

    def to_dict(self, *args, **kwargs):
        """
        Converts the current object into a dictionary;
        Any argguments are treated as in the `dict` constructor.
        """
        kwargs.update(self._asdict())
        for arg in args:
            kwargs.update(arg)
        return kwargs


class Project(namedtuple('Project', 'name')):
    """
    Metadata about a project.
    """



class PartyCrasher(object):
    def __init__(self, config_file=None, thresholds=DEFAULT_THRESHOLDS):
        self.config = ConfigParser(default_config())
        self.thresholds = thresholds

        # TODO: Abstract config out.
        if config_file is not None:
            self.config.readfp(config_file)

        self.esServers = self.config.get('partycrasher.elastic', 'hosts').split()

        # Default to localhost if it's not configured.
        if len(self.esServers) < 1:
            self.esServers = ['localhost']

        # self.es and self.bucketer are lazy properties.
        self._es = None
        self._bucketer = None

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

    def _connect_to_elasticsearch(self):
        """
        Establishes a connection to ElasticSearch. given configuration.
        """
        self._es = Elasticsearch(self.esServers)

        # XXX: Monkey-patch our instance to the global.
        ESCrash.es = self._es

        self._bucketer = MLTCamelCase(name="buckets",
                                      thresholds=self.thresholds,
                                      lowercase=False, only_stack=False,
                                      index='crashes', elasticsearch=self.es)
        self._bucketer.create_index()
        return self._es

    # TODO catch duplicate and return DuplicateRecordError
    def ingest(self, crash, dryrun=False):
        """
        Ingest a crash; the Crash may be a simple dictionary, or a
        pre-existing Crash instance.
        """
        true_crash = Crash(crash)

        if dryrun:
            true_crash['buckets'] = self.bucketer.assign_buckets(true_crash)
            return true_crash
        else:
            return self.bucketer.assign_save_buckets(true_crash)

    def get_bucket(self, threshold, bucket_id, project=None):
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
            }
        }

        response = self.es.search(body=query, index='crashes')
        reports_found = response['hits']['total']

        # Since no reports where found, assume the bucket does not exist (at
        # least for this project).
        if reports_found < 1:
            raise BucketNotFoundError(bucket_id)

        reports = self._get_reports_by_bucket(response,
                                              threshold).get(bucket_id)
        assert len(reports) > 0

        return Bucket(id=bucket_id,
                      project=project,
                      threshold=threshold,
                      total = reports_found,
                      top_reports=reports)

    def top_buckets(self, lower_bound, threshold=None, project=None):
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
            "aggs": {
                "top_buckets_filtered": {
                    "filter": {
                        "bool": { "must": filters }
                    },
                    "aggs": {
                        "top_buckets": {
                            "terms": {
                                "field": "buckets." + threshold.to_elasticsearch(),
                                "order": { "_count": "desc" }
                            }
                        }
                    }
                }
            }
        }

        response = self.es.search(body=query, index='crashes')
        # Oh, ElasticSearch! You and your verbose responses!
        top_buckets = (response['aggregations']
                       ['top_buckets_filtered']
                       ['top_buckets']
                       ['buckets'])

        reports_by_project = self._get_reports_by_bucket(response, threshold)

        return [Bucket(id=bucket['key'], project=project, threshold=threshold,
                       total=bucket['doc_count'],
                       top_reports=reports_by_project.get(bucket['key'], ()))
                for bucket in top_buckets]

    def get_crash(self, database_id):
        self._connect_to_elasticsearch()

        try:
            return ESCrash(database_id, index='crashes')
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

    def delete_crash(self, database_id):
        # TODO: we have to call ES directly here, theres nothing in
        # Crash/ESCrash or Bucketer to handle this case maybe
        # ESCrash(database_id).delete()
        raise NotImplementedError("BUT WHY~!~~~~")

    @staticmethod
    def _get_reports_by_bucket(response, threshold):
        """
        Returns a dictionary of projects => reports, from the response.
        """
        buckets = defaultdict(list)

        raw_hits = response['hits']['hits']

        for hit in raw_hits:
            report = hit['_source']
            crash = ESCrash(Crash(report))
            bucket_id = crash.get_bucket_id(threshold)
            buckets[bucket_id].append(crash)

        return buckets


def default_config():
    return {
        'partycrasher.http': {
            'prefix': '/'
        },

        'partycrasher.elastic': {
            'primary': 'localhost:9200'
        },
    }
