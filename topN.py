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

from crash import Crash, Stacktrace, Stackframe
from comparer import Comparer
import re

class TopN(Comparer):

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
