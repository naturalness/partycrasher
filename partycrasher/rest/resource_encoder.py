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

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

from datetime import datetime
from collections import OrderedDict
import traceback
import sys

from decimal import Decimal

from partycrasher.pc_encoder import PCEncoder
from partycrasher.project import Project
from partycrasher.threshold import Threshold
from partycrasher.bucket import Bucket, TopMatch
from partycrasher.rest.api_utils import full_url_for, merge
from partycrasher.api.report import Report
from partycrasher.api.search import Search
from partycrasher.api.thresholds import Thresholds
from partycrasher.api.report_bucket import ReportBucketSearch
from partycrasher.api.report_threshold import BucketSearch

from flask import json, request, redirect, make_response

def search_url_append(path, params, key, conv=str):
    if key in params:
        if isinstance(params[key], (list, tuple)):
            path += key + 's/' + ','.join([conv(p) for p in params[key]]) + '/'
        else:
            path += key + 's/' + conv(params[key]) + '/'
        del params[key]
    return path

def url_for_search(search, direct_search=True):
    endpoint = 'view'
    path = '/'
    params = {}
    for k, v in search.items():
        assert k is not None
        if v is not None:
            params[k] = v
    #if 'from' in search._d:
        #assert 'from' in params, search['from']
    path = search_url_append(path, params, 'type')
    path = search_url_append(path, params, 'project')
    path = search_url_append(path, params, 'threshold')
    merge(params, 'bucket', 'bucket_id')
    path = search_url_append(path, params, 'bucket')
    #DEBUG("search " + search.__class__.__name__)
    if isinstance(search, BucketSearch):
        path += 'buckets/'
    elif isinstance(search, Search):
        #if direct_search:
        path += 'reports/'
    else:
        raise RuntimeError("what")
    path = path.rstrip('/') # it's already in the route 
    params['path'] = path
    url = full_url_for(endpoint, **params)
    if 'from' in search and search['from'] is not None:
        assert 'from' in url
    return url

def url_for_report(report):
    urlp = url_for_search(report.came_from).split('?', 1)
    url = urlp[0]
    assert url.endswith('reports/')
    url += report.database_id
    return url
    
def url_for_report_id(report_id):
    return full_url_for('view',
        path = 'reports/'+ report_id
        )

def auto_url_for(thing):
    if isinstance(thing, Search):
        return url_for_search(thing)
    elif isinstance(thing, Report):
        return url_for_report(thing)
    else:
        raise TypeError("Can't get url for %s" % str(type(thing)))
    
def json_traceback(tb):
    tb = traceback.extract_tb(tb)
    out_tb = []
    i = 0
    for frame in reversed(tb):
        i = i + 1
        out_tb.append({
            'file': frame[0],
            'fileline': frame[1],
            'function': frame[2],
            'extra': frame[3],
            'depth': i
            })
    return out_tb

traceback_class = None

try:
    raise RuntimeError("Fake error!")
except RuntimeError as ex:
    (t, v, tb) = sys.exc_info()
    traceback_class = tb.__class__
    del t
    del v
    del tb
    del ex

class ResourceEncoder(PCEncoder):
    def default(self, o):
        if isinstance(o, Search):
            return url_for_search(o)
        elif isinstance(o, Report):
            d = o.restify_()
            d['href'] = url_for_report(o)
            return d
        elif hasattr(o, 'restify'):
            return o.restify()
        elif isinstance(o, TopMatch):
            d = super(ResourceEncoder, self).default(o).copy()
            d['href'] = url_for_report_id(o['report_id'])
            return d
        elif isinstance(o, traceback_class):
            return json_traceback(o)
        #elif isinstance(o, Decimal):
            #return "WHATTTTTT!!!!"
        else:
            return super(ResourceEncoder, self).default(o)

