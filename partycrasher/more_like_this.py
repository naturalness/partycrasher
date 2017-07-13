#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2016 Joshua Charles Campbell

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

from __future__ import print_function, division

from partycrasher.crash_filter import CrashFilter
from partycrasher.more_like_this_response import MoreLikeThisResponse
from partycrasher.es.crash import elastify
from partycrasher.crash import Crash

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

class MoreLikeThisQuery(object):
    def __init__(self,
                 index,
                 max_query_terms=20,
                 terminate_after=None,
                 filterer=None,
                 min_score=None):
        self.max_query_terms = max_query_terms
        self.terminate_after = terminate_after
        assert min_score is not None
        self.min_score = min_score
        self.index = index
        if filterer is None:
            self.filterer = CrashFilter()
        else:
            self.filterer = filterer
    
    def make_mlt(self, 
                 crash,
                 filterer,
                 all_terms=False):
        doc = filterer.filter_crash(crash)
        mlt = { 
                'like': [
                        {
                            '_index': self.index.name,
                            '_type': 'crash',
                            'doc': doc,
                        }
                    ],
                    # Avoid some ElasticSearch optimizations:
                    #
                    # Search for WAY more terms than ElasticSearch would
                    # normally construct.
                    # Force ElasticSearch to query... like, all the things.
                    'min_term_freq': 0,
                    'min_doc_freq': 0,
              }
        if self.max_query_terms is not None:
            mlt['max_query_terms'] = self.max_query_terms
        if all_terms is True:
            mlt['max_query_terms'] = 10000
        return mlt

    def make_query(self,
                   crash,
                   filterer,
                   all_terms=False):
        query = {
            'more_like_this': self.make_mlt(crash, filterer, all_terms)
          }
        return query

    def make_body(self,
                  crash,
                  explain):
        body = {
            # Only fetch database ID, buckets, and project.
            '_source': ['buckets', 'database_id', 'project'],
            'query': self.make_query(crash, self.filterer),
            'size': 1,
        }
        if self.min_score > 0:
            body['min_score'] = self.min_score
        if self.terminate_after is not None:
            body['terminate_after'] = self.terminate_after
        if explain:
            body['explain'] = True
        return body

class MoreLikeThisFiltered(MoreLikeThisQuery):
    def __init__(self,
                 search_filters = [],
                  **kwargs):
        self.search_filters = search_filters
        super(MoreLikeThisFiltered,self).__init__(**kwargs)
    
    def make_id_filter(self,
                       ids):
          return {
              'ids': {
                  'values': ids
                }
            }

    def make_query(self,
                   crash,
                   filterer,
                   ids=None,
                   all_terms=False):
        query = {
            'bool': {
                'should': (super(MoreLikeThisFiltered,self)
                    .make_query(crash, filterer=filterer, all_terms=all_terms))
              }
          }
        filters = self.search_filters
        if ids is not None:
            filters.appnd(self.make_id_filter(self.ids))
        if len(filters) > 0:
            query['bool']['filters'] = filters
        return query
    
    def make_body(self,
                  crash,
                  explain=False,
                  ids=None):
        body = {
            # Only fetch database ID, buckets, and project.
            '_source': ['buckets', 'database_id', 'project'],
            'query': self.make_query(crash, self.filterer, ids),
            'size': 1,
        }
        if self.min_score > 0:
            body['min_score'] = self.min_score
        if self.terminate_after is not None:
            body['terminate_after'] = self.terminate_after
        if explain:
            body['explain'] = True
        return body
        
    
class MoreLikeThisRescored(object):
    def __init__(self,
                 query=None,
                 rescore_filterer=None,
                 rescore_window_size=500,
                 search_weight=1.0,
                 rescore_weight=1.0,
                  **kwargs):
        if query is None:
            self.query = MoreLikeThisFiltered( **kwargs)
        else:
            self.query = query
        self.rescore_filterer = rescore_filterer
        self.window_size = rescore_window_size
        self.search_weight = search_weight
        self.rescore_weight = rescore_weight

    def make_body(self,
                  crash,
                  explain=False,
                  ids=None):
        assert self.rescore_filterer is not None
        body = self.query.make_body(crash, explain, ids)
        body["rescore"] = {
            "window_size": self.window_size,
            "query": {
                "rescore_query": self.query.make_query(crash,
                                                       self.rescore_filterer,
                                                       ids,
                                                       all_terms=True),
                "query_weight": self.search_weight,
                "rescore_query_weight": self.rescore_weight
              }
          }
        return body


class MoreLikeThisSearcher(object):
    
    def __init__(self, index, **kwargs):
        self.index = index
        if 'rescore_filterer' in kwargs:
            self.querybuilder = MoreLikeThisRescored(index=index, **kwargs)
        else:
            self.querybuilder = MoreLikeThisFiltered(index=index, **kwargs)
        return self
    
    def query(self,
              crash,
              explain):
        body = self.querybuilder.make_body(crash, explain, None)
        #assert 'terminate_after' in body
        response = self.index.search(body=elastify(body))
        return MoreLikeThisResponse(response)

       
    def summary(self,
                crash):
        assert isinstance(crash, Crash)
        body = self.querybuilder.make_body(crash, True, None)
        response = self.index.search(body=elastify(body))
        # TODO: sum all summaries
        hits = MoreLikeThisResponse(response).hits
        if len(hits) > 0:
            return MoreLikeThisResponse(response).hits[0].explanation_summary
        else:
            return []
    
    def compare(self,
                crash,
                other_ids):
        body = self.querybuilder.make_body(crash, False, other_ids)
        response = self.index.search(body=elastify(body))
        return MoreLikeThisResponse(response)
    
class MoreLikeThis(MoreLikeThisSearcher):
    """ Class to setup MLT search config. """
    def __init__(self, index, config):
        always_remove_fields = [r'^database_id',
                         r'^buckets',
                         r'force_bucket',
                         r'stacktrace\.depth',
                         r'^date',
                         r'logdf']
        filterer = CrashFilter(config.remove_fields+always_remove_fields,
                               config.keep_fields)
        rescore_filterer = CrashFilter(config.rescore_remove_fields+always_remove_fields,
                               config.rescore_keep_fields)
        super(MoreLikeThis,self).__init__(
            index=index,
            max_query_terms=config.max_query_terms,
            terminate_after=config.terminate_after,
            min_score=config.min_score,
            filterer=filterer,
            rescore_filterer=rescore_filterer,
            rescore_window_size=config.rescore_window_size,
            rescore_weight=config.rescore_weight,
            search_weight=config.search_weight
            )
