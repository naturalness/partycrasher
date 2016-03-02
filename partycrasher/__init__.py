# -*- coding: UTF-8 -*-

import ConfigParser

from elasticsearch import Elasticsearch, NotFoundError

from partycrasher.crash import Crash
from partycrasher.es_crash import ESCrash, ReportNotFoundError
from partycrasher.bucketer import MLTCamelCase


__version__ = u'0.1.0'


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
        self._bucketer = MLTCamelCase(thresh=0.0,
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

    def top_buckets(self, lower_bound, threshold=None, project=None):
        if threshold is None:
            threshold = self.default_threshold

        # TODO: compute lower-bound properly

        query = {
            "aggs": {
                "top_buckets_since_date": {
                    "date_range": {
                        "field":"date_bucketed",
                        # TODO: determine date range from `since` parameter
                        "ranges":[{"from":"now-7d"}]
                    },
                    "aggs": {
                        "top_buckets": {
                            "cardinality": {
                                "field":"bucket","precision_threshold":0
                            }
                        }
                    }
                }
            }
        }
        response = self.es.search(body=query, index='crashes')
        from pprint import pprint
        pprint(response)

        results = response['aggregations']['top_buckets_since_date']

        return {
            'top_buckets': results['buckets']
        }


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

    def delcrash(database_id):
        # TODO: we have to call ES directly here, theres nothing in Crash/ESCrash or Bucketer to handle this case
        # maybe ESCrash(database_id).delete()
        raise NotImplementedError("BUT WHY~!~~~~")
