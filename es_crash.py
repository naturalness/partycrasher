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

import datetime, time
from crash import Crash, Stacktrace, Stackframe
from elasticsearch import Elasticsearch
from weakref import WeakValueDictionary

class ESCrashMeta(type):
    # The purpose of all of this shit is to ensure that we don't
    # end up with two copies of the same crash in elastic search
    # in memory because then they would fall out of sync, and
    # cause really annoying and hard to find bugs, etc.
    # So, if a ESCrash with the same database_id is already
    # retrieved/added to ES and is already in memory, then we
    # just return that very same object
    # It's not my fault, the only way to do this is with metaclasses.
    # I seriously tried.
    _crashes = WeakValueDictionary()
    def __call__(cls, crash=None):
        cls.index_create()
        # This is the case that the constructor was called with a whole
        # crash datastructure
        if isinstance(crash, Crash):
            if 'database_id' in crash:
                # The case that we already have it in memory
                if crash['database_id'] in cls._crashes:
                    already = cls._crashes[crash['database_id']]
                    assert(Crash(already) == crash)
                    return already
                # We don't have it in memory so see if its already in ES
                existing = cls.getrawbyid(crash['database_id'])
                if not existing is None:
                    # It is already in elastic search
                    # make sure its the same data
                    assert(existing == crash)
                    newish = super(ESCrashMeta, cls).__call__(existing)
                    # cache it as a weak reference
                    cls._crashes[crash['database_id']] = newish
                    return newish
                # It's not in ES, so add it
                else:
                    r = cls.es.create(index='crashes',
                                doc_type='crash',
                                body=crash,
                                id=crash['database_id'],
                                )
                    assert r['created']
                    new = super(ESCrashMeta, cls).__call__(crash)
                    # Cache it as a weak reference
                    cls._crashes[crash['database_id']] = new
                    return new
            else:
                raise Exception("Crash with no database_id!")
        # The case where the constructor is called with a database id only
        elif isinstance(crash, str):
            if crash in cls._crashes:
                return cls._crashes[crash]
            existing = cls.getrawbyid(crash)
            if not existing is None:
                newish = super(ESCrashMeta, cls).__call__(existing)
                cls._crashes[crash] = newish
                return newish
            else:
                raise Exception("ID not found!")
        else:
            raise ValueError()


class ESCrash(Crash):
    """Class for a crash that's stored in Elastic"""
    __metaclass__ = ESCrashMeta

    # Global ES connection
    es = Elasticsearch()
    crashes = {}
    
    @classmethod
    def getrawbyid(cls, database_id):
        if database_id in cls.crashes:
            return cls.crashes[database_id]
        r = cls.es.search(
            index='crashes',
            body={
                'query': {
                    'filtered':{
                        'query': {
                            'match_all': {}
                            },
                        'filter': {
                            'term': {
                                'database_id': database_id,
                                }
                            }
                        }
                    }
                },
            )
        if r['hits']['total'] == 0:
            return None
        elif r['hits']['total'] > 1:
            raise Exception("The ID occurs in ES twice, which shouldn't be possible, since they are all supposed to be stored with their document ID equal to the database ID.")
        else:
            # should this be ESCRash.__base__?
            return Crash(r['hits']['hits'][0]['_source'])
    
    @classmethod
    def index_create(cls):
        if cls.es.indices.exists(index='crashes'):
            return
        else:
            #known_types = {
                #datetime : 'date',
                #Stacktrace: None,
            #}    
            #properties = {}
            #for field, info in cls.canonical_fields.iteritems():
                #ftype = known_types[info['type']]
                #properties[field] = {
                    #'type': ftype
                    #}
            cls.es.indices.create(index='crashes',
                body={
                    'mappings': {
                        'crash': {
                            'properties': {
                                'database_id': {
                                    'type': 'string',
                                    'index': 'not_analyzed'
                                    },
                                'bucket': {
                                    'type': 'string',
                                    'index': 'no',
                                    }
                                }
                            }
                        }
                    }
                )
            cls.es.cluster.health(wait_for_status='yellow')
    def __init__(self, *args):
        self.hot = False
        super(ESCrash, self).__init__(*args)
        self.hot = True

    def __setitem__(self, key, val):
        if key in self:
            oldval = self[key]
        else:
            oldval = None
        super(ESCrash, self).__setitem__(key, val)
        newval = self[key]
        if (oldval != newval) and self.hot:
            r = self.es.update(index='crashes',
                        doc_type='crash',
                        id=self['database_id'],
                        body={
                            'doc': {
                                    key: val
                                }
                            }
                        )


import unittest
class TestCrash(unittest.TestCase):

    exampleCrash1 = Crash({
        'database_id': 'exampleCrash1',
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

