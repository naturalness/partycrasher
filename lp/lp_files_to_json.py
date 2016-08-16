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
Crash = crash.Crash

topdir = sys.argv[1]

buckets = []

bugs_total = 0
no_stacktrace = 0

crashes = dict()
oracle = dict()

for bucketdir in os.listdir(topdir):
    bucket = bucketdir
    bucketdir = os.path.join(topdir, bucketdir)
    assert os.path.isdir(bucketdir)
    buglist = os.listdir(bucketdir)
    #if len(buglist) < 2:
        #continue
    buckets.append(bucket)
    for bugdir in buglist:
        bugdir = os.path.join(bucketdir, bugdir)
        assert os.path.isdir(bugdir)
        #print repr(os.listdir(bugdir))
        if len(os.listdir(bugdir)) > 1:
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
print(str(bugs_total) + " loaded", file=sys.stderr)
print(str(no_stacktrace) + " thrown out because of unparsable stacktraces", file=sys.stderr)
print(json.dumps({'crashes': crashes, 'oracle': oracle}, cls=crash.CrashEncoder, indent=2))

