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

    def __init__(self, n=3):
        self.n = n

    def get_signature(self, crash):
        signature = ''
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

    def compare(self, a, b):
        for i in range(0, self.n):
            if i >= len(a['stacktrace']):
                if i < len(b['stacktrace']):
                    return False
                else:
                    return True
            if i >= len(b['stacktrace']):
                if i < len(a['stacktrace']):
                    return False
                else:
                    return True
            if a['stacktrace'][i]['function'] is None:
                return False
            if b['stacktrace'][i]['function'] is None:
                return False
            if a['stacktrace'][i]['function'] != b['stacktrace'][i]['function']:
                return False
        return True

class TopNLoose(Comparer):

    def __init__(self, n=3):
        self.n = n

    def compare(self, a, b):
        for i in range(0, self.n):
            if i >= len(a['stacktrace']):
                if i < len(b['stacktrace']):
                    return False
                else:
                    return True
            if i >= len(b['stacktrace']):
                if i < len(a['stacktrace']):
                    return False
                else:
                    return True
            fna = a['stacktrace'][i]['function']
            fnb = b['stacktrace'][i]['function']
            fna = re.sub(r"[^a-zA-Z]", "", fna)
            fnb = re.sub(r"[^a-zA-Z]", "", fnb)
            fna = fna.lower()
            fnb = fnb.lower()
            if fna != fnb:
                return False
        return True

class TopNAddress(Comparer):

    def __init__(self, n=3):
        self.n = n        

    def compare(self, a, b):
        for i in range(0, self.n):
            if i >= len(a['stacktrace']):
                if i < len(b['stacktrace']):
                    return False
                else:
                    return True
            if i >= len(b['stacktrace']):
                if i < len(a['stacktrace']):
                    return False
                else:
                    return True
            try:
                if a['stacktrace'][i]['address'] != b['stacktrace'][i]['address']:
                    return False
            except KeyError:
                return False # treat unknown addresses as never equal
        return True

class TopNFile(Comparer):
    """
    Rule 2. Top frame comparison. From:

          S. Wang, F. Khomh, and Y.  Zou, “Improving bug localization using
          correlations in crash reports,” in 2013 10th IEEE Working Conference
          on Mining Software Repositories (MSR), 2013, pp. 247–256.

    """

    def __init__(self, n=1):
        self.n = n

    @staticmethod
    def compare_frames(a, b):
        # Sentinel object that will NEVER compare equal.
        # >>> (NeverEqual == NeverEqual) == False
        NeverEqual = float('nan')
        return a.stacktrace[0].get('file', NeverEqual) == \
               b.stacktrace[0].get('file', NeverEqual)

    def compare(self, a, b):
        """
        Two crashes are correlated if the top stack frame occured in the same
        **SOURCE** file.
        """
        assert len(a.stacktrace) > 0
        assert len(b.stacktrace) > 0

        for sa, sb, _ in zip(a.stacktrace, b.stacktrace, xrange(self.n)):
            if not self.compare_frame(sa, sb):
                return False
        return True


import unittest
class TestTopN(unittest.TestCase):
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

