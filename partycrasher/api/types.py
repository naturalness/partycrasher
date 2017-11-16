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

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

from six import text_type, string_types

from six import PY2, PY3
if PY3:
    from collections.abc import Mapping
elif PY2:
    from collections import Mapping
    
import weakref

from partycrasher.api.search import Search
from partycrasher.api.report_type import ReportType

cached_types = weakref.WeakKeyDictionary()

def get_cached_types(search):
    global cached_types
    if search in cached_types:
        DEBUG("HIT")
        return cached_types[search]
    else:
        DEBUG("MISS " + repr(search._d))
        r = search(size=0)
        types = {
            t: ReportType(search=search, report_type=t) 
            for t in r['counts']['type'].keys()
            }
        cached_types[search] = types
        return types

class Types(Mapping):
    """
    Represents the types available under a certain search.
    """
    def __init__(self, search):
        self.search = search
        # Lazy-load types
        self._d = get_cached_types(search)
    
    def __getitem__(self, key):
        return self._d.__getitem__(key)
    
    def __iter__(self):
        return self._d.__iter__()

    def __len__(self):
        return self._d.__len__()
    
    def restify(self):
        return self._d
