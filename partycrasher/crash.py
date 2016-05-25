#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import json, datetime
import dateparser
from collections import OrderedDict

from threshold import Threshold


# This is the separator which is meant to be used when turning
# stack traces into strings, between levels of the stack, going
# DOWN from the TOP (most recent call FIRST)
STACK_SEPARATOR = u' ≻ '

class Buckets(object):
    """Proxy for OrderedDict"""
    def __init__(self, *args, **kwargs):
        self._od = OrderedDict(*args, **kwargs)

    def __getattr__(self, a):
        return getattr(self._od, a)

    def __setitem__(self, *args, **kwargs):
        return self._od.__setitem__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._od.__getitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self._od.__delitem__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, Buckets):
            return self._od.__eq__(other._od)
        else:
            return self._od.__eq__(other)

    def copy(self, *args, **kwargs):
        new = Buckets()
        new._od = self._od.copy()
        return new

    # TODO: automatically convert keys of wrong type to Threshold

class Stackframe(dict):
    pass

class Stacktrace(list):

    stackframe_class = Stackframe

    """A list which can only contain stackframes..."""
    def __init__(self, value=[], **kwargs):
        if isinstance(value, list):
            if len(value) == 0:
                return
            else:
                self.extend(map(self.stackframe_class, value))
        else:
            raise AttributeError

    def extend(self, arg):
        for a in arg:
            assert isinstance(a, self.stackframe_class)
        return super(Stacktrace, self).extend(arg)

    def append(self, *args):
        return self.extend(args)

    def __setitem__(self, index, value):
        for v in value:
            assert isinstance(v, self.stackframe_class)
        return super(Stacktrace, self).__setitem__(index, value)

    def __setslice__(self, i, j, seq):
        for v in seq:
            assert isinstance(v, self.stackframe_class)
        return super(Stacktrace, self).__setitem__(i, j, seq)

    def __eq__(self, other):
        return (super(Stacktrace, self).__eq__(other)
                and self.__class__ == other.__class__)

# TODO: MOVE DATE STUFF HERE.

class Crash(dict):

    stacktrace_class = Stacktrace

    synonyms = {
        'crash_id': 'database_id', # Mozilla
        'os_ver' : 'os_version', # Mozilla
        'cpu_arch' : 'cpu', # Mozilla
        'frames' : 'stacktrace', # Mozilla
    }
    # Code review: can use a set()/frozenset() for this.
    breakapart = {
        'crash_info' : 1, # Mozilla
        'system_info' : 1, # Mozilla
    }

    canonical_fields = {
        'date': {
            'type': datetime.datetime,
            'converter': dateparser.parse,
            },
        'stacktrace': {
            'type': Stacktrace,
            'converter': Stacktrace,
            },
        'database_id': {
            'type': bytes,
            'converter': bytes,
            },
        'project': {
            'type': bytes,
            'converter': bytes,
            },
        'buckets': {
            'type': Buckets,
            'converter': Buckets,
            },
    }

    def __init__(self, *args):
        super(Crash, self).__init__(*args)
        if not (len(args) == 1 and isinstance(args[0], self.__class__)):
            self.normalize()

    def __eq__(self, other):
        return (super(Crash, self).__eq__(other)
                and self.__class__ == other.__class__)

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

    def __getitem__(self, key):
        if key in self.synonyms:
            return super(Crash, self).__getitem__(self.synonyms[key])
        else:
            return super(Crash, self).__getitem__(key)

    def __setitem__(self, key, val):
        # Translates key synonyms to their "canonical" key.
        synonyms = self.synonyms
        # First force strings to be unicoded
        if isinstance(key, bytes):
            key = key.decode(encoding='utf-8', errors='replace')
        if isinstance(val, bytes):
            val = val.decode(encoding='utf-8', errors='replace')
        if key in synonyms:
            return super(Crash, self).__setitem__(synonyms[key], val)
        elif key in self.breakapart:
            # Inline all keys from the assigned value to THIS dict.
            if isinstance(val, dict):
                # Code review: use self.update() instead;
                # though... Not sure if dict.update() uses __setitem__
                # internally.
                for key2 in val:
                    # It's okay to recurse on this function using indexing
                    # syntax: self[key2] = val[key2]
                    self.__setitem__(key2, val[key2])
            else:
                # Code review: Is TypeError more semantically related?
                raise ValueError("Expected a dict!")
        elif key == 'crashing_thread': # Mozilla
            if (isinstance(val, dict)):
                for key2 in val:
                    self.__setitem__(key2, val[key2])
            else:
                raise ValueError("Expected a dict!")
        elif key in self.canonical_fields:
            if isinstance(val, self.canonical_fields[key]['type']):
                return super(Crash, self).__setitem__(key, val)
            else:
                if self.canonical_fields[key]['converter'] is not None:
                    return super(Crash, self).__setitem__(key,
                        self.canonical_fields[key]['converter'](val))
                else:
                    raise ValueError(key + " must be of type " +
                             self.canonical_fields[key]['type'].__name__)
        else:
            return super(Crash, self).__setitem__(key, val)

    @property
    def stacktrace(self):
        return self['stacktrace']

    @property
    def project(self):
        return self['project']

    @property
    def id(self):
        return self['database_id']

    def normalize(self):
        """
        wat.
        """
        # Use self.keys() so that we can remove items (it is impossible to
        # modify the dictionary during iteration).
        for key in self.keys():
            # __setitem__ WILL change the
            value = self[key]
            del self[key]
            self.__setitem__(key, value)

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
        else:
            return json.JSONEncoder.default(self, o)

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
