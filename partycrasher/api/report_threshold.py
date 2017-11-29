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
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from copy import copy

from partycrasher.threshold import Threshold
from partycrasher.bucket import Bucket
from partycrasher.api.search import Page, Search
from partycrasher.api.report_bucket import ReportBucket
from partycrasher.pc_encoder import pretty

class BucketPage(Page):
    """Class representing a page of buckets from search results."""
    def __init__(self,
                 buckets,
                 **kwargs):
        super(BucketPage, self).__init__(buckets=buckets, **kwargs)
        assert self['threshold'] is not None
        
    @property
    def results(self):
        return self.buckets
    
    @property
    def total(self):
        return self.total_buckets


class BucketSearch(Search):
    """Class representing the buckets available under a certain search."""
    def __init__(self, **kwargs):
        super(BucketSearch, self).__init__(**kwargs)
        assert self['threshold'] is not None
    
    def page(self, 
             from_=None, 
             size=None
             ):
        """
        Given a datetime lower_bound (from date), calculates the top buckets
        in the given timeframe for the given threshold (automatically
        determined if not given). The results can be tailed for a specific
        project if needed.

        Returns a list of {'doc_count': int, 'key': id} dictionaries.
        """
        query = self.build_query(size=0)
        
        must = query["query"]["bool"]["must"]

        # Oh, ElasticSearch! You and your verbose query "syntax"!
        query["aggs"]["top_buckets_filtered"] = {
            # Filter the top buckets by date, and maybe by project.
            "filter": {
                "bool": { "must": must }
            },
            # Get the top buckets in descending order of size.
            "aggs": {
                "top_buckets": {
                    "terms": {
                        "field": "buckets." 
                            + self['threshold'].to_elasticsearch(),
                        "order": { "_count": "desc" },
                    },
                    # Get the date of the latest crash per bucket.
                    "aggs": {
                        "first_seen": {
                            "min": {
                                "field": "date"
                                }
                            },
                        "last_seen": {
                            "max": {
                                "field": "date"
                                }
                            }
                        }
                    }
                }
            }
        
        if size is None:
          size = 10
          
        (query["aggs"]["top_buckets_filtered"]["aggs"]
                  ["top_buckets"]["terms"]["size"]) = 1000
        
        #actual_size = size
        
        #if from_ is not None:
            #assert from_ >= 0
            #actual_size = actual_size + from_
        #if size is not None:
            #assert size >= 0
            #(query["aggs"]["top_buckets_filtered"]["aggs"]
                  #["top_buckets"]["terms"]["size"]) = actual_size
        
        #debug(pretty(query))
        response = self.context.search(body=query)
        #debug(pretty(response))

        # Oh, ElasticSearch! You and your verbose responses!
        top_buckets = (response['aggregations']
                       ['top_buckets_filtered']
                       ['top_buckets']
                       ['buckets'])
        total = len(top_buckets)
        
        if from_ is not None:
            top_buckets = top_buckets[from_:]
        else:
            from_ = 0
        if size is not None:
            top_buckets = top_buckets[0:size]
        else:
            size = total
        
        first_page = self.new_first_page()
        
        buckets = [ReportBucket(
                        search=first_page, 
                        id=bucket['key'], 
                        project=self['project'],
                        type=self['type'],
                        threshold=self['threshold'],
                        total=bucket['doc_count'],
                        first_seen=bucket['first_seen']['value_as_string'],
                        last_seen=bucket['last_seen']['value_as_string'],
                        )
                   for bucket in top_buckets]
        
        assert self['threshold'] is not None
        r = BucketPage(
                       buckets=buckets,
                       total=total,
                       search=self,
                       from_=from_,
                       size=size
                       )
        return r
    
class ReportThreshold(Threshold):
    def __init__(self, search, result, from_=None, size=None):
        super(ReportThreshold, self).__init__(result)
        search = BucketSearch(search=search, threshold=Threshold(self))
        self.buckets = BucketSearch(
            search=search,
            from_=from_,
            size=size
            )
    
    def restify(self):
        return self.buckets
