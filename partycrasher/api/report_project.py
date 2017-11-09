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

from partycrasher.project import Project
from partycrasher.api.report_threshold import BucketSearch
from partycrasher.api.search import Search
from partycrasher.api.cache import cached_threshold

class ReportProject(Project):
    """
    API object representing a particular project inside a search context.
    """
    def __init__(self, search, **kwargs):
        super(ReportProject, self).__init__(**kwargs)
        self.original_search = search
        search=Search(search=search, project=self)
        self.reports = search
        self.buckets = cached_threshold(search)
    
    def restify(self):
        d = dict()
        d['reports'] = self.reports
        d['name'] = self.name
        d['buckets'] = self.buckets
        #from partycrasher.api.types import Types
        #d['types'] = Types(copy(elf.reports))
        return d
