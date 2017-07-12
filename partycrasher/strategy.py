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

from partycrasher.more_like_this import MoreLikeThis
from partycrasher.bucket import Buckets

class Strategy(object):
    def __init__(self, config, index):
        self.config = config
        self.index = index
    
    def query(self, crash, explain):
        return self.searcher.query(crash, explain)
    
    def matching_buckets(self, *args, **kwargs):
        raise NotImplementedError() 

class MLT(Strategy):
    def __init__(self, *args, **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.searcher = MoreLikeThis(config=self.config, index=self.index)
        self.max_top_match_score = 0
        self.total_top_match_scores = 0
        self.total_matches = 0
    
    def matching_buckets(self, thresholds, search_result):
        matching_buckets = Buckets()
        if len(search_result.hits) > 0:
            similarity = search_result.top_match.score
            thresholds = sorted(thresholds)
            
            for threshold in thresholds:
                if similarity >= float(threshold):
                    bucket = search_result.top_match.buckets[threshold]
                    matching_buckets[threshold] = bucket
                else:
                    matching_buckets[threshold] = None
            matching_buckets['top_match'] = search_result.top_match.as_top_match()
        else:
            for threshold in thresholds:
                matching_buckets[threshold] = None
            matching_buckets['top_match'] = None
        return matching_buckets
