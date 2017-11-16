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

import weakref
from six import text_type, string_types

from six import PY2, PY3
if PY3:
    from collections.abc import Mapping
elif PY2:
    from collections import Mapping

from partycrasher.api.search import Search
from partycrasher.api.report_project import ReportProject

cached_projects = weakref.WeakKeyDictionary()
#cached_projects = {}

def get_cached_projects(search):
    global cached_projects
    if search in cached_projects:
        #DEBUG("HIT")
        return cached_projects[search]
    else:
        #DEBUG("MISS " + repr(search._d))
        r = search(size=0)
        projects = {
            p: ReportProject(search=search, project=p) 
            for p in r['counts']['project'].keys()
            }
        cached_projects[search] = projects
        return projects

class Projects(Mapping):
    """
    Represents the projects available under a certain search.
    """
    def __init__(self, search):
        self.search = search
        # Load projects
        self._d = get_cached_projects(search)
    
    def __getitem__(self, key):
        return self._d.__getitem__(key)
    
    def __iter__(self):
        return self._d.__iter__()

    def __len__(self):
        return self._d.__len__()

    def restify(self):
        return self._d
