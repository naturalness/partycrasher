#!/usr/bin/env python

#  Copyright (C) 2015 Jshua Charles Campbell

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

from __future__ import division

import os, sys, pprint, random
import crash
from topN import TopN, TopNLoose, TopNAddress, TopNFile
from es_crash import ESCrash
from elasticsearch import Elasticsearch
import elasticsearch.helpers

comparisons = {
    'top1': {'comparer': TopN(1)}, 
    'top2': {'comparer': TopN(2)},
    'top3': {'comparer': TopN(3)},
    'top3l': {'comparer': TopNLoose(3)},
    'top3a': {'comparer': TopNAddress(3)},
    'top1file' : {'comparer': TopNFile(1)},
}

#TODO: MISSING CODE HERE TO ITERATE OVER EVERYTHING IN ELASTIC
es = Elasticsearch()
oracle_all = elasticsearch.helpers.scan(es,
    index='oracle',
    query={
        '_source': ['database_id', 'bucket']
    })
    
all_ids = {}
all_buckets = {}
seen_buckets = {}

for i in oracle_all:
    database_id = i['_source']['database_id']
    bucket = i['_source']['bucket']
    all_ids[database_id] = bucket
    if not bucket in all_buckets:
        all_buckets[bucket] = [database_id]
    else:
        all_buckets[bucket].append(database_id)
del oracle_all

print str(len(all_ids)) + " IDs found in oracle"
crashes_so_far = 0

for database_id in sorted(all_ids.keys()):
    oracledata = ESCrash(database_id, index='oracle')
    crashdata = ESCrash(database_id)
    if len(crashdata['stacktrace']) < 1:
        continue
    #print database_id
    if (crashes_so_far % 100) == 0:
        print "in %i/%i crashes and %i bugkets:" % (crashes_so_far, len(all_ids), len(all_buckets))
    for comparison in comparisons:
        comparison_data = comparisons[comparison]
        if not ('tp' in comparison_data):
            comparison_data['tp'] = 0
        if not ('fp' in comparison_data):
            comparison_data['fp'] = 0
        if not ('tn' in comparison_data):
            comparison_data['tn'] = 0
        if not ('fn' in comparison_data):
            comparison_data['fn'] = 0
        comparer = comparison_data['comparer']
        this_signature = comparer.get_signature(crashdata)
        oracle_match = es.search(
            index='oracle',
            body={
                'query': {
                    #'match': {
                        #comparison: this_signature
                        #}
                    'filtered':{
                        'query': {
                            'match_all': {}
                            },
                        'filter': {
                            'term': {
                                comparison: this_signature,
                            }
                        }
                    }
                },
                #'min_score': 1.0,
                'aggregations': {
                    'buckets': {
                        'terms': {
                            'field': 'bucket',
                            'size': 10
                        }
                    }
                }
            })
        other_buckets = {}
        #print len(oracle_match['aggregations']['buckets']['buckets'])
        if len(oracle_match['aggregations']['buckets']['buckets']) > 2 and False:
            pprint.PrettyPrinter(indent=4).pprint(oracle_match)
            sys.exit(0)
        for other_result in oracle_match['aggregations']['buckets']['buckets']:
            other_bucket = other_result['key']
            other_buckets[other_bucket] = True
        for bucket in seen_buckets:
            if bucket in other_buckets:
                if bucket == oracledata['bucket']:
                    comparison_data['tp'] += 1
                else:
                    comparison_data['fp'] += 1
            else:
                if bucket == oracledata['bucket']:
                    comparison_data['fn'] += 1
                else:
                    comparison_data['tn'] += 1
        #print "%s: tp %i, fp %i, tn %i, fn %i" \
            #% (comparison,
                #comparison_data['tp'],
                #comparison_data['fp'],
                #comparison_data['tn'],
                #comparison_data['fn'],
                #)
        if (crashes_so_far % 100) == 0:
            try:
                precision = comparison_data['tp']/(comparison_data['tp']+comparison_data['fp'])
                recall = comparison_data['tp']/(comparison_data['tp']+comparison_data['fn'])
                specificity = comparison_data['tn']/(comparison_data['fp']+comparison_data['tn'])
                beta = 1.0
                fscore = (1.0+(beta**2.0))*((precision*recall)/((beta**2.0)*precision+recall))
                print "%s: precision %f, recall %f, specificity %f, f-score %f" \
                    % (comparison,
                    precision,
                    recall,
                    specificity,
                    fscore,
                    )
            except ZeroDivisionError:
                pass
        oracledata[comparison] = this_signature
    crashes_so_far += 1
    bucket = oracledata['bucket']
    # prevent ourselves from seeing the future!
    if not bucket in seen_buckets:
        seen_buckets[bucket] = [database_id]
    else:
        seen_buckets[bucket].append(database_id)
    

