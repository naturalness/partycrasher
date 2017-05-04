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
from abc import ABCMeta

import elasticsearch
from elasticsearch import Elasticsearch

from partycrasher.pc_exceptions import IdenticalReportError
from partycrasher.crash import Crash, Stacktrace, Stackframe, CrashEncoder, Buckets
from partycrasher.threshold import Threshold

import json # For debugging

class ReportNotFoundError(KeyError):
    """
    Raised when... the crash is not found!
    """

class ESCrashMeta(ABCMeta):
    # The purpose of all of this shit is to ensure that we don't
    # end up with two copies of the same crash in elastic search
    # in memory because then they would fall out of sync, and
    # cause really annoying and hard to find bugs, etc.
    # So, if a ESCrash with the same database_id is already
    # retrieved/added to ES and is already in memory, then we
    # just return that very same object
    # It's not my fault, the only way to do this is with metaclasses.
    # I seriously tried.
    _cached = {}

    def __call__(cls, crash=None, index=None, unsafe=False):
        # This is the case that the constructor was called with a whole
        # crash datastructure
        if index is None:
            raise ValueError('No ElasticSearch index specified!')
        if index not in cls._cached:
            cls._cached[index] = WeakValueDictionary()
        if isinstance(crash, Crash):
            if 'database_id' in crash:
                # The case that we already have it in memory
                if crash['database_id'] in cls._cached[index]:
                    already = cls._cached[index][crash['database_id']]
                    assert(Crash(already) == crash)
                    return already
                # We don't have it in memory so see if its already in ES
                if not unsafe:
                    existing = cls.getrawbyid(crash['database_id'], index=index)
                else:
                    existing = None

                if not existing is None:

                    if existing != crash:
                        # We already know of it! Raise an identical report
                        # error.
                        # TODO: not resilient to multiple running instances of
                        # PartyCrasher :c
                        raise IdenticalReportError(existing)

                    # It is already in elastic search
                    # make sure its the same data
                    newish = super(ESCrashMeta, cls).__call__(crash=existing, index=index)
                    # cache it as a weak reference
                    cls._cached[index][crash['database_id']] = newish
                    return newish
                # It's not in ES, so add it
                else:
                    # Ensure this is UTC ISO format
                    now = datetime.datetime.utcnow()
                    crash.setdefault('date', now.isoformat())
                    if 'stacktrace' in crash and crash['stacktrace'] is not None:
                        for frame in crash['stacktrace']:
                            if 'logdf' in frame:
                                raise ValueError("logdf should not be stored in ElasticSearch")
                    crash_es_safe = crash.copy()
                    try:
                        response = cls.es.create(index=index,
                                                 doc_type='crash',
                                                 body=json.dumps(crash, cls=ESCrashEncoder),
                                                 id=crash['database_id'],
                                                 refresh=True)
                        assert response['created']
                    except elasticsearch.exceptions.ConflictError as e:
                        if (('DocumentAlreadyExistsException' in e.error)
                            or ('document_already_exists_exception' in e.error)):
                            print("Got DocumentAlreadyExistsException on create!", file=sys.stderr)
                            already = None
                            while already is None:
                                print("Waiting for ElasticSearch to catch up...", file=sys.stderr)
                                time.sleep(1) # Let ES think about its life...
                                already = cls.getrawbyid(crash['database_id'], index=index)
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
                    new = super(ESCrashMeta, cls).__call__(crash=crash, index=index)
                    # Cache it as a weak reference
                    cls._cached[index][crash['database_id']] = new
                    return new
            else:
                raise Exception("Crash with no database_id!")
        # The case where the constructor is called with a database id only
        elif isinstance(crash, str) or isinstance(crash, unicode):
            if crash in cls._cached[index]:
                return cls._cached[index][crash]
            existing = cls.getrawbyid(crash, index=index)
            if existing is not None:
                # Found it in ElasticSearch!
                newish = super(ESCrashMeta, cls).__call__(crash=existing, index=index)
                cls._cached[index][crash] = newish
                return newish
            else:
                raise ReportNotFoundError(crash)
        else:
            raise ValueError()


class ESCrash(Crash):
    """Class for a crash that's stored in Elastic"""
    __metaclass__ = ESCrashMeta

    # Global ES connection
    es = None
    crashes = {}

    @classmethod
    def getrawbyid(cls, database_id, index=None):
        if index is None:
            raise ValueError('No ElasticSearch index specified!')
        if cls.es is None:
            raise RuntimeError('Forgot to monkey-patch ES connection to ESCrash!')

        if index in cls.crashes:
            if database_id in cls.crashes[index]:
                return cls.crashes[database_id]
        try:
            response = cls.es.get(index=index, id=database_id)
        except elasticsearch.exceptions.NotFoundError:
            return None

        return Crash(response['_source'])

    def __init__(self, index=None, crash=None):
        if index is None:
            raise ValueError('No ElasticSearch index specified!')
        self.index = index
        self.hot = False
        super(ESCrash, self).__init__(crash)
        self.hot = True

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
    def hacky_serialize_thresholds(value):
        """
        Must serialize thresholds, but ElasticSearch is all like... nah.
        Actually the problem is that python dumps doesn't allow non-string keys?
        """
        assert isinstance(value, Buckets)

        new_dict = value._od.copy()
        for key in value.keys():
            if not isinstance(key, Threshold):
                continue
            # Change threshold to saner value.
            new_dict[key.to_elasticsearch()] = value[key]
            del new_dict[key]
        return new_dict

    def default(self, o):
        #assert False
        #print(type(o), file=sys.stderr)
        if isinstance(o, Buckets):
            return self.hacky_serialize_thresholds(o)
        else:
            return CrashEncoder.default(self, o)

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
