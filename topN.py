#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2016 Joshua Charles Campbell

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

from crash import Crash, Stacktrace, Stackframe, STACK_SEPARATOR
from comparer import Comparer
import re

class TopN(Comparer):

    def __init__(self, n=3, *args, **kwargs):
        super(TopN, self).__init__(*args, **kwargs)
        self.n = n

    def get_signature(self, crash):
        signature = u''
        for i in range(0, self.n):
            if i >= len(crash['stacktrace']):
                return signature
            if len(signature) > 0:
                signature += STACK_SEPARATOR
            if crash['stacktrace'][i]['function'] is None:
                # This depends on the assumption that the database_id is
                # unique, which is enforced by es_crash.py
                signature += crash['database_id'] + "#" + str(i)
                continue
            signature += crash['stacktrace'][i]['function']
        return signature

class TopNLoose(TopN):
    # TODO: NEEDS TESTS

    def get_signature(self, crash):
        signature = u''
        for i in range(0, self.n):
            if i >= len(crash['stacktrace']):
                return signature
            if len(signature) > 0:
                signature += STACK_SEPARATOR
            if crash['stacktrace'][i]['function'] is None:
                # This depends on the assumption that the database_id is
                # unique, which is enforced by es_crash.py
                signature += crash['database_id'] + "#" + str(i)
                continue
            fn = crash['stacktrace'][i]['function']
            fn = re.sub(r"[^a-zA-Z]", "", fn)
            fn = fn.lower()
            signature += fn
        return signature

class TopNAddress(TopN):

    def get_signature(self, crash):
        signature = u''
        for i in range(0, self.n):
            if i >= len(crash['stacktrace']):
                return signature
            if len(signature) > 0:
                signature += STACK_SEPARATOR
            if ('address' not in crash['stacktrace'][i]
                or crash['stacktrace'][i]['address'] is None):
                # This depends on the assumption that the database_id is
                # unique, which is enforced by es_crash.py
                signature += crash['database_id'] + "#" + str(i)
                continue
            signature += crash['stacktrace'][i]['address']
        return signature

class TopNFile(Comparer):
    """
    Rule 2. Top frame comparison. From:

          S. Wang, F. Khomh, and Y.  Zou, “Improving bug localization using
          correlations in crash reports,” in 2013 10th IEEE Working Conference
          on Mining Software Repositories (MSR), 2013, pp. 247–256.

    """

    def __init__(self, n=1, *args, **kwargs):
        super(TopNFile, self).__init__(*args, **kwargs)
        self.n = n

    def get_signature(self, crash):
        signature = u''
        for i in range(0, self.n):
            if i >= len(crash['stacktrace']):
                return signature
            if len(signature) > 0:
                signature += STACK_SEPARATOR
            
            if ('file' not in crash['stacktrace'][i]
                or crash['stacktrace'][i]['file'] is None):
                # This depends on the assumption that the database_id is
                # unique, which is enforced by es_crash.py
                signature += crash['database_id'] + "#" + str(i)
                continue
            signature += crash['stacktrace'][i]['file']
        return signature

class TopNModule(Comparer):
    """
    Rule 2. Top frame comparison. From:

          S. Wang, F. Khomh, and Y.  Zou, “Improving bug localization using
          correlations in crash reports,” in 2013 10th IEEE Working Conference
          on Mining Software Repositories (MSR), 2013, pp. 247–256.

    """

    def __init__(self, n=1, *args, **kwargs):
        super(TopNModule, self).__init__(*args, **kwargs)
        self.n = n

    def get_signature(self, crash):
        signature = u''
        for i in range(0, self.n):
            if i >= len(crash['stacktrace']):
                return signature
            if len(signature) > 0:
                signature += STACK_SEPARATOR
            #print crash['stacktrace'][i]
            if ('file' in crash['stacktrace'][i]
                and not crash['stacktrace'][i]['file'] is None):
                signature += crash['stacktrace'][i]['file']
                continue
            if ('dylib' in crash['stacktrace'][i]
                and not crash['stacktrace'][i]['dylib'] is None):
                signature += crash['stacktrace'][i]['dylib']
                continue
            # This depends on the assumption that the database_id is
            # unique, which is enforced by es_crash.py
            signature += crash['database_id'] + "#" + str(i)
        return signature

import unittest
class TestTopN(unittest.TestCase):
    exampleJson1 = '{\n'\
        '        "CrashCounter": "1",\n'\
        '        "ExecutablePath": "/usr/bin/nm-applet",\n'\
        '        "NonfreeKernelModules": "cdrom",\n'\
        '        "Package": "network-manager-gnome 0.6.5-0ubuntu3",\n'\
        '        "PackageArchitecture": "i386",\n'\
        '        "ProcCmdline": "nm-applet --sm-disable",\n'\
        '        "ProcCwd": "/home/jerrid",\n'\
        '        "ProcEnviron": "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games",\n'\
        '        "Signal": "11",\n'\
        '        "SourcePackage": "network-manager-applet",\n'\
        '        "StacktraceTop": "?? ()",\n'\
        '        "Title": "nm-applet crashed with SIGSEGV",\n'\
        '        "Uname": "Linux kws3 2.6.22-7-generic #1 SMP Mon Jun 25 17:33:14 GMT 2007 i686 GNU/Linux",\n'\
        '        "UserGroups": "adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video",\n'\
        '        "bucket": "15",\n'\
        '        "cpu": "i386",\n'\
        '        "database_id": "launchpad:122451",\n'\
        '        "date": "2007-06-26T17:37:21",\n'\
        '        "os": "Ubuntu 7.10",\n'\
        '        "stacktrace": [\n'\
        '            {\n'\
        '                "address": "0x0805f92c",\n'\
        '                "args": "",\n'\
        '                "depth": 0,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0x085e5618",\n'\
        '                "args": "",\n'\
        '                "depth": 1,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0x085e5618",\n'\
        '                "args": "",\n'\
        '                "depth": 2,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xbfc06a88",\n'\
        '                "args": "",\n'\
        '                "depth": 3,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xbfc06a84",\n'\
        '                "args": "",\n'\
        '                "depth": 4,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xb730fa28",\n'\
        '                "args": "",\n'\
        '                "depth": 5,\n'\
        '                "dylib": "/usr/lib/libgnome-keyring.so.0",\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xbfc06a88",\n'\
        '                "args": "",\n'\
        '                "depth": 6,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0x00000000",\n'\
        '                "args": "",\n'\
        '                "depth": 7,\n'\
        '                "function": null\n'\
        '            }\n'\
        '        ],\n'\
        '        "type": "Crash"\n'\
        '}\n'
                        
    # Different from 1 only in database_id, and one missing address
    exampleJson2 = '{\n'\
        '        "CrashCounter": "1",\n'\
        '        "ExecutablePath": "/usr/bin/nm-applet",\n'\
        '        "NonfreeKernelModules": "cdrom",\n'\
        '        "Package": "network-manager-gnome 0.6.5-0ubuntu3",\n'\
        '        "PackageArchitecture": "i386",\n'\
        '        "ProcCmdline": "nm-applet --sm-disable",\n'\
        '        "ProcCwd": "/home/jerrid",\n'\
        '        "ProcEnviron": "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games",\n'\
        '        "Signal": "11",\n'\
        '        "SourcePackage": "network-manager-applet",\n'\
        '        "StacktraceTop": "?? ()",\n'\
        '        "Title": "nm-applet crashed with SIGSEGV",\n'\
        '        "Uname": "Linux kws3 2.6.22-7-generic #1 SMP Mon Jun 25 17:33:14 GMT 2007 i686 GNU/Linux",\n'\
        '        "UserGroups": "adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video",\n'\
        '        "bucket": "15",\n'\
        '        "cpu": "i386",\n'\
        '        "database_id": "launchpad:122451B",\n'\
        '        "date": "2007-06-26T17:37:21",\n'\
        '        "os": "Ubuntu 7.10",\n'\
        '        "stacktrace": [\n'\
        '            {\n'\
        '                "address": "0x0805f92c",\n'\
        '                "args": "",\n'\
        '                "depth": 0,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0x085e5618",\n'\
        '                "args": "",\n'\
        '                "depth": 1,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "args": "",\n'\
        '                "depth": 2,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xbfc06a88",\n'\
        '                "args": "",\n'\
        '                "depth": 3,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xbfc06a84",\n'\
        '                "args": "",\n'\
        '                "depth": 4,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xb730fa28",\n'\
        '                "args": "",\n'\
        '                "depth": 5,\n'\
        '                "dylib": "/usr/lib/libgnome-keyring.so.0",\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0xbfc06a88",\n'\
        '                "args": "",\n'\
        '                "depth": 6,\n'\
        '                "function": null\n'\
        '            },\n'\
        '            {\n'\
        '                "address": "0x00000000",\n'\
        '                "args": "",\n'\
        '                "depth": 7,\n'\
        '                "function": null\n'\
        '            }\n'\
        '        ],\n'\
        '        "type": "Crash"\n'\
        '}\n'

    def test_no_function(self):
        should_contain = 'launchpad:122451#0'
        crash = Crash.fromjson(self.exampleJson1)
        topn = TopN(3)
        topna = TopNAddress(3)
        topnf = TopNFile(3)
        signature = topn.get_signature(crash)
        assert 'launchpad:122451#0' in signature
        print repr(signature)
        assert signature == \
            u'launchpad:122451#0 ≻ launchpad:122451#1 ≻ launchpad:122451#2'
        assert topna.get_signature(crash) == \
            u'0x0805f92c ≻ 0x085e5618 ≻ 0x085e5618'
        crash2 = Crash.fromjson(self.exampleJson2)
        assert not topn.compare(crash, crash2)
        assert topn.compare(crash, crash)
        assert not topna.compare(crash, crash2)
        assert topna.compare(crash, crash)
        assert not topnf.compare(crash, crash2)
        assert topnf.compare(crash, crash)
        
if __name__ == '__main__':
    unittest.main()

