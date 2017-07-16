##!/usr/bin/env pythoFprettyn

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

from __future__ import division, print_function

import os, sys, pprint, random, time, operator, math, csv

# XXX: import things from within the partycrasher package.
REPOSITORY_ROUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(REPOSITORY_ROUTE, 'partycrasher'))

from partycrasher import crash
import json
import requests
from partycrasher.rest.client import RestClient
import copy
import signal
import subprocess
import traceback
import datetime

import logging
from logging import error, warn, info, debug
logging.getLogger().setLevel(logging.DEBUG)

import fake_data_generator


# TODO: argparse
DONT_ACTUALLY_COMPUTE_STATS=False
BLOCK_SIZE=1000
PARALLEL=8
BOOTSTRAP_CRASHES=1000000 # WARNING: Destroys temporal relationships!
BOOTSTRAP_RESUME_AT=0 # This doesn't actually work properly yet, don't use it.
RESET_STATS_AFTER_BLOCK=True
TOTALLY_FAKE_DATA=False
INJECT_FAKE_FIELDS=True
START_GUNICORN=True
interval = BLOCK_SIZE
increasing_spacing = False

beta = 1.0

def get_comparisons(client):
    comparisons = {
    }

    response = requests.get(client.root_url)
    thresholds = response.json()['buckets'].keys()
    #except:
        #raise
        #print response.status_code
        #print response.text
        #raise

    for threshold in thresholds:
        name = "T" + threshold
        comparisons[name] = {'threshold': threshold}

    for comparison in comparisons:
        comparison_data = comparisons[comparison]
        if BOOTSTRAP_RESUME_AT == 0:
            comparison_data['csvfileh'] = open(comparison + '.csv', 'w')
            comparison_data['csvfile'] = csv.writer(comparison_data['csvfileh'])
            comparison_data['csvfile'].writerow([
                'after',
                'n',
                'b3p',
                'b3r',
                'b3f',
                'purity',
                'invpur',
                'purf',
                'buckets',
                'obuckets',
                'time',
                ])
        else:
            comparison_data['csvfileh'] = open(comparison + '.csv', 'ab')
            comparison_data['csvfile'] = csv.writer(comparison_data['csvfileh'])
    return comparisons

def load_oracle_data(oracle_file_path):
    with open(oracle_file_path, mode='r') as oracle_file:
        oracle_file_data = json.load(oracle_file)

    all_crashes = oracle_file_data['crashes']
    oracle_all = oracle_file_data['oracle']
    all_ids = {}
    all_buckets = {}

    del oracle_file_data
    
    print(str(len(all_crashes)) + " crashes found in oracle")

    crashes = {}
    skipped_ids = set()

    for database_id, crash in all_crashes.items():
        assert crash['database_id'] == database_id
        if len(crash['stacktrace']) < 1:
            print("Skipping: " + database_id)
            skipped_ids.add(database_id)
            continue
        crashes[database_id] = crash
            
            
    for k, v in oracle_all.items():
        assert k == v['database_id']
        database_id = v['database_id']
        if database_id in skipped_ids:
            continue
        bucket = v['bucket']
        all_ids[database_id] = bucket
        if not bucket in all_buckets:
            all_buckets[bucket] = [database_id]
        else:
            all_buckets[bucket].append(database_id)

    print(str(len(all_ids)) + " IDs used in oracle")

    
    if not BOOTSTRAP_CRASHES > 0:
        total_ids = len(all_ids)
        total_buckets = len(all_buckets)
    else:
        total_ids = BOOTSTRAP_CRASHES
        total_buckets = len(all_buckets)
    
    return (crashes, oracle_all, all_ids, total_ids, total_buckets)

def argmax(d):
    mv = None
    mk = None
    for k, v in d.items():
        if mv is None or v > m:
            mv = v
            mk = k
    return (mk, mv)

def reset_index(client):
    # reset simulation index for each comparison type
    # for time-travel prevention
    response = None
    try:
        response = requests.delete(client.path_to('reports'))
        assert response.status_code == 200
        del response
    except:
        if response is not None:
            print(response.status_code)
            print(response.text)
        raise


def ingest_one(mblock):
    client, data = mblock
    if PARALLEL > 1:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    crashdata = data['crashdata']
    for k, v in crashdata.items():
        if '.' in k:
            k.replace('.', '_')
    assert 'buckets' not in crashdata
    retries = 3
    while retries > 0:
        response = None
        try:
            #print("p", file=sys.stderr)
            response = requests.post(client.path_to('reports'), json=crashdata)
            assert (response.status_code == 201 or response.status_code == 303), response.status_code
        except Exception as e:
            retries -= 1
            #debug(response.content)
            traceback.print_exc()
            print("POST failed...", file=sys.stderr)
            sys.stderr.flush()
            time.sleep(1)
            if retries < 1:
                raise
        else:
            break # don't retry if it worked
    try:
        simulationdata = response.json()['report']
    except ValueError as e:
        print(response.content)
        traceback.print_exc()
        raise
    assert 'buckets' in simulationdata
    data['simulationdata'] = simulationdata
    return data

# this must go after definition of functions which will be called in pool
if PARALLEL > 0:
    import multiprocessing
    pool = multiprocessing.Pool(PARALLEL)

def process_block(client, block, crashes_so_far, comparisons, totals):
    global pool
    print("Processing %i crashes (%i to %i)..." % (len(block), 
                                          crashes_so_far - len(block) + 1,
                                          crashes_so_far))
    # ingest
    start = time.time()

    mblock = [(client, data) for data in block]
    if PARALLEL > 0:
        r = pool.map_async(ingest_one, mblock, 1)
        #try:
        block_results = r.get(999999) # set a large but finite timeout for old version of python as a work around for http://bugs.python.org/issue8296
        #except KeyboardInterrupt:
            #print 'Caught SIGINT, exiting...'
            #pool.terminate()
            #pool.join()
            #if START_GUNICORN:
                #stop_gunicorn()
            #sys.exit(130)
        pool.close()
        pool.join()
        pool = multiprocessing.Pool(PARALLEL)
    else:
        block_results = map(ingest_one, mblock)
    finish = time.time()
    ingest_time = finish-start
    print("%i crashes in %fs: %0.1fcrashes/s" % (
      len(block),
      ingest_time,
      len(block)/(ingest_time)))
    # accumulate counts
    for block_result in block_results:
        # unpack
        oracledata = block_result['oracledata']
        crashdata = block_result['crashdata']
        simulationdata = block_result['simulationdata']
        database_id = block_result['database_id']
        
        # total up counts for each threshold
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
            
        bucket = oracledata['bucket']
        # prevent ourselves from seeing the future!
        seen_buckets = totals['seen_buckets']
        if not bucket in seen_buckets:
            seen_buckets[bucket] = [database_id]
        else:
            seen_buckets[bucket].append(database_id)
        totals['seen_crashes'].append(database_id)

    if not DONT_ACTUALLY_COMPUTE_STATS:
        total_ids = totals['total_ids']
        total_buckets = totals['total_buckets']
        seen_buckets = totals['seen_buckets']
        seen_crashes = totals['seen_crashes']
        N = len(seen_crashes)
        print("in %i, after %i/%i crashes and %i/%i bugkets:" % (N, 
                                                       crashes_so_far,
                                                       total_ids, 
                                                       len(seen_buckets), 
                                                       total_buckets))
        print("\tb3_P\tb3_R\tb3_F\tpurity\tinvpur\tpurF\tbuckets")
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
            purity = 0.0
            for clustername, cluster in assigned_to_oracle.items():
                C = assigned_totals[clustername]
                intersection = max(cluster.values())
                purity += (C/N) * (intersection/C)
            ipurity = 0.0
            F = 0.0
            for categoryname, category in oracle_to_assigned.items():
                L = oracle_totals[categoryname]
                intersection = max(category.values())
                ipurity += (L/N) * (intersection/L)
                Fmax = 0.0
                for clustername, cluster in category.items():
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
            print("%s:\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f" \
                % (comparison,
                precision,
                recall,
                fscore,
                purity,
                ipurity,
                F,
                len(assigned_totals)/len(oracle_totals)
                ))
            comparison_data['csvfile'].writerow([
                crashes_so_far,
                N,
                precision,
                recall,
                fscore,
                purity,
                ipurity,
                F,
                len(assigned_totals),
                len(oracle_totals),
                ingest_time,
                ])
            comparison_data['csvfileh'].flush()
        


def iterate_crash(
    client,
    database_id, 
    oracledata, 
    crashdata, 
    comparisons,
    totals,
):
    iterate_crash.ingest_block.append({
            'database_id': database_id,
            'oracledata': oracledata,
            'crashdata': crashdata
        })
    iterate_crash.crashes_so_far += 1
    if ((iterate_crash.crashes_so_far >= iterate_crash.print_after)
        or (iterate_crash.crashes_so_far >= (totals['total_ids']-2))):
        if increasing_spacing:
            iterate_crash.print_after = (
                  (
                      int(math.sqrt(iterate_crash.print_after)) 
                      + int(math.sqrt(interval))
                  )
              ** 2)
        else:
            iterate_crash.print_after += interval
        if RESET_STATS_AFTER_BLOCK:
            comparisons_block = {
                  k: copy.copy(v) for k, v in comparisons.items()
                  }
            for v in comparisons_block.values():
                assert 'oracle_to_assigned' not in v
            totals['seen_buckets'] = {}
            totals['seen_crashes'] = []
        else:
            comparisons_block = comparisons
        process_block(client,
                      iterate_crash.ingest_block, 
                      iterate_crash.crashes_so_far,
                      comparisons_block,
                      totals)
        iterate_crash.ingest_block = []

class FakeFieldInjector(object):
    def __init__(self):
        self.metadata_vocab_alpha = 1000
        self.metadata_total_words = 100
        self.metadata_total_fields = 50
        self.metadata_field_word_alpha = 100
        self.metadata_vocab = fake_data_generator.ChineseRestaurant(
            self.metadata_vocab_alpha,
            fake_data_generator.Strings('', 0))
        self.metadata_fields = fake_data_generator.FakeMetadataFields(
            self.metadata_vocab,
            self.metadata_total_words,
            self.metadata_total_fields,
            self.metadata_field_word_alpha)
    def inject(self, crashref):
        for i in range(0, self.metadata_total_fields):
            field = self.metadata_fields.get_field(i)
            crashref[field.name] = " ".join(field.draw())
        #debug(crash.pretty(crashref))

        

def simulate(client, comparisons, oracle_data):
    (crashes, oracle_all, all_ids, total_ids, total_buckets) = oracle_data
    totals = {
        'total_ids': total_ids,
        'total_buckets': total_buckets,
        'seen_buckets': {},
        'seen_crashes': []
        }
    if not BOOTSTRAP_CRASHES > 0:
        for database_id in sorted(all_ids.keys()):
            oracledata = oracle_all[database_id]
            crashdata = crashes[database_id]
            #print json.dumps(crashdata, indent=2)
            iterate_crash(
              database_id,
              oracledata,
              crashdata,
              comparisons,
              totals,
              )
    else:
        import random
        fake_field_injector = None
        if INJECT_FAKE_FIELDS:
            fake_field_injector = FakeFieldInjector()
        for fake_i in range(BOOTSTRAP_RESUME_AT, BOOTSTRAP_CRASHES):
            database_id = "fake:%010i" % fake_i
            source_database_id = list(all_ids.keys())[
              random.randrange(0, len(all_ids.keys()))]
            oracledata = copy.copy(oracle_all[source_database_id])
            oracledata['database_id'] = database_id
            crashdata = copy.copy(crashes[source_database_id])
            crashdata['database_id'] = database_id
            crashdata['date'] = datetime.datetime.fromtimestamp(
                946684800 + fake_i).isoformat()
            if INJECT_FAKE_FIELDS:
                fake_field_injector.inject(crashdata)
            iterate_crash(
                          client,
                          database_id,
                          oracledata,
                          crashdata,
                          comparisons,
                          totals,
                          )

class GunicornStarter(object):
    def __init__(self):
        self.start_gunicorn()
    
    def start_gunicorn(self):
        info("Starting gunicorn...")
        if PARALLEL > 0:
            self.gunicorn = subprocess.Popen(['gunicorn',
                '--access-logfile', 'gunicorn-access.log',
                '--error-logfile',  'gunicorn-error.log',
                '--log-level', 'debug',
                '--workers', str(PARALLEL),
                '--worker-class', 'sync',
                '--bind', 'localhost:5000',
                '--timeout', '60',
                '--pid', 'gunicorn.pid',
                '--capture-output',
                'partycrasher.rest.validator',
                ],
                preexec_fn=os.setsid)
            print('gunicorn started on %i' % (self.gunicorn.pid))
            time.sleep(5)
        else:
            self.gunicorn = subprocess.Popen(['python',
                'partycrasher/rest_service.py',
                '--port=5000',
                '--debug',
                '--allow-delete-all',
                ],
                preexec_fn=os.setsid)
            time.sleep(5)
            print('flask started on %i' % (self.gunicorn.pid))
        
    def stop_gunicorn(self):
        if self.gunicorn.poll() is None:
            os.killpg(os.getpgid(self.gunicorn.pid), signal.SIGTERM)
        self.gunicorn.wait()
     
    def close(self):
        self.stop_gunicorn()
        
def buckettest(oracle_file_path, rest_service_url):
    client = RestClient(rest_service_url)

    # static variables
    iterate_crash.print_after = BLOCK_SIZE 
    iterate_crash.crashes_so_far = 0
    iterate_crash.ingest_block = []
    

    if START_GUNICORN:
        gunicorn_starter = GunicornStarter()

    try:
        if not BOOTSTRAP_RESUME_AT:
            reset_index(client)
        if TOTALLY_FAKE_DATA:
            synthesize(get_comparisons())
        else:
            simulate(
                client,
                get_comparisons(client),
                load_oracle_data(oracle_file_path)
            )
    except:
        traceback.print_exc()
    finally:
        print('Cleaing up...')
        if PARALLEL > 1:
            pool.terminate()
            pool.join()
        if START_GUNICORN:
            gunicorn_starter.stop_gunicorn()

    

if __name__ == '__main__':
    if len(sys.argv) < 2+1:
        print("Usage: " + sys.argv[0] + "oracle.json http://restservicehost:port/")

    oracle_file_path = sys.argv[1]
    rest_service_url = sys.argv[2]

    buckettest(oracle_file_path, rest_service_url)
