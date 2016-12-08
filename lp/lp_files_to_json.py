#!/usr/bin/env python

#  Copyright (C) 2015, 2016 Joshua Charles Campbell

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

import os, sys, pprint, random
import crash
import json
import re
import csv
import datetime
import operator
from tokenizers import PatternTokenizer, camel
Crash = crash.Crash

topdir = sys.argv[1]

buckets = []

bugs_total = 0
no_stacktrace = 0

crashes = dict()
oracle = dict()

idsfile = open('ids_okay', 'wb')
idsbucketsfile = open('ids_okay_buckets', 'wb')

packages = dict()

def rec_package(crash):
    package = None
    if 'SourcePackage' in crash:
        package = crash['SourcePackage']
    elif 'Package' in crash:
        package = crash['Package']
    else:
        return
    if package not in packages:
        packages[package] = []
    packages[package].append(crash['database_id'])

def save_packages():
    with open('packages.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Package', 'Count'])
        packages_sorted = sorted(packages.items(), key=lambda x: len(x[1]))
        for package in packages_sorted:
            writer.writerow([
                package[0],
                len(package[1])
            ])

def save_packages():
    with open('packages.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Package', 'Count'])
        packages_sorted = sorted(packages.items(), key=lambda x: len(x[1]))
        for package in packages_sorted:
            writer.writerow([
                package[0],
                len(package[1])
            ])

buckets_dist = dict()

def rec_bucket(crash, bucket):
    if bucket not in buckets_dist:
        buckets_dist[bucket] = []
    buckets_dist[bucket].append(crash['database_id'])

def save_buckets_dist():
    with open('buckets_dist.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Bucket', 'Count'])
        buckets_sorted = sorted(buckets_dist.items(), key=lambda x: len(x[1]))
        for bucket in buckets_sorted:
            writer.writerow([
                bucket[0],
                len(bucket[1])
            ])
            
date_ranges = dict()

def rec_date_info(crash, bucket):
    if bucket not in date_ranges:
        date_ranges[bucket] = {
            'min': datetime.datetime.min,
            'max': datetime.datetime.max
            }
    date_range = date_ranges[bucket]
    if crash['date'] > date_range['min']:
        date_range['min'] = crash['date']
    if crash['date'] < date_range['max']:
        date_range['max'] = crash['date']

def save_date_ranges():
    with open('date_ranges.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Bucket', 'Count', 'Delta', 'First', 'Last'])
        for date_range in date_ranges.values():
            try:
                delta = date_range['min'] - date_range['max']
                date_range['delta'] = delta.total_seconds()
            except:
                print(date_range, file=sys.stderr)
                raise
        date_ranges_sorted = sorted(date_ranges.items(),
            key = lambda x: x[1]['delta'])
        for date_range in date_ranges_sorted:
            writer.writerow([
                date_range[0],
                len(buckets_dist[date_range[0]]),
                date_range[1]['delta'],
                date_range[1]['min'],
                date_range[1]['max']
                ])

architectures = dict()

def rec_architecture(crash):
    architecture = None
    if 'Architecture' in crash:
        architecture = crash['Architecture']
    elif 'cpu' in crash:
        architecture = crash['cpu']
    else:
        return
    if architecture not in architectures:
        architectures[architecture] = []
    architectures[architecture].append(crash['database_id'])

def save_architectures():
    with open('architectures.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Architecture', 'Count'])
        architectures_sorted = sorted(architectures.items(), key=lambda x: len(x[1]))
        for architecture in architectures_sorted:
            writer.writerow([
                architecture[0],
                len(architecture[1])
            ])
    
signals = dict()

def rec_signal(crash):
    signal = None
    if 'Signal' in crash:
        signal = crash['Signal']
    else:
        return
    if signal not in signals:
        signals[signal] = []
    signals[signal].append(crash['database_id'])

def save_signals():
    with open('signals.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Signal', 'Count'])
        signals_sorted = sorted(signals.items(), key=lambda x: len(x[1]))
        for signal in signals_sorted:
            writer.writerow([
                signal[0],
                len(signal[1])
            ])

lengths = dict()
ulengths = dict()

def iterate_all_fields(c, prefix, method):
    if isinstance(c, dict):
        for k, v in c.iteritems():
            subfields = iterate_all_fields(v, prefix + k + ".", method)
    elif isinstance(c, list):
        for i in c:
            subfields = iterate_all_fields(i, prefix, method)
    elif isinstance(c, basestring) or c is None:
        if prefix[-1] == '.':
            prefix = prefix[:-1]
        method(prefix, c)
    elif isinstance(c, datetime.datetime):
        pass
    else:
        raise NotImplementedError("can't handle " + c.__class__.__name__)
    return

def rec_lengths(crash):
    def rec_length(key, value):
        if key not in lengths:
            lengths[key] = []
        if value is None:
            length = 0
        else:
            length = len(camel.__call__(value))
        lengths[key].append((crash['database_id'], length))
        if value is not None:
            #print(key + " " + value + " " + str(length), file=sys.stderr)
            if key not in ulengths:
                ulengths[key] = dict()
            ulengths[key][value] = length

    iterate_all_fields(crash, "", rec_length)
    
def save_lengths():
    length_counts = []
    with open('lengths.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Crash', 'Field', 'Length'])
        for field, v in lengths.items():
            for i in v:
                dbid = i[0]
                length = i[1]
                if field == 'stacktrace.function':
                    writer.writerow([
                        dbid, field, length
                    ])
                if len(length_counts) - 1 < length:
                    for l in range(len(length_counts) - 1, length + 2):
                        length_counts.append(0)
                length_counts[length] += 1
    with open('length_counts.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Length', 'Count'])
        for i in range(0, len(length_counts)):
            writer.writerow([i, length_counts[i]])
    with open('unique_lengths.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Length'])
        for k, v in ulengths['stacktrace.function'].items():
            writer.writerow([v])

libs = dict()

def rec_libs(crash):
    if len(crash['stacktrace']) >= 1:
        frame = crash['stacktrace'][0]
        if 'dylib' in frame:
            dylib = frame['dylib']
            print(dylib, file=sys.stderr)
            match = re.search(r".+/([^/.]+)\.", dylib)
            if match is not None:
              dylib = match.group(1)
              print(dylib, file=sys.stderr)
              if dylib not in libs:
                  libs[dylib] = 0
              libs[dylib] += 1
            
def save_libs():
    with open('top_libs.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Lib', 'Count'])
        for k, v in sorted(libs.items(), key=operator.itemgetter(1), reverse=True):
            writer.writerow([k, v])


for bucketdir in os.listdir(topdir):
    bucket = bucketdir
    bucketdir = os.path.join(topdir, bucketdir)
    assert os.path.isdir(bucketdir)
    buglist = os.listdir(bucketdir)
    #if len(buglist) < 2:
        #continue
    buckets.append(bucket)
    print(bucket, file=sys.stderr)
    for bugdir in buglist:
        bugdir = os.path.join(bucketdir, bugdir)
        print(bugdir, file=sys.stderr)
        assert os.path.isdir(bugdir)
        #print repr(os.listdir(bugdir))
        if len(os.listdir(bugdir)) >= 1:
            database_id = 'launchpad:'+os.path.basename(bugdir)
            try:
                print("Disk: " + database_id, file=sys.stderr)
                crashdata = crash.Crash.load_from_file(bugdir)
            except IOError as e:
                if "No stacktrace" in str(e):
                    no_stacktrace += 1
                    continue
                else:
                    raise
            crashes[database_id] = crashdata
            oracledata = crash.Crash({
                'database_id': database_id,
                'bucket': bucket,
                })
            oracle[database_id] = oracledata
            bugs_total += 1
            match = re.match(r'[^:]+:(\d+)$', database_id)
            sql_id = match.group(1)
            print(str(sql_id), file=idsfile)
            if len(buglist) >= 2:
                print(str(sql_id), file=idsbucketsfile)
            rec_package(crashdata)
            rec_bucket(crashdata, bucket)
            rec_date_info(crashdata, bucket)
            rec_architecture(crashdata)
            rec_signal(crashdata)
            rec_lengths(crashdata)
            rec_libs(crashdata)
print(str(bugs_total) + " loaded", file=sys.stderr)
print(str(no_stacktrace) + " thrown out because of unparsable stacktraces", file=sys.stderr)
print(json.dumps({'crashes': crashes, 'oracle': oracle}, cls=crash.CrashEncoder, indent=2))

idsbucketsfile.close()
idsfile.close()
save_packages()
save_buckets_dist()
save_date_ranges()
save_architectures()
save_signals()
save_lengths()
save_libs()