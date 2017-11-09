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
#from partycrasher.crash import Crash
from partycrasher.api.util import (
    maybe_date, 
    maybe_threshold, 
    maybe_project,
    maybe_bucket,
    maybe_text,
    maybe_type
    )
from partycrasher.bucket import Bucket
from partycrasher.api.report import Report
from partycrasher.context import Context
from partycrasher.crash_type import CrashType
from partycrasher.es.crash import ESCrash

class Search(PCDefaultDict):
    
    canonical_fields = {
        'threshold': {
            'type': Threshold,
            'converter': maybe_threshold,
            'default': None,
            'multi': True
            },
        'project': {
            'type': Project,
            'converter': maybe_project,
            'default': None,
            'multi': True
            },
        'since': {
            'type': datetime,
            'converter': maybe_date,
            'default': None,
            'multi': False
            },
        'until': {
            'type': datetime,
            'converter': maybe_date,
            'default': None,
            'multi': False
            },
        'query_string': {
            'type': string_types,
            'converter': maybe_text,
            'default': None,
            'multi': False
            },
        'bucket_id': {
            'type': string_types,
            'converter': maybe_text,
            'default': None,
            'multi': True
            },
        'type': {
            'type': CrashType,
            'converter': maybe_type,
            'default': None,
            'multi': True
            },
        }
        
    def __init__(self,
                 context=None,
                 search=None,
                 from_=None,
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
        if from_ is not None:
            self['from'] = from_
        self.freeze()
    
    def __copy__(self):
        return self.__class__(search=self)
        
    def build_disjunction(self, field, things):
        if isinstance(things, list):
            return {
                "bool": {
                    "should": [
                        self.build_disjunction(field, thing)
                            for thing in things
                        ],
                    "minimum_should_match": 1
                    }
                }
        else:
            return {
                "term": {
                    field: things
                    }
                }

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
        
        # May filter optionally by type name.
        if self['type'] is not None:
            must.append(self.build_disjunction("type", self['type']))

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
    
    def raw_crash_to_report(self, crash):
        return Report(
                self,
                ESCrash.de_elastify(crash), 
                saved=True)

    def raw_results_to_page(self, raw, page_class, **kwargs):
        total_hits = raw['hits']['total']
        raw_hits = raw['hits']['hits']
        
        counts = {}
        for field in self.context.fixed_summary_fields.keys():
            converter = lambda x: x
            if field == "project":
                converter = Project
            if field == "type":
                converter = CrashType
            field_counts = {}
            raw_agg = raw['aggregations'][field]['buckets']
            for b in raw_agg:
                field_counts[b['key']] = b['doc_count']
            counts[field] = field_counts
        
        reports = []
        for hit in raw_hits:
            crash = hit['_source']
            report = self.raw_crash_to_report(crash)
            reports.append(report)
        
        return page_class(reports=reports,
                          total=total_hits,
                          counts=counts,
                          search=self,
                          **kwargs
                          )
    
    def page(self, from_, size):
        """Get search results for a particular page."""
        if from_ is None:
            from_ = self._d.get('from', None)
        if from_ is None:
            from_ = 0
        if size is None:
            size = self._d.get('size', None)
        query = self.build_query(from_=from_, size=size)
        raw = self.run(query)
        page = self.raw_results_to_page(
            raw, ReportPage, 
            from_=from_, 
            size=len(raw['hits']['hits'])
            )
        return page
    
    def __call__(self, from_=None, size=None):
        return self.page(from_=from_, size=size)

    def as_dict(self):
        return self._d
    
    def new_blank(self):
        return Search(context=self.context)
    
    @property
    def project(self):
        if 'project' in self._d and self._d['project'] is not None:
            from partycrasher.api.report_project import ReportProject
            return ReportProject(project=self._d['project'], 
                                    search=self.new_blank())
        return None
    
    @property
    def type(self):
        if 'type' in self._d and self._d['type'] is not None:
            from partycrasher.api.report_type import ReportType
            return ReportType(report_type=self._d['type'], 
                                    search=self.new_blank())
        return None
    
    def __eq__(self, other):
        return self._d.__eq__(other._d)
    
    def __hash__(self):
        return hash(self.as_hashable())
    
class Page(PCDict):
    def __init__(self,
                 from_,
                 **kwargs):
        kwargs['from'] = from_
        super(Page, self).__init__(**kwargs)
        assert self['search'] is not None
        assert self['from'] is not None
        assert self['size'] is not None
        self['search'] = Search(
            search=self['search'],
            from_=self['from'],
            size=self['size']
            )
        assert self['search']['from'] is not None
        self._d.update(self['search'].as_dict())
        assert self['from'] is not None
        assert self['size'] is not None
        
        if self['from']+self['size']<self['total']:
            next_from = self['from']+self['size']
            self['next_page'] = Search(
                search=self['search'],
                from_=next_from,
                size=self['size']
                )
        else:
            self['next_page'] = None
        
        if self['from'] > 0:
            prev_from = max(
                0,
                self['from']-self['size'])
            self['prev_page'] = Search(
                search=self['search'],
                from_=prev_from,
                size=self['size']
                )
        else:
            self['prev_page'] = None
            
        if self['project'] is not None:
            from partycrasher.api.report_project import ReportProject
            self['project'] = ReportProject(
                search=self['search'].new_blank(),
                project=self['project']
                )
        if self['type'] is not None:
            from partycrasher.api.report_type import ReportType
            self['type'] = ReportType(
                search=self['search'].new_blank(),
                report_type=self['type']
                )
        self.freeze()
            
    def restify(self):
        return self.as_dict()

class ReportPage(Page):
    def __init__(self,
                reports,
                **kwargs):
        super(ReportPage, self).__init__(reports=reports, **kwargs)

    @property
    def results(self):
        return self.reports
    
    @property
    def total(self):
        return self.total_reports

