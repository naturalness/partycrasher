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

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from partycrasher.bucket import Buckets, Bucket, TopMatch
from partycrasher.threshold import Threshold
from partycrasher.pc_exceptions import MissingBucketError
from partycrasher.es_bucket import ESBuckets

class MoreLikeThisHit(object):
    def __init__(self, raw_hit):
        self.raw_hit = raw_hit
        self.score = raw_hit['_score']
        assert isinstance(self.score, (float, int))
        if '_source' in raw_hit:
            self.database_id = raw_hit['_source']['database_id']
            self.project = raw_hit['_source']['project']
    
    @property
    def prec_top_match(self):
        return self.buckets.top_match

    @property
    def buckets(self):
        # TODO: cache this?
        crash = self.raw_hit['_source']
        try:
            buckets = crash['buckets']
        except KeyError:
            # We couldn't find the bucket field. ASSUME that this means that
            # its bucket assignment has not yet propegated to whatever shard
            # returned the results.
            message = ('Bucket field {!r} not found in crash: '
                      '{!r}'.format('buckets', crash))
            raise MissingBucketError(message)
        buckets = ESBuckets(buckets)
        return buckets

    @property
    def explanation(self):
        try:
          return self.raw_hit['_explanation']['details']
        except:
          error(json.dumps(body, indent=2, cls=ESCrashEncoder))
          error(json.dumps(response, indent=2))
          raise

    @property
    def explanation_summary(self):
        explanation = self.explanation
        with open('explained', 'wb') as debug_file:
            print(json.dumps(self.raw_hit['_explanation'], indent=2), file=debug_file)
        def flatten(explanation):
          flattened = []
          for subexplanation in explanation:
            if subexplanation["description"].startswith("weight"):
              flattened.append(subexplanation)
            else:
              #print(subexplanation["description"])
              if "details" in subexplanation:
                flattened.extend(flatten(subexplanation["details"]))
          return flattened
            
        explanation = flatten(explanation)
        explanation = sorted(explanation, key=itemgetter('value'), reverse=True)
        #with open("explanation", 'w') as f:
          #print(json.dumps(explanation, indent=2), file=f)
          
        summary = []
        for i in explanation:
          #print(i['description'])
          match = re.match(r'^weight\(([^\s:]+):([^\s]+) in .*$', i['description'])
          if match is not None:
            summary.append({'field': match.group(1), 'term': match.group(2), 'value': i['value']})
        #del summary[30:]
        #print(json.dumps(summary, indent=2, cls=ESCrashEncoder), file=sys.stderr)
        
        return summary
      
    def as_top_match(self):
        return TopMatch(report_id=self.database_id,
                        score=self.score,
                        project=self.project)

class MoreLikeThisResponse(object):
    # JSON structure:
    # matches['hit']['hits] ~> [
    #   {
    #       "_score": 8.9,
    #       "_source": {
    #           "buckets": {
    #               "1.0": "***bucket-id-1***",
    #               "9.0": "***bucket-id-2***"
    #           }
    #       }
    #   }

    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.raw_hits = self.response_dict['hits']['hits']
        self.hits = [MoreLikeThisHit(h) for h in self.raw_hits]
        if len(self.hits) > 0:
            self.top_match = self.hits[0]
        else:
            self.top_match = None

    def matching_buckets(self, thresholds):
        matching_buckets = Buckets()
        if len(self.hits) > 0:
            similarity = self.top_match.score
            thresholds = sorted(thresholds)
            
            for threshold in thresholds:
                if similarity >= float(threshold):
                    bucket = self.top_match.buckets[threshold]
                    matching_buckets[threshold] = bucket
                else:
                    matching_buckets[threshold] = None
            matching_buckets['top_match'] = self.top_match.as_top_match()
        else:
            for threshold in thresholds:
                matching_buckets[threshold] = None
            matching_buckets['top_match'] = None
        return matching_buckets
            
            