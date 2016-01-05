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

import os, sys
import crash
from topN import TopN, TopNLoose, TopNAddress

topdir = sys.argv[1]

crashes = []
buckets = []

comparisons = {
    'top1': {'comparer': TopN(1)}, 
    'top2': {'comparer': TopN(2)},
    'top3': {'comparer': TopN(3)},
    'top3l': {'comparer': TopNLoose(3)},
    'top3a': {'comparer': TopNAddress(3)},
}


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
            crashdata = crash.Crash.load_from_file(bugdir)
            crashdata['bucket'] = bucket
            if len(crashdata['stacktrace']) < 1:
                continue
            crashes.append(crashdata)
            print "in %i crashes and %i bugkets:" % (len(crashes), len(buckets))
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
                for other in crashes:
                    compared_same = comparison_data['comparer'].compare(crashdata, other)
                    bucket_same = (crashdata['bucket'] == other['bucket'])
                    if compared_same and bucket_same:
                        comparison_data['tp'] += 1
                    if compared_same and (not bucket_same):
                        comparison_data['fp'] += 1
                    if (not compared_same) and (not bucket_same):
                        comparison_data['tn'] += 1
                    if (not compared_same) and bucket_same:
                        comparison_data['fn'] += 1
                print "%s: tp %i, fp %i, tn %i, fn %i" \
                    % (comparison,
                       comparison_data['tp'],
                       comparison_data['fp'],
                       comparison_data['tn'],
                       comparison_data['fn'],
                      )
                try:
                    print "%s: recall %f, specificity %f, precision %f, fall-out %f" \
                        % (comparison,
                        comparison_data['tp']/(comparison_data['tp']+comparison_data['fn']),
                        comparison_data['tn']/(comparison_data['fp']+comparison_data['tn']),
                        comparison_data['tp']/(comparison_data['tp']+comparison_data['fp']),
                        comparison_data['fp']/(comparison_data['fp']+comparison_data['tn']),
                        )
                except ZeroDivisionError:
                    pass
            print ""
