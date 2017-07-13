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

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from datetime import datetime

from partycrasher.pc_dict import PCDict
from partycrasher.project import Project
from partycrasher.threshold import Threshold

class CommonSearch(object):
    def __init__(self,
                 index=None,
                 config=None,
                 threshold=None,
                 project=None,
                 since=None,
                 until=None,
                 query_string=None,
                 bucket_id=None):
        self.index = index
        self.config = config
        self.threshold = Threshold(threshold)
        self.project = project
        if since is not None:
            assert isinstance(since, datetime)
        self.since = since
        if until is not None:
            assert isinstance(until, datetime)
        self.until = until
        self.query_string = query_string
        self.bucket_id = bucket_id

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
                        threshold.to_elasticsearch(): self.bucket_id
                    }
                })
        
        aggs = {}
        
        for field in self.config.fixed_summary_fields.keys():
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
        
        

    def feedbackize(self, d):
        """
        Takes a dictionary and adds information about how the search
        was performed to it.
        """
        d["threshold"] = self.threshold
        d["project"] = self.project
        d["since"] = self.since
        d["until"] = self.until
        d["query_string"] = self.query_string
        d["search"] = self
        d["bucket_id"] = self.bucket_id
        return d
    
    def run(self, query):
        raw = self.index.search(body=query)
        return raw


    def raw_results_to_page(self, raw, page_class):
        total_hits = raw['hits']['total']
        raw_hits = raw['hits']['hits']
        
        counts = {}
        for field in self.config.fixed_summary_fields.keys():
            converter = lambda x: x
            if field == "project":
                converter = Project
            field_counts = {}
            raw_agg = raw['aggregations'][field]['buckets']
            for b in raw_agg:
                field_counts = (b['key'], b['doc_count'])
            counts[field] = field_counts
        
        reports = []
        for hit in raw_hits:
            report = hit['_source']
            # TODO?: use Report class?
            crash = Crash(report)
            reports.append(crash)
        
        return page_class(reports=reports,
                          total_reports=total_hits,
                          counts=counts)

class CommonPage(PCDict):
    def next_page(self):
        #TODO: implement ES scrolling
        return self.report_buckets.page(
            from_=self.from_+self.size,
            size=self.size,
            )
    
    def restify(self):
        d = {}
        for k, v in self._d.items():
            if k == 'search':
                continue
            d[k] = v
        return d
