#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016  Eddie Antonio Santos <easantos@ualberta.ca>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from collections import OrderedDict
from partycrasher.crash import Crash, CrashEncoder
from partycrasher.project import Project
from partycrasher.threshold import Threshold
from partycrasher.bucket import Bucket, TopMatch
from partycrasher.rest.api_utils import full_url_for
from partycrasher.api.report import Report
from partycrasher.api.search import Search
from partycrasher.api.thresholds import Thresholds
from partycrasher.api.report_bucket import ReportBucketSearch
from partycrasher.api.report_threshold import BucketSearch

from flask import json, request, redirect, make_response

def url_for_search(search):
    if isinstance(o, BucketSearch):
        endpoint = 'query_buckets'
    elif isinstance(o, Search):
        endpoint = 'search'
    else:
        return search
    params = {}
    for k, v in stuff.items():
        assert k is not None
        if v is not None:
            params[k] = v
    if 'project' not in params:
        endpoint = endpoint + '_no_project'
    return full_url_for(endpoint, **params)
    
def auto_url_for(thing):
    if isinstance(thing, Search):
        return url_for_search(thing)
    elif isinstance(thing, Report) or isinstance(thing, Crash):
        return full_url_for('view_report',
                            project=thing.project,
                            report_id=thing.database_id
                            )
    else:
        return thing

class ResourceEncoder(CrashEncoder):
    def default(self, o):
        if isinstance(o, Search):
            return url_for_search('search', o.as_dict())
        elif hasattr(o, 'restify'):
            return o.restify()
        elif isinstance(o, Threshold):
            return str(o)
        elif isinstance(o, Crash):
            d = super(ResourceEncoder, self).default(o).copy()
            d['href'] = full_url_for('view_report',
                                     project=o.project,
                                     report_id=o.id
                                     )
            return d
        elif isinstance(o, Bucket):
            d = super(ResourceEncoder, self).default(o).copy()
            if 'project' in d and d['project'] is not None:
                d['href'] = full_url_for('view_bucket',
                                     threshold=o.threshold,
                                     bucket_id=o.id,
                                     project=o.project
                                     )
            else:
                d['href'] = full_url_for('view_bucket_no_project',
                                     threshold=o.threshold,
                                     bucket_id=o.id
                                     )
            return d
        elif isinstance(o, Project):
            d = {
              'name': super(ResourceEncoder, self).default(o),
              'href': full_url_for('query_buckets',
                                     threshold='4.0',
                                     project=o.name
                                     )
            }
            return d
        elif isinstance(o, TopMatch):
            d = super(ResourceEncoder, self).default(o).copy()
            d['href'] = full_url_for('view_report',
                                     project=o.project,
                                     report_id=o.report_id
                                     )
            return d
        else:
            return super(ResourceEncoder, self).default(o)

