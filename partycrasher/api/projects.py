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

from six import text_type, string_types

from six import PY2, PY3
if PY3:
    from collections.abc import Mapping
elif PY2:
    from collections import Mapping

from partycrasher.api.search import Results
from partycrasher.api.report_project import ReportProject

class Projects(Mapping):
    """
    Represents the projects available under a certain search.
    """
    def __init__(self, search):
        self.search = search
        # Lazy-load projects
        self._d = None
    
    def get_projects(self):
        """Get project tree."""
        r = Results(self.search, size=0)
        projects = {p:
            ReportProject(self.search, p) 
            for p in r.counts['project'].keys()}
        return projects
    
    def load(self):
        if self._d is None:
            self._d = self.get_projects()
        return self._d
        
    def __getitem__(self, key):
        self.load()
        return self._d.__getitem__(key)
    
    def __iter__(self):
        self.load()
        return self._d.__iter__()

    def __len__(self):
        self.load()
        return self._d.__len__()
    
    def restify(self):
        self.load()
        d = {}
        for k, v in self._d.items():
            d[str(k)] = {
                'reports': v.reports.search,
                'buckets': v.buckets.search
            }
        return d
