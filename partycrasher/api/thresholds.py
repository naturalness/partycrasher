#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2017 Joshua Charles Campbell

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

from copy import deepcopy

from six import text_type, string_types
from six import PY2, PY3
if PY3:
    from collections.abc import Mapping
elif PY2:
    from collections import Mapping

from partycrasher.threshold import Threshold
from partycrasher.api.report_threshold import ReportThreshold

class Thresholds(Mapping):
    """
    Represents the thresholds available under a certain search.
    """
    def __init__(self, search):
        self.search = search
        # Lazy-load projects
        self._d = self.get_thresholds()
    
    def get_thresholds(self):
        thresholds = {
            t: ReportThreshold(self.search, t) for t in self.search.thresholds
            }
        return thresholds
    
    def __getitem__(self, key):
        return self._d.__getitem__(key)
    
    def __iter__(self):
        return self._d.__iter__()

    def __len__(self):
        return self._d.__len__()
    
    def restify(self):
        d = {}
        for k, v in self._d.items():
            d[str(k)] = v
        return d
