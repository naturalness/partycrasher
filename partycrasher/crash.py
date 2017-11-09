#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016 Joshua Charles Campbell

#  This program is free software; you can reditext_typeibute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is ditext_typeibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import print_function

import sys, json, datetime
import dateparser
from collections import OrderedDict

from partycrasher.threshold import Threshold
from partycrasher.project import Project
from partycrasher.bucket import Buckets, Bucket, TopMatch
from partycrasher.pc_dict import PCDict, PCList
from partycrasher.crash_type import CrashType

from six import string_types, text_type

def parse_utc_date(s):
    return dateparser.parse(s, settings={'TIMEZONE': 'UTC',
                                         'RETURN_AS_TIMEZONE_AWARE': False})
            
class Stackframe(PCDict):
    """
    Represents a Stackframe in a crash object. Proxy object for a dictionary.
    """
    __slots__ = tuple()
    
    synonyms = {}
    
    canonical_fields = {
        'depth': {
            'type': int,
            'converter': int,
            },
        'address': {
            'type': text_type,
            'converter': text_type,
            },
        'function': {
            'type': text_type,
            'converter': text_type,
            },
        'args': {
            'type': text_type,
            'converter': text_type,
            },
        'file': {
            'type': text_type,
            'converter': text_type,
            },
        'dylib': {
            'type': text_type,
            'converter': text_type,
            },
    }

class Stacktrace(PCList):
    __slots__ = tuple()
    member_type = Stackframe
    member_converter = Stackframe

class Crash(PCDict):
    
    __slots__ = tuple()

    synonyms = {
        'crash_id': 'database_id', # Mozilla
        'os_ver' : 'os_version', # Mozilla
        'cpu_arch' : 'cpu', # Mozilla
        'frames' : 'stacktrace', # Mozilla
    }

    canonical_fields = {
        'date': {
            'type': datetime.datetime,
            'converter': parse_utc_date,
            },
        'stacktrace': {
            'type': Stacktrace,
            'converter': Stacktrace,
            },
        'database_id': {
            'type': text_type,
            'converter': text_type,
            },
        'project': {
            'type': Project,
            'converter': Project,
            },
        'type': {
            'type': CrashType,
            'converter': CrashType,
            },
        'buckets': {
            'type': Buckets,
            'converter': Buckets,
            },
    }

    def get_bucket_id(self, threshold):
        key = Threshold(threshold).to_elasticsearch()
        try:
            buckets = self['buckets']
        except KeyError:
            raise Exception('No assigned buckets for: {!r}'.format(self))
        try:
            return buckets[key]
        except KeyError:
            raise Exception('Buckets threshold {} not assigned for: '
                            '{!r}'.format(key, self))

    @classmethod
    def load_from_file(cls, path):
        import launchpad_crash
        crash_classes = [ launchpad_crash.LaunchpadCrash ]

        crash = None
        for crash_class in crash_classes:
            try:
                crash = crash_class.load_from_file(path)
            except NotImplementedError:
                raise
            else:
                break
        if crash is None:
            raise NotImplementedError("I don't know how to load this!")
        return crash

    @staticmethod
    def make_id(project, database_id):
        raise NotImplementedError("make_id removed")

    @property
    def id(self):
        return self['database_id']

    @property
    def id_without_project(self):
        return self['database_id']

    def json(self):
        return json.dumps(self, cls=CrashEncoder)

    @classmethod
    def fromjson(cls, s):
        d = json.loads(s)
        assert isinstance(d, dict)
        c = cls(d)
        return c

class CrashEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            serialized = o.isoformat()
            return serialized
        elif isinstance(o, Buckets):
            return o.json_serializable()
        elif isinstance(o, Crash):
            return o.as_dict()
        elif isinstance(o, Stacktrace):
            return o._l
        elif isinstance(o, Stackframe):
            return o.as_dict()
        elif isinstance(o, Bucket):
            return o.as_dict()
        elif isinstance(o, TopMatch):
            return o.as_dict()
        elif isinstance(o, Threshold):
            return text_type(o)
        elif isinstance(o, Project):
            return o.name
        elif isinstance(o, CrashType):
            return o.name
        else:
            return super(CrashEncoder, self).default(o)

def pretty(thing):
    return json.dumps(thing, cls=CrashEncoder, indent=2)


import unittest
class TestCrash(unittest.TestCase):
    exampleCrash1 = Crash({
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

    exampleJson1 = '{\n'\
        '    "CrashCounter": "1",\n'\
        '    "ExecutablePath": "/bin/nbd-server",\n'\
        '    "NonfreeKernelModules": "fglrx",\n'\
        '    "Package": "nbd-server 1:2.9.3-3ubuntu1",\n'\
        '    "PackageArchitecture": "i386",\n'\
        '    "ProcCmdline": "/bin/nbd-server",\n'\
        '    "ProcCwd": "/",\n'\
        '    "ProcEnviron": "PATH=/sbin:/bin:/usr/sbin:/usr/bin",\n'\
        '    "Signal": "11",\n'\
        '    "SourcePackage": "nbd",\n'\
        '    "StacktraceTop": "\\ufffd?? ()",\n'\
        '    "Title": "nbd-server crashed with SIGSEGV",\n'\
        '    "Uname": "Linux mlcochff 2.6.22-7-generic #1 SMP Mon Jun 25 17:33:14 GMT 2007 i686 GNU/Linux",\n'\
        '    "cpu": "i386",\n'\
        '    "date": "2007-06-27T12:04:43",\n'\
        '    "os": "Ubuntu 7.10",\n'\
        '    "stacktrace": [\n'\
        '        {\n'\
        '            "address": "0x0804cbd3",\n'\
        '            "args": "argc=",\n'\
        '            "depth": 0,\n'\
        '            "extra": [\n'\
        '                "\\tserve = (SERVER *) 0x0",\n'\
        '                "\\tservers = (GArray *) 0x8051418",\n'\
        '                "\\terr = (GError *) 0x0"\n'\
        '            ],\n'\
        '            "file": "nbd-server.c:1546",\n'\
        '            "function": "main"\n'\
        '        },\n'\
        '        {\n'\
        '            "address": "0xb7cfcebc",\n'\
        '            "args": "",\n'\
        '            "depth": 1,\n'\
        '            "function": "??"\n'\
        '        },\n'\
        '        {\n'\
        '            "address": "0x00000001",\n'\
        '            "args": "",\n'\
        '            "depth": 2,\n'\
        '            "function": "??"\n'\
        '        },\n'\
        '        {\n'\
        '            "address": "0xbfeff544",\n'\
        '            "args": "",\n'\
        '            "depth": 3,\n'\
        '            "function": "??"\n'\
        '        },\n'\
        '        {\n'\
        '            "address": "0xbfeff54c",\n'\
        '            "args": "",\n'\
        '            "depth": 4,\n'\
        '            "function": "??"\n'\
        '        },\n'\
        '        {\n'\
        '            "address": "0xb7f1b898",\n'\
        '            "args": "",\n'\
        '            "depth": 5,\n'\
        '            "function": "??"\n'\
        '        },\n'\
        '        {\n'\
        '            "address": "0x00000000",\n'\
        '            "args": "",\n'\
        '            "depth": 6,\n'\
        '            "function": "??"\n'\
        '        }\n'\
        '    ],\n'\
        '    "type": "Crash"\n'\
        '}\n'


    def test_serdes(self):
        serdes = Crash.fromjson(self.exampleCrash1.json())
        assert (self.exampleCrash1 == serdes)
        assert len(self.exampleCrash1['stacktrace']) > 1
        assert len(serdes['stacktrace']) > 1

    def test_desser(self):
        assert (json.loads(Crash.fromjson(self.exampleJson1).json()) ==
                json.loads(self.exampleJson1))


if __name__ == '__main__':
    unittest.main()
