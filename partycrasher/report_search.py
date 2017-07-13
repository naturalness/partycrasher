#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2016, 2017 Joshua Charles Campbell

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

from __future__ import print_function

from six import string_types

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

import datetime

from partycrasher.bucket import Bucket
from partycrasher.threshold import Threshold
from partycrasher.common_search import CommonPage, CommonSearch

class ReportPage(CommonPage):
    """Class representing a page of reports from a bucket or search."""
    pass

class ReportBucket(CommonSearch):
    """Class representing a bucket of reports."""
    def __init__(self, **kwargs):
        assert 'bucket_id' in kwargs
        super(ReportBucket, self).__init__(**kwargs)
        
    def page(from_=None, 
             size=None):
        """
        Returns a page of crashes for the given bucket.
        """
        query = self.build_query(from_=from_, size=size)
        query["sort"] = { "date": { "order": "desc" }}
        
        raw = self.run(query)
        
        with open('bucket_response', 'w') as debug_file:
            print(json.dumps(raw, indent=2), file=debug_file)
        
        reports_found = raw['hits']['total']

        # Since no reports were found, assume the bucket does not exist (at
        # least for this project).
        if reports_found < 1:
            raise BucketNotFoundError(bucket_id)

        return self.raw_results_to_page(raw, ReportPage)

class ReportSearch(CommonSearch):
    def page(from_=None,
             size=None):
        query = self.build_query(from_=from_, size=size)
        raw = self.run(query)
        return self.raw_results_to_page(raw, ReportPage)
