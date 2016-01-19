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

topdir = sys.argv[1]

buckets = []

from elasticsearch import Elasticsearch
bugs_total = 0

for bucketdir in os.listdir(topdir):
    bucket = bucketdir
    bucketdir = os.path.join(topdir, bucketdir)
    assert os.path.isdir(bucketdir)
    buglist = os.listdir(bucketdir)
    if len(buglist) < 2:
        continue
    buckets.append(bucket)
    for bugdir in buglist:
        bugdir = os.path.join(bucketdir, bugdir)
        assert os.path.isdir(bugdir)
        #print repr(os.listdir(bugdir))
        if len(os.listdir(bugdir)) > 1:
            database_id = 'launchpad:'+os.path.basename(bugdir)
            try:
                crashdata = ESCrash(database_id)
                print "ES: " + database_id
            except:
                crashdata = None
            if crashdata is None:
                try:
                    print "Disk: " + database_id
                    crashdata = crash.Crash.load_from_file(bugdir)
                except IOError as e:
                    if "No stacktrace" in str(e):
                        continue
                    else:
                        raise
                crashdata = ESCrash(crashdata)
            try:
                oracledata = ESCrash(database_id, index='oracle')
            except:
                oracledata = None
            if oracledata is None:
                oracledata = crash.Crash({
                    'database_id': database_id,
                    'bucket': bucket,
                    })
                oracledata = ESCrash(oracledata, index='oracle')
            else:
                oracledata['bucket'] = bucket
            bugs_total += 1
print str(bugs_total) + " loaded"