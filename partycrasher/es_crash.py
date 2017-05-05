#!/usr/bin/env python

#  Copyright (C) 2015, 2016 Joshua Charles Campbell

#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import print_function
import sys
import datetime
import time
from weakref import WeakValueDictionary
from collections import OrderedDict
import json

from six import string_types

import elasticsearch
from elasticsearch import Elasticsearch

import dateparser

from partycrasher.pc_exceptions import IdenticalReportError, ReportNotFoundError
from partycrasher.crash import (
  Crash, 
  Stacktrace, 
  Stackframe, 
  CrashEncoder, 
  pretty,
  parse_utc_date,
  )
from partycrasher.threshold import Threshold
from partycrasher.bucket import Buckets
from partycrasher.pc_dict import Dict
from partycrasher.es_bucket import ESBuckets

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

def parse_es_date(s):
    return parse_utc_date(s)

class ESCrash(Crash):
    """Class for a crash that's stored in Elastic"""

    # Global ES connection
    es = None
    
    """ Dict of WeakValueDictionarys that caches the thing in ES.
        Used to prevent multiple copies of the same ESCrash from existing
        in memory.
    """
    crashes = {}
    
    @staticmethod
    def de_elastify(d):
        """ Take a dict and de_elastifies it, turning it into a Crash
            (but not an ESCrash: to do that call ESCrash())
        """
        if 'buckets' in d:
            d['buckets'] = ESBuckets(d['buckets'])
        if 'date' in d:
            d['date'] = parse_es_date(d['date'])
        return Crash(d)
    
    def getrawbyid(self, database_id):
        index = self.index
        if index is None:
            raise ValueError('No ElasticSearch index specified!')
        if self.es is None:
            raise RuntimeError('Forgot to monkey-patch ES connection to ESCrash!')

        if index in self.crashes:
            assert database_id not in self.crashes[self.index]

        try:
            response = self.es.get(index=self.index, id=database_id)
        except elasticsearch.exceptions.NotFoundError:
            return None
        
        return self.de_elastify(response['_source'])
      
    def load_from_es(self, dbid):
        if dbid in self.crashes[self.index]:
            self._d = self.crashes[self.index][dbid]
            self.hot = True
            return
        
        existing = self.getrawbyid(dbid)
        if existing is not None:
            # Found it in ElasticSearch!
            self.crashes[self.index][dbid] = existing._d
            self._d = existing._d
            self.hot = True
        else:
            raise ReportNotFoundError(dbid)
    
    def elastify(self):
        """ Produce JSON representation of ESCrash object for use with
            ElasticSearch.
        """
        #debug(json.dumps(self, cls=ESCrashEncoder, indent=2))
        return elastify(self)
    
    def add_to_es(self):
        #debug("adding")
        if 'stacktrace' in self and self['stacktrace'] is not None:
            for frame in self['stacktrace']:
                if 'logdf' in frame:
                    raise ValueError("logdf should not be stored in ElasticSearch")
        try:
            assert "buckets" in self
            assert "date" in self
            body = self.elastify()
            response = self.es.create(index=self.index,
                                      doc_type='crash',
                                      body=body,
                                      id=self['database_id'],
                                      refresh=True)
            assert response['created']
        except elasticsearch.exceptions.ConflictError as e:
            if (('DocumentAlreadyExistsException' in e.error)
                or ('document_already_exists_exception' in e.error)):
                print("Got DocumentAlreadyExistsException on create!", file=sys.stderr)
                already = None
                while already is None:
                    print("Waiting for ElasticSearch to catch up...", file=sys.stderr)
                    time.sleep(1) # Let ES think about its life...self
                    already = self.getrawbyid(crash['database_id'])
                if not already is None:
                    # It got added...
                    # I think what is happening here is that the
                    # python client lib is retrying after the create
                    # times out, but ES did recieve the create and
                    # created the document but didn't return in time
                    pass
                else:
                    raise
            else:
                raise

      
    def check_sync(self):
        if 'database_id' not in self:
            raise Exception("Crash with no database_id!")

        # The case that we already have it in memory
        if self['database_id'] in self.crashes[self.index]:
            already = self.crashes[self.index][self['database_id']]
            # already should be a cached _d
            #debug(pretty(self._d))
            #debug(pretty(already))
            assert(already == self._d)
            self._d = already
            return

        # We don't have it in memory so see if its already in ES
        if not self.unsafe:
            existing = self.getrawbyid(self['database_id'])
        else:
            existing = None

        if existing is None:
            # It's not in ES, so add it
            self.add_to_es()
        else:
            # It is already in elastic search
            # make sure its the same data
            if existing._d != self._d:
                # We already know of it! Raise an identical report
                # error.
                raise IdenticalReportError(existing)

        # cache it as a weak reference
        self.crashes[self.index][self['database_id']] = self._d
        self.hot = True

    def __init__(self, index, crash, unsafe=False):
        self.index = index
        self.hot = False
        self.unsafe = unsafe
        if index not in self.crashes:
            self.crashes[index] = WeakValueDictionary()
        if isinstance(crash, Crash):
            self.set_d(crash._d.copy())
            self.check_sync()
        elif isinstance(crash, string_types):
            self.load_from_es(crash)
        else:
            raise TypeError("Can't load/save a " + crash.__class__.__name__)
        assert self.hot

    def __setitem__(self, key, val):
        """
        crash[key] = value

        Updates the crash; propegates the update to ElasticSearch.
        Currently, there's no batching of requests, so try to avoid changing values.
        """

        # Keep the old value of the key, if it exists,
        oldval = self.get(key, None)

        # Let the super class do weird value remapping stuff.
        super(ESCrash, self).__setitem__(key, val)
        # After the super class is done its magic, the value may have
        # changed...
        newval = self[key]

        # Update the crash in ElasticSearch.
        if (oldval != newval) and self.hot:
            body={
                'doc': {
                        key: newval
                    }
                }
            r = self.es.update(index=self.index,
                        doc_type='crash',
                        id=self['database_id'],
                        # use our own serializer instead of py-elasticsearch
                        body=json.dumps(body, cls=ESCrashEncoder)
                        )

    def delete():
        del _cached[self['database_id']]
        raise NotImplementedError
        # TODO: code to delete from ES
        # TODO: clear self

class ESCrashEncoder(CrashEncoder):

    @staticmethod
    def hacky_serialize_thresholds(buckets):
        """
        Must serialize thresholds, but ElasticSearch is all like... nah.
        Actually the problem is that python dumps doesn't allow non-string keys?
        """
        assert isinstance(buckets, Buckets)

        new_dict = OrderedDict()
        for key, value in buckets.items():
            if not isinstance(key, Threshold):
                continue
            # Change threshold to saner value.
            key = key.to_elasticsearch()
            value = value['id']
            new_dict[key] = value
        return new_dict

    def default(self, o):
        #assert False
        #print(type(o), file=sys.stderr)
        if isinstance(o, Buckets):
            return self.hacky_serialize_thresholds(o)
        else:
            return CrashEncoder.default(self, o)

def elastify(o, **kwargs):
    return json.dumps(o, cls=ESCrashEncoder, **kwargs)

import unittest
class TestCrash(unittest.TestCase):

    exampleCrash1 = Crash({
        'database_id': 'exampleCrash1',
        'project': 'Ubuntu',
        'CrashCounter': '1',
        'ExecutablePath': '/bin/nbd-server',
        'NonfreeKernelModules': 'fglrx',
        'Package': 'nbd-server 1:2.9.3-3ubuntu1',
        'PackageArchitecture': 'i386',
        'ProcCmdline': '/bin/nbd-server',
        'ProcCwd': '/',
        'ProcEnviron': 'PATH=/sbin:/bin:/usr/sbin:/usr/bin',
        'Signal': '11',
        'SourcePackage': 'nbd',
        'StacktraceTop': '\xa0?? ()',
        'Title': 'nbd-server crashed with SIGSEGV',
        'Uname': 'Linux mlcochff 2.6.22-7-generic #1 SMP Mon Jun 25 17:33:14 GMT 2007 i686 GNU/Linux',
        'cpu': 'i386',
        'date': datetime.datetime(2007, 6, 27, 12, 4, 43),
        'os': 'Ubuntu 7.10',
        'stacktrace': Stacktrace([
                        Stackframe({
                            'address': u'0x0804cbd3',
                            'args': u'argc=',
                            'depth': 0,
                            'extra': [   u'\tserve = (SERVER *) 0x0',
                                        u'\tservers = (GArray *) 0x8051418',
                                        u'\terr = (GError *) 0x0'],
                            'file': u'nbd-server.c:1546',
                            'function': u'main'}),
                        Stackframe({
                            'address': u'0xb7cfcebc',
                            'args': u'',
                            'depth': 1,
                            'function': u'??'}),
                        Stackframe({
                            'address': u'0x00000001',
                            'args': u'',
                            'depth': 2,
                            'function': u'??'}),
                        Stackframe({
                            'address': u'0xbfeff544',
                            'args': u'',
                            'depth': 3,
                            'function': u'??'}),
                        Stackframe({
                            'address': u'0xbfeff54c',
                            'args': u'',
                            'depth': 4,
                            'function': u'??'}),
                        Stackframe({
                            'address': u'0xb7f1b898',
                            'args': u'',
                            'depth': 5,
                            'function': u'??'}),
                        Stackframe({
                            'address': u'0x00000000',
                            'args': u'',
                            'depth': 6,
                            'function': u'??'})
                        ]),
        'type': 'Crash'})

    def test_es_reachable_working(self):
        es = Elasticsearch(hosts=['localhost'])
        es.indices.create(index='test-index', ignore=400)
        es.indices.delete(index='test-index', ignore=[400, 404])

    def test_es_add(self):
        import gc
        es = ESCrash.es
        es.indices.delete(index='crashes', ignore=[400, 404])
        mycrash = ESCrash(self.exampleCrash1)
        mycrash_dupe = ESCrash(self.exampleCrash1)
        assert mycrash is mycrash_dupe
        mycrash_another = ESCrash('exampleCrash1')
        assert mycrash is mycrash_another
        del mycrash
        del mycrash_another
        del mycrash_dupe
        gc.collect()
        es.indices.flush(index='crashes')
        time.sleep(1)
        fetched_from_es = ESCrash('exampleCrash1')
        fetched_from_es_undone = Crash(fetched_from_es)
        assert fetched_from_es_undone == self.exampleCrash1
        fetched_from_es['cpu'] = 'amd64'


if __name__ == '__main__':
    unittest.main()
