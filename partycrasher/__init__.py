# -*- coding: UTF-8 -*-

import ConfigParser

from elasticsearch import Elasticsearch, NotFoundError

from partycrasher.crash import Crash
from partycrasher.es_crash import ESCrash
from partycrasher.bucketer import MLTCamelCase


__version__ = "0.0.1"


class PartyCrasher(object):
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser({'elastic': ''})
        self.esServers = self.config.get('DEFAULT', 'elastic').split()
        if len(self.esServers) < 1:
            self.esServers = ['localhost']
        self.es = Elasticsearch(self.esServers)
        self.bucketer = MLTCamelCase(thresh=4.0, lowercase=False, only_stack=False, index='crashes', es=self.es, name="bucket")
        self.bucketer.create_index()

    # TODO catch duplicate and return 303
    # TODO multi-bucket multi-threshold mumbo-jumbo
    def ingest(self, crash):
        try:
            return self.bucketer.assign_save_bucket(Crash(crash))
        except NotFoundError as e:
            raise Exception(' '.join([e.error, str(e.status_code), repr(e.info)]))

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
