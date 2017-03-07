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

from __future__ import print_function, division

import json
import operator
from multiprocessing import Pool

from partycrasher.crash import Crash, pretty
from partycrasher.rest_client import RestClient
from partycrasher.threshold import Threshold

def compute_average_dissimilarity_vs_bucket(crash, bucket,  similaritys):
    total_dis = 0.0
    n = 0
    for other in bucket:
        if other != crash:
            #dissimilarty = 1/(1+similaritys[crash][other])
            dissimilarty = similaritys[crash][other]
            total_dis += dissimilarty
            n += 1
    return total_dis/n
    

def compute_silhouette(crashes, buckets, similaritys):
    tot_s_i = 0.0
    n_s_i = 0
    for bucket_id in buckets:
        bucket = buckets[bucket_id]
        if len(bucket) < 2:
            continue
        for crash in bucket:
            a_i = compute_average_dissimilarity_vs_bucket(crash, bucket,  similaritys)
            b_i = 1.0
            for other_bucket_id in buckets:
                other_bucket = buckets[other_bucket_id]
                if crash not in other_bucket:
                    maybe_b_i = compute_average_dissimilarity_vs_bucket(crash, other_bucket,  similaritys)
                    if maybe_b_i < b_i:
                        b_i = maybe_b_i
            s_i = (b_i - a_i) / max((b_i, a_i))
            #print("crash %s a_i %f b_i %f s_i %f" % (crash, a_i, b_i, s_i))
            tot_s_i += s_i
            n_s_i += 1
    avg_s_i = tot_s_i/n_s_i
    print("avg silhouette: %f" % (avg_s_i))
            
                        
                    
        

def compute_metrics_threshold(crashes, threshold, similaritys):
    print("Threshold: " + str(threshold))
    # Make a bucket map
    buckets = {}
    # Make a crash map
    crashes_by_id = {}
    for crash in crashes:
        id_ = crash['database_id']
        bucket = crash['buckets'][threshold.to_elasticsearch()]['id']
        #print(id_ + " " + bucket)
        crashes_by_id[id_] = crash
        if bucket not in buckets:
            buckets[bucket] = set()
        assert not id_ in buckets[bucket]
        buckets[bucket].add(id_)
    if len(buckets) < 2:
        print("Not enough buckets!")
        return
    compute_silhouette(crashes, buckets, similaritys)
      
def get_similarity(args):
    id_, others, client = args
    results = client.compare(id_, others)
    assert len(results) == len(others)
    print("%f %f" % (max(results), min(results)))
    ids = [id_] * len(others)
    return zip(ids, others, results)
    
        
def get_similaritys(crashes, client):
    similaritys = {}
    tocompute = []
    for ci in range(0, len(crashes)):
        others = []
        for cj in range(0, len(crashes)):
            others.append(crashes[cj]['database_id'])
        tocompute.append(
            (crashes[ci]['database_id'], 
              others,
              client)
            )
    p = Pool(8)
    results = reduce(operator.add, p.map(get_similarity, tocompute))
    for crash, other, similarity in results:
        if crash not in similaritys:
            similaritys[crash] = {}
        similaritys[crash][other] = similarity
        #if crash == other:
            #print("%s self: %f" % (crash, similarity))
    # ES computes asymmetric similaritys so lets average them
    for ci in similaritys:
        for cj in similaritys[ci]:
            ij = similaritys[ci][cj]
            ji = similaritys[cj][ci]
            if (ij != ji):
                avg = (ij + ji)/2
                similaritys[ci][cj] = avg
                similaritys[cj][ci] = avg
    return similaritys
        

def compute_metrics(date_range_start, rest_service_url):
    client = RestClient(rest_service_url)
    crashes = client.get_a_bunch_of_crashes(date_range_start, 500)
    similaritys = get_similaritys(crashes, client)
    #print(pretty(similaritys))
    #print(pretty(crashes))
    for i in sorted(crashes[0]['buckets']):
        try:
            i = Threshold(i)
        except:
            continue
        compute_metrics_threshold(crashes, i, similaritys)
          
compute_metrics("2000", "http://localhost:5000/")


