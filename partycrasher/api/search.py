#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016, 2017 Joshua Charles Campbell

#  This program is free software; you can reditext_typeibute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) rany later version.
#
#  This program is ditext_typeibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import division

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from six import string_types, text_type
from six import PY2, PY3
if PY3:
    from collections.abc import Sequence
elif PY2:
    from collections import Sequence

from datetime import datetime
from copy import copy

from partycrasher.pc_dict import PCDict, PCDefaultDict
from partycrasher.project import Project
from partycrasher.threshold import Threshold
from partycrasher.crash import Crash
from partycrasher.api.util import (
    maybe_date, 
    maybe_threshold, 
    maybe_project,
    maybe_bucket,
    maybe_text
    )
from partycrasher.bucket import Bucket
from partycrasher.api.report import Report
from partycrasher.context import Context

class Search(PCDefaultDict):
    
    canonical_fields = {
        'threshold': {
            'type': Threshold,
            'converter': maybe_threshold,
            'default': None
            },
        'project': {
            'type': Project,
            'converter': maybe_project,
            'default': None
            },
        'since': {
            'type': datetime,
            'converter': maybe_date,
            'default': None
            },
        'until': {
            'type': datetime,
            'converter': maybe_date,
            'default': None
            },
        'query_string': {
            'type': string_types,
            'converter': maybe_text,
            'default': None
            },
        'bucket_id': {
            'type': string_types,
            'converter': maybe_text,
            'default': None
            },
        }
        
    def __init__(self,
                 context=None,
                 search=None,
                 **kwargs):
        if context is not None:
            assert isinstance(context, Context), context.__class__.__name__
            self.context = context
        else:
            assert search is not None
            self.context = search.context
        if search is None:
            super(Search, self).__init__(**kwargs)
        else:
            super(Search, self).__init__(search)
            self.update(kwargs)
        self.thresholds = self.context.thresholds

    def build_query(self, 
                    from_=None, 
                    size=None):
        # Build up a boolean-must query
        must = []
        
        if ((self.since is not None) 
                or (self.until is not None)):
            date = {}
            if self.since is not None:
                date['gt'] = self.since.isoformat()
            if self.until is not None:
                date['lt'] = self.until.isoformat()
            must.append({
                "range": {
                    "date": date
                    }
                })
        
        # May filter optionally by project name.
        if self.project is not None:
            must.append({
                "term": {
                    "project": self.project
                }
            })
        
        if self.query_string is not None:
            must.append({
                "query_string": {
                    "query": self.query_string,
                    # This is necessary due to how we tokenize things
                    # which is not on whitespace I.E. if the user 
                    # searched for CamelCaseThing it will be interpreted
                    # as a search for Camel AND Case AND Thing rather
                    # than Camel OR Case OR Thing
                    "default_operator": "AND",
                }
            })
        
        if self.bucket_id is not None:
            assert self.threshold is not None
            must.append({
                "term": {
                    "buckets." + 
                        self.threshold.to_elasticsearch(): self.bucket_id
                    }
                })
        
        aggs = {}
        
        for field in self.context.fixed_summary_fields.keys():
            aggs[field] = {
                "terms": {
                    "field": field,
                    "size": 10
                    }
                }
        
        es_query = {
            "query": {
                "bool": { 
                    "must": must
                    }
                },
            "aggs": aggs
            }
        
        if from_ is not None:
            es_query["from"] = from_;
        if size is not None:
            es_query["size"] = size;
        return es_query

    def run(self, query):
        raw = self.context.search(body=query)
        return raw


    def raw_results_to_page(self, raw, page_class):
        total_hits = raw['hits']['total']
        raw_hits = raw['hits']['hits']
        
        counts = {}
        for field in self.context.fixed_summary_fields.keys():
            converter = lambda x: x
            if field == "project":
                converter = Project
            field_counts = {}
            raw_agg = raw['aggregations'][field]['buckets']
            for b in raw_agg:
                field_counts[b['key']] = b['doc_count']
            counts[field] = field_counts
        
        reports = []
        for hit in raw_hits:
            report = hit['_source']
            # TODO?: use Report class?
            crash = Crash(report)
            reports.append(crash)
        
        return page_class(reports=reports,
                          total_reports=total_hits,
                          counts=counts,
                          search=self)
    
    def page(self, from_=None, size=None):
        """Get search results for a particular page."""
        query = self.build_query(from_=from_, size=size)
        raw = self.run(query)
        page = self.raw_results_to_page(raw, Page)
        page['from'] = from_
        page['size'] = len(raw['hits']['hits'])
        return page

    def as_dict(self):
        return self._d
    
class Page(PCDict):
    def __init__(self,
                 reports,
                 **kwargs):
        super(Page, self).__init__(**kwargs)
        self['reports'] = reports
        
    def next_page(self):
        #TODO: implement ES scrolling
        return self.search.page(
            from_=self['from']+self['size'],
            size=self['size'],
            )
    
    def restify(self):
        if 'search' in self:
            d = copy(self['search'].as_dict())
        else:
            d = {}
        d.update(self._d)
        return d
    
    @property
    def results(self):
        return self.reports
    
    @property
    def total(self):
        return self.total_reports

class View(Sequence):
    """Fluent interface"""
    search_class = Search
    item_class = Report
    
    def __init__(self,
                 from_=0, 
                 size=10,
                 **kwargs):
        self.search = self.search_class(**kwargs)
        assert isinstance(self.search, Search)
        self._from = from_
        self._size = size
        self._page = None
        self._length = None
    
    def seek(self, from_, size):
        self._from = from_
        self._size = size
        return self.page
        
    @property
    def page(self):
        assert isinstance(self.search, Search)
        if self._page is None:
            self._page = self.search.page(self._from, self._size)
        if self._length is None:
            self._length = self._page.total
        return self._page
    
    def in_page(self, i):
        return i >= self.page.from_ and (
            i < self.page.from_ + len(self.page.results))
        
    def __getitem__(self, i):
        if self._page is None or not self._pagein_page(i):
            self._page = None
            self._from = i
            self.page()
        return item_class(self.search, 
                          self.page.results[i-self.page._from])
    
    def __len__(self):
        if self._length is None:
            self.page()
        return self._length
        
class Results(object):
    def __init__(self, search, from_=None, size=None):
        self.reports = View(
            search=search,
            from_=from_,
            size=size
            )
    
    def restify(self):
        return self.reports.page
        return d
    
    @property
    def counts(self):
        return self.reports.page.counts
