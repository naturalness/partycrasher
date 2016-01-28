#!/usr/bin/env python

#  Copyright (C) 2015, 2016 Jshua Charles Campbell

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

import os, sys, pprint, random, time, operator, math, csv
import crash
from topN import TopN, TopNLoose, TopNAddress, TopNFile, TopNModule
from es_crash import ESCrash
from elasticsearch import Elasticsearch
import elasticsearch.helpers
from bucketer import MLT, MLTStandardUnicode, MLTLetters, MLTIdentifier, MLTCamelCase, MLTLerch, MLTNGram

es = ESCrash.es

mode = sys.argv[1]
assert mode in ['purity', 'accuracy']

beta = 1.0

comparisons = {
    'ids': {'bucketer': MLTIdentifier, 'kwargs': {'thresh':4.0, 'lowercase':False, 'only_stack':True}},
    'idls': {'bucketer': MLTIdentifier, 'kwargs': {'thresh':4.0, 'lowercase':True, 'only_stack':True}},
    #'ngram5l': {'bucketer': MLTNGram, 'kwargs': {'thresh':4.0, 'lowercase':True, 'n':5}},
    # done vvvv
    #'ngram3l': {'bucketer': MLTNGram, 'kwargs': {'thresh':4.0, 'lowercase':True, 'n':3}},
    #'spc': {'bucketer': MLT, 'kwargs': {'thresh':4.0, 'lowercase':False}},
    #'spcl': {'bucketer': MLT, 'kwargs': {'thresh':4.0, 'lowercase':True}},
    #'uni': {'bucketer': MLTStandardUnicode, 'kwargs': {'thresh':4.0, 'lowercase':False}},
    #'unil': {'bucketer': MLTStandardUnicode, 'kwargs': {'thresh':4.0, 'lowercase':True}},
    #'let': {'bucketer': MLTLetters, 'kwargs': {'thresh':4.0, 'lowercase':False}},
    #'letl': {'bucketer': MLTLetters, 'kwargs': {'thresh':4.0, 'lowercase':True}},
    #'id': {'bucketer': MLTIdentifier, 'kwargs': {'thresh':4.0, 'lowercase':False}},
    #'idl': {'bucketer': MLTIdentifier, 'kwargs': {'thresh':4.0, 'lowercase':True}},
    #'cc': {'bucketer': MLTCamelCase, 'kwargs': {'thresh':4.0, 'lowercase':False}},
    #'ccl': {'bucketer': MLTCamelCase, 'kwargs': {'thresh':4.0, 'lowercase':True}},
    #'lerch0.25': {'bucketer': MLTLerch, 'kwargs': {'thresh':0.25, 'only_stack':True}},
    #'lerch0.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':0.0, 'only_stack':True}},
    #'lerch0.5': {'bucketer': MLTLerch, 'kwargs': {'thresh':0.5, 'only_stack':True}},
    #'lerch1.5': {'bucketer': MLTLerch, 'kwargs': {'thresh':1.5, 'only_stack':True}},
    #'lerch1.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':1.0, 'only_stack':True}},
    #'lerch2.25': {'bucketer': MLTLerch, 'kwargs': {'thresh':2.25, 'only_stack':True}},
    #'lerch3.25': {'bucketer': MLTLerch, 'kwargs': {'thresh':3.25, 'only_stack':True}},
    #'lerch3.5': {'bucketer': MLTLerch, 'kwargs': {'thresh':3.5, 'only_stack':True}},
    #'lerch3.75': {'bucketer': MLTLerch, 'kwargs': {'thresh':3.75, 'only_stack':True}},
    #'lerch4.5': {'bucketer': MLTLerch, 'kwargs': {'thresh':4.5, 'only_stack':True}},
    #'lerch5.5': {'bucketer': MLTLerch, 'kwargs': {'thresh':5.5, 'only_stack':True}},
    #'lerch7.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':7.0, 'only_stack':True}},
    #'lerch2.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':2.0, 'only_stack':True}},
    #'lerch2.5': {'bucketer': MLTLerch, 'kwargs': {'thresh':2.5, 'only_stack':True}},
    #'lerch2.75': {'bucketer': MLTLerch, 'kwargs': {'thresh':2.75, 'only_stack':True}},
    #'lerch3.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':3.0, 'only_stack':True}},
    #'lerch4.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':4.0, 'only_stack':True}},
    #'lerchc': {'bucketer': MLTLerch, 'kwargs': {'thresh':4.0, 'only_stack':False}},
    #'lerch5.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':5.0, 'only_stack':True}},
    #'lerch6.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':6.0, 'only_stack':True}},
    #'lerch8.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':8.0, 'only_stack':True}},
    #'lerch10.0': {'bucketer': MLTLerch, 'kwargs': {'thresh':10.0, 'only_stack':True}},
    #'top1': {'comparer': TopN, 'kwargs': {'n':1}}, 
    #'top2': {'comparer': TopN, 'kwargs': {'n':2}},
    #'top3': {'comparer': TopN, 'kwargs': {'n':3}},
    #'lerchC': {'bucketer': Lerch, 'kwargs': {'thresh':4.0, 'only_stack':False}},
    #'top1a': {'comparer': TopNAddress, 'kwargs': {'n':1}},
    #'top1f' : {'comparer': TopNFile, 'kwargs': {'n':1}},
    #'top1m' : {'comparer': TopNModule, 'kwargs': {'n':1}},
    # trash pile vvvvv
    #'top1l': {'comparer': TopNLoose, 'kwargs': {'n':1}},
}

max_buckets = 1

for comparison in comparisons:
    comparison_data = comparisons[comparison]
    comparison_data['csvfileh'] = open(comparison + '.csv', 'wb')
    comparison_data['csvfile'] = csv.writer(comparison_data['csvfileh'])
    comparison_data['csvfile'].writerow([
        'n',
        'b3p',
        'b3r',
        'b3f',
        'purity',
        'invpur',
        'purf',
        'buckets',
        'obuckets',
        ])
    if 'comparer' in comparison_data:
        kwargs = comparison_data['kwargs']
        comparison_data['comparer'] = (
            comparison_data['comparer'](
                es=es,
                name=comparison,
                index=comparison,
                max_buckets=max_buckets,
                **kwargs)
            )
        comparison_data['bucketer'] = comparison_data['comparer']
    elif 'bucketer' in comparison_data:
        kwargs = comparison_data['kwargs']
        comparison_data['bucketer'] = (
            comparison_data['bucketer'](
                es=es,
                index=comparison,
                name=comparison,
                max_buckets=max_buckets,
                **kwargs)
            )

oracle_all = elasticsearch.helpers.scan(es,
    index='oracle',
    query={
        '_source': ['database_id', 'bucket']
    })
    
all_ids = {}
all_buckets = {}
seen_buckets = {'new':True}

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
print_after = 1000
increasing_spacing = False

def argmax(d):
    mv = None
    mk = None
    for k, v in d.iteritems():
        if mv is None or v > m:
            mv = v
            mk = k
    return (mk, mv)

# reset simulation index for each comparison type
# for time-travel prevention
print "Resetting indices..."
for comparison in sorted(comparisons.keys()):
    print "Deleting index %s" % comparison
    es.indices.delete(index=comparison, ignore=[400, 404])
    comparisons[comparison]['bucketer'].create_index()
es.cluster.health(wait_for_status='yellow')
print "Running simulations..."

interval = print_after

for database_id in sorted(all_ids.keys()):
    oracledata = ESCrash(database_id, index='oracle')
    crashdata = ESCrash(database_id)
    if len(crashdata['stacktrace']) < 1:
        continue
    #print database_id
    do_print = False
    if ((crashes_so_far >= print_after)
        or (crashes_so_far >= (len(all_ids)-2))):
        if increasing_spacing:
            print_after = (int(math.sqrt(print_after)) + int(math.sqrt(interval))) ** 2
        else:
            print_after += interval
        do_print = True
        print "in %i/%i crashes and %i/%i bugkets:" % (crashes_so_far, len(all_ids), len(seen_buckets), len(all_buckets))
        if mode == 'purity':
            print "\tb3_P\tb3_R\tb3_F\tpurity\tinvpur\tpurF\tbuckets"
    for comparison in sorted(comparisons.keys()):
        comparison_data = comparisons[comparison]
        if mode == 'accuracy':
            if not ('tp' in comparison_data):
                comparison_data['tp'] = 0
            if not ('fp' in comparison_data):
                comparison_data['fp'] = 0
            if not ('tn' in comparison_data):
                comparison_data['tn'] = 0
            if not ('fn' in comparison_data):
                comparison_data['fn'] = 0
        elif mode == 'purity':
            if not ('oracle_to_assigned' in comparison_data):
                comparison_data['oracle_to_assigned'] = {}
                comparison_data['assigned_to_oracle'] = {}
                comparison_data['oracle_totals'] = {}
                comparison_data['assigned_totals'] = {}
                comparison_data['bcubed'] = {}
        oracle_to_assigned = comparison_data['oracle_to_assigned']
        assigned_to_oracle = comparison_data['assigned_to_oracle']
        oracle_totals = comparison_data['oracle_totals']
        assigned_totals = comparison_data['assigned_totals']
        bcubed = comparison_data['bcubed']
        if 'comparer' in comparison_data:
            bucketer = comparison_data['comparer']
            comparer = comparison_data['comparer']
        else:
            bucketer = comparison_data['bucketer']
            comparer = None
        if mode == 'accuracy':
            simulation_buckets = bucketer.alt_bucket(crashdata, bucket_field='bucket')
            for bucket in seen_buckets:
                if bucket == 'new':
                    if len(simulation_buckets) == 0:
                        if not (oracledata['bucket'] in seen_buckets):
                            comparison_data['tp'] += 1
                        else:
                            comparison_data['fp'] += 1
                    else:
                        if not (oracledata['bucket'] in seen_buckets):
                            comparison_data['fn'] += 1
                        else:
                            comparison_data['tn'] += 1
                else:
                    if bucket in simulation_buckets:
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
            if do_print:
                try:
                    precision = comparison_data['tp']/(comparison_data['tp']+comparison_data['fp'])
                    recall = comparison_data['tp']/(comparison_data['tp']+comparison_data['fn'])
                    specificity = comparison_data['tn']/(comparison_data['fp']+comparison_data['tn'])
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
            # add to the simulation data set now that we've seen it
            if comparer is not None:
                simulationdata = comparer.save_signature(crashdata)
            else:
                if len(simulation_buckets) > 0:
                    assign = simulation_buckets[0]
                else:
                    assign = 'bucket:' + crashdata['database_id'] # Make a new bucket
                simulationdata = bucketer.assign_save_bucket(crashdata, bucket=assign)
            simulationdata['bucket'] = oracledata['bucket']
        elif mode == 'purity':
            simulationdata = bucketer.assign_save_bucket(crashdata)
            simbucket = simulationdata[comparison]
            obucket = oracledata['bucket']
            bcubed[database_id] = (simbucket, obucket)
            #print simbucket + " // " + obucket
            if not (obucket in oracle_to_assigned):
                oracle_to_assigned[obucket] = {}
                oracle_totals[obucket] = 0
            if not (simbucket in oracle_to_assigned[obucket]):
                oracle_to_assigned[obucket][simbucket] = 0
            oracle_to_assigned[obucket][simbucket] += 1
            oracle_totals[obucket] += 1
            if not (simbucket in assigned_to_oracle):
                assigned_to_oracle[simbucket] = {}
                assigned_totals[simbucket] = 0
            if not (obucket in assigned_to_oracle[simbucket]):
                assigned_to_oracle[simbucket][obucket] = 0
            assigned_to_oracle[simbucket][obucket] += 1
            assigned_totals[simbucket] += 1
            if do_print:
                purity = 0.0
                N = crashes_so_far + 1
                for clustername, cluster in assigned_to_oracle.iteritems():
                    C = assigned_totals[clustername]
                    intersection = max(cluster.values())
                    purity += (C/N) * (intersection/C)
                ipurity = 0.0
                F = 0.0
                for categoryname, category in oracle_to_assigned.iteritems():
                    L = oracle_totals[categoryname]
                    intersection = max(category.values())
                    ipurity += (L/N) * (intersection/L)
                    Fmax = 0.0
                    for clustername, cluster in category.iteritems():
                        C = assigned_totals[clustername]
                        intersection = cluster
                        precision = intersection/C
                        recall = intersection/L
                        fscore = (1.0+(beta**2.0))*((precision*recall)/((beta**2.0)*precision+recall))                    
                        if fscore > Fmax:
                            Fmax = fscore
                    F += (L/N) * Fmax
                #print "%s:\t\tpurity\t%0.3f,\tinvpur\t%0.3f,\tf-score\t%0.3f" \
                    #% (comparison,
                    #purity,
                    #ipurity,
                    #F,
                    #)
                precision = 0.0
                recall = 0.0
                for e in bcubed.values():
                    c = 0
                    pn = 0
                    rn = 0
                    for ep in bcubed.values():
                        #correct = (e[0] == ep[0]) == (e[1] == ep[1])
                        if (e[0] == ep[0]) and (e[1] == ep[1]):
                            c += 1
                        if (e[0] == ep[0]):
                            pn += 1
                        if (e[1] == ep[1]):
                            rn += 1
                    precision += (c/pn)
                    recall += (c/rn)
                precision = precision/N
                recall = recall/N
                fscore = (1.0+(beta**2.0))*((precision*recall)/((beta**2.0)*precision+recall))                    
                print "%s:\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f" \
                    % (comparison,
                    precision,
                    recall,
                    fscore,
                    purity,
                    ipurity,
                    F,
                    len(assigned_totals)/len(oracle_totals)
                    )
                comparison_data['csvfile'].writerow([
                    N,
                    precision,
                    recall,
                    fscore,
                    purity,
                    ipurity,
                    F,
                    len(assigned_totals),
                    len(oracle_totals),
                    ])
                comparison_data['csvfileh'].flush()
        es.indices.refresh(index=comparison)
        #es.indices.flush(index=comparison)
    crashes_so_far += 1
    bucket = oracledata['bucket']
    # prevent ourselves from seeing the future!
    if not bucket in seen_buckets:
        seen_buckets[bucket] = [database_id]
    else:
        seen_buckets[bucket].append(database_id)
    def get_active():
        nodes = es.nodes.stats()['nodes']
        node = nodes[nodes.keys()[0]]
        things = 0
        for k, v in node['thread_pool'].iteritems():
            things += v['active'] + v['queue']
        #print things
        return things
    #while get_active() > 1:
        #time.sleep(0.1)
    last_seen_buckets = seen_buckets

