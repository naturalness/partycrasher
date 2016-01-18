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

crashes = []
buckets = []

comparisons = {
    'top1': {'comparer': TopN(1)}, 
    'top2': {'comparer': TopN(2)},
    'top3': {'comparer': TopN(3)},
    'top3l': {'comparer': TopNLoose(3)},
    'top3a': {'comparer': TopNAddress(3)},
    'top1file' : {'comparer': TopNFile(1)},
}

#TODO: MISSING CODE HERE TO ITERATE OVER EVERYTHING IN ELASTIC

            if crashdata is None:
                try:
                    crashdata = crash.Crash.load_from_file(bugdir)
                except IOError as e:
                    if "No stacktrace" in str(e):
                        continue
                    else:
                        raise
                crashdata['bucket'] = bucket
                crashdata = ESCrash(crashdata)
                print "Disk: " + database_id
            if len(crashdata['stacktrace']) < 1:
                continue
            if (len(crashes) % 100) == 0:
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
                #print "%s: tp %i, fp %i, tn %i, fn %i" \
                    #% (comparison,
                       #comparison_data['tp'],
                       #comparison_data['fp'],
                       #comparison_data['tn'],
                       #comparison_data['fn'],
                      #)
                if (len(crashes) % 100) == 0:
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
            if (len(crashes) % 100) == 0:
                print ""
            crashes.append(crashdata)

