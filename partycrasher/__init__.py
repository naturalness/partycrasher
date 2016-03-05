# -*- coding: UTF-8 -*-

import ConfigParser
from datetime import datetime
from collections import namedtuple, defaultdict

from elasticsearch import Elasticsearch, NotFoundError

# Some of these imports are part of the public API...
from partycrasher.crash import Crash
from partycrasher.es_crash import ESCrash
from partycrasher.es_crash import ReportNotFoundError
from partycrasher.bucketer import MLTCamelCase


class BucketNotFoundError(KeyError):
    """
    When a particular bucket cannot be found.
    """

__version__ = u'0.1.0'

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


class PartyCrasher(object):
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser({'elastic': ''})
        self.esServers = self.config.get('DEFAULT', 'elastic').split()
        if len(self.esServers) < 1:
            self.esServers = ['localhost']
        # self.es and self.bucketer are lazy properties.
        self._es = None
        self._bucketer = None

    @property
    def es(self):
        if not self._es:
            self._connect_to_elasticsearch()
        return self._es

    @property
    def bucketer(self):
        if not self._bucketer:
            self._connect_to_elasticsearch()
        return self._bucketer

    @property
    def default_threshold(self):
        # TODO: determine from static/dynamic configuration
        return 4.0

    def _connect_to_elasticsearch(self):
        """
        Actually connects to ElasticSearch.
        """
        self._es = Elasticsearch(self.esServers)
        # TODO: Have more than one bucketer.
        self._bucketer = MLTCamelCase(thresh=4.0,
                                      lowercase=False,
                                      only_stack=False,
                                      index='crashes',
                                      es=self.es,
                                      name="bucket")
        self._bucketer.create_index()
        return self._es

    # TODO catch duplicate and return 303
    # TODO multi-bucket multi-threshold mumbo-jumbo
    def ingest(self, crash):
        try:
            return self.bucketer.assign_save_bucket(Crash(crash))
        except NotFoundError as e:
            raise Exception(' '.join([e.error, str(e.status_code), repr(e.info)]))

    def bucket(self, threshold, bucket_id):
        query = {
            "filter": {
                "term": {
                    "bucket": bucket_id
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
                      project=None,
                      threshold=self.default_threshold,
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

        if threshold is None:
            threshold = self.default_threshold

        # Filters by lower-bound by default;
        filters = [{
            "range": {
                "date_bucketed": {
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
                                "field": "bucket",
                                "order": {
                                    "_count": "desc"
                                }
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

        return [Bucket(id=b['key'],
                       total=b['doc_count'],
                       project=project,
                       threshold=threshold,
                       top_reports=reports_by_project.get(b['key'], ()))
                for b in top_buckets]

    # TODO catch duplicate and return 303
    def dryrun(self, crash):
        try:
            return self.bucketer.assign_bucket(Crash(crash))
        except NotFoundError as e:
            raise Exception(' '.join([e.error, str(e.status_code), repr(e.info)]))

    def get_crash(self, database_id):
        try:
            return ESCrash(database_id, index='crashes')
        except NotFoundError as e:
            raise KeyError(database_id)

    def delete_crash(database_id):
        # TODO: we have to call ES directly here, theres nothing in Crash/ESCrash or Bucketer to handle this case
        # maybe ESCrash(database_id).delete()
        raise NotImplementedError("BUT WHY~!~~~~")

    @staticmethod
    def _get_reports_by_bucket(response, _threshold):
        """
        Returns a dictionary of projects => reports, from the response.
        """
        buckets = defaultdict(list)

        raw_hits = response['hits']['hits']

        for hit in raw_hits:
            report = hit['_source']
            # TODO: multiple threshold support.
            bucket_id = report['bucket']
            buckets[bucket_id].append(Crash(report))

        return buckets
