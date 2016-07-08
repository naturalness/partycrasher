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

# XXX: import things from within the partycrasher package.
REPOSITORY_ROUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(REPOSITORY_ROUTE, 'partycrasher'))

import crash
import json
import requests
from rest_client import RestClient

DONT_ACTUALLY_COMPUTE_PERF=True

if len(sys.argv) < 2+1:
    print "Usage: " + sys.argv[0] + "oracle.json http://restservicehost:port/"

oracle_file_path = sys.argv[1]
rest_service_url = sys.argv[2]

client = RestClient(rest_service_url)

beta = 1.0

comparisons = {
}

response = requests.get(client.root_url)
thresholds = response.json()['config']['thresholds']
#except:
    #raise
    #print response.status_code
    #print response.text
    #raise

for threshold in thresholds:
    name = "T" + threshold
    comparisons[name] = {'threshold': threshold}

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

with open(oracle_file_path, mode='r') as oracle_file:
    oracle_file_data = json.load(oracle_file)

crashes = oracle_file_data['crashes']
oracle_all = oracle_file_data['oracle']
all_ids = {}
all_buckets = {}
seen_buckets = {'new':True}

del oracle_file_data

for k, v in oracle_all.iteritems():
    database_id = v['database_id']
    bucket = v['bucket']
    all_ids[database_id] = bucket
    if not bucket in all_buckets:
        all_buckets[bucket] = [database_id]
    else:
        all_buckets[bucket].append(database_id)

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
#print "Resetting indices..."
#for comparison in sorted(comparisons.keys()):
    #print "Deleting index %s" % comparison
    #es.indices.delete(index=comparison, ignore=[400, 404])
    #comparisons[comparison]['bucketer'].create_index()
#es.cluster.health(wait_for_status='yellow')
#print "Running simulations..."
try:
    response = requests.delete(client.path_to('reports'))
    assert response.status_code == 200
    del response
except:
    print response.status_code
    print response.text
    raise

interval = print_after

for database_id in sorted(all_ids.keys()):
    oracledata = oracle_all[database_id]
    crashdata = crashes[database_id]
    #print json.dumps(crashdata, indent=2)
    if len(crashdata['stacktrace']) < 1:
        print "Skipping: " + database_id
        continue
    do_print = False
    if ((crashes_so_far >= print_after)
        or (crashes_so_far >= (len(all_ids)-2))):
        if increasing_spacing:
            print_after = (int(math.sqrt(print_after)) + int(math.sqrt(interval))) ** 2
        else:
            print_after += interval
        do_print = True
        print "in %i/%i crashes and %i/%i bugkets:" % (crashes_so_far, len(all_ids), len(seen_buckets), len(all_buckets))
        print "\tb3_P\tb3_R\tb3_F\tpurity\tinvpur\tpurF\tbuckets"
    response = requests.post(client.path_to('reports'), json=crashdata)
    simulationdata = response.json()
    for comparison in sorted(comparisons.keys()):
        comparison_data = comparisons[comparison]
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
        #print json.dumps(response.json(), indent=2)
        #sys.exit(1)
        #simulationdata = bucketer.assign_save_buckets(crash.Crash(crashdata))
        simbuckets = simulationdata['buckets']
        #print repr(simbuckets)
        #for k in simbuckets.keys():
            #print k.__hash__()
        #print repr(comparison_data['threshold'].__hash__())
        simbucket = simbuckets[str(comparison_data['threshold'])]['id']
        #print repr(simbucket)
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
        if do_print and not DONT_ACTUALLY_COMPUTE_PERF:
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
        #es.indices.refresh(index=comparison)
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

