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
from partycrasher.crash import Crash, Stacktrace, Stackframe
from partycrasher.project import Project
from partycrasher.crash_type import CrashType
from partycrasher import launchpad_crash
import json
import re
import csv
import datetime
import operator
from tokenizers import PatternTokenizer, camel

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug
logging.basicConfig(level=logging.DEBUG)

topdir = sys.argv[1]

buckets = []

bugs_total = 0
no_stacktrace = 0

crashes = dict()
oracle = dict()

idsfile = open('ids_okay', 'w')
idsbucketsfile = open('ids_okay_buckets', 'w')

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
                ERROR(date_range)
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
    def call_method(k, v):
        if k[-1] == '.':
            k = k[:-1]
        method(k, v)

    if isinstance(c, dict):
        for k, v in c.iteritems():
            subfields = iterate_all_fields(v, prefix + k + ".", method)
    if isinstance(c, Crash) or isinstance(c, Stackframe):
        for k, v in c._d.items():
            subfields = iterate_all_fields(v, prefix + k + ".", method)
    elif isinstance(c, list):
        for i in c:
            subfields = iterate_all_fields(i, prefix, method)
    elif isinstance(c, Stacktrace):
        for i in c._l:
            subfields = iterate_all_fields(i, prefix, method)
    elif isinstance(c, Project) or isinstance(c, CrashType):
        call_method(prefix, c.name)
    elif isinstance(c, str) or c is None:
        call_method(prefix, c)
    elif isinstance(c, int):
        call_method(prefix, str(c))
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
            #DEBUG(dylib)
            match = re.search(r".+/([^/.]+)\.", dylib)
            if match is not None:
              dylib = match.group(1)
              #DEBUG(dylib)
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
    INFO(bucket)
    for bugdir in buglist:
        bugdir = os.path.join(bucketdir, bugdir)
        INFO(bugdir)
        assert os.path.isdir(bugdir)
        #print repr(os.listdir(bugdir))
        if len(os.listdir(bugdir)) >= 1:
            database_id = 'launchpad:'+os.path.basename(bugdir)
            try:
                INFO("Disk: " + database_id)
                crashdata = Crash.load_from_file(bugdir)
            except IOError as e:
                if "No stacktrace" in str(e):
                    no_stacktrace += 1
                    continue
                else:
                    raise
            crashes[database_id] = crashdata
            oracledata = Crash({
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
INFO(str(bugs_total) + " loaded")
INFO(str(no_stacktrace) + " thrown out because of unparsable stacktraces")
print(json.dumps({'crashes': crashes, 'oracle': oracle}, cls=CrashEncoder, indent=2))

idsbucketsfile.close()
idsfile.close()
save_packages()
save_buckets_dist()
save_date_ranges()
save_architectures()
save_signals()
save_lengths()
save_libs()
