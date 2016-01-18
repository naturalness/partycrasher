#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2016 Jshua Charles Campbell

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

import os, sys, re, errno, json, copy, datetime, time, uuid
import dateutil.parser as dateparser
import json_store
import requests

crash_query_url = 'https://crash-stats.mozilla.com/api/ProcessedCrash/'
crash_query = {
    'datatype': 'processed',
    }


delay = 0.65
last_query = datetime.datetime.utcnow()

# attempt to download 1/4 of the data (by UUID)
target_limit = 2**126 


def doaday(day=None):
    global delay
    global last_query
    session = requests.Session()
    print day
    path = 'days/%s' % (str(day))
    done = 0
    downloaded = 0
    started = datetime.datetime.utcnow()
    with open(path + '.json', 'r') as infile:
        data = json.load(infile)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    for auuid in data.keys():
        if uuid.UUID(auuid).int > target_limit:
            del data[auuid]
    for auuid in sorted(data.keys()):
        auuid_path = path + '/%s.json' % auuid
        if os.path.isfile(auuid_path):
            done += 1
            continue
        crash_query_auuid = copy.deepcopy(crash_query)
        crash_query_auuid['crash_id'] = auuid
        while True:
            now = datetime.datetime.utcnow()
            sleep_time = (last_query - now).total_seconds() + delay
            if sleep_time > 0.0:
                time.sleep(sleep_time)
            last_query = datetime.datetime.utcnow()
            response = session.get(crash_query_url, params=crash_query_auuid)
            if response.status_code == 429:
                print "Got 429 :("
                time.sleep(120)
            elif response.status_code == 424:
                print "Got 424... failed dependency?"
                print response.status_code
                print response.text
                print response.url
                break
            else:
                #delay = delay*0.99
                break
        if response.status_code == 424:
            continue # No clue what's going on here, waiting for a response
                     # from mozilla, for now just skip it
        try:
            assert response.status_code == 200
            assert 'application/json' in response.headers['content-type']
        except:
            print response.status_code
            print response.text
            raise
        with open(auuid_path, "w") as json_file:
            json_file.write(response.text)
        done += 1
        downloaded += 1
        remaining = len(data)-done
        now = datetime.datetime.utcnow()
        dt = now - started
        rate = dt/downloaded
        eta = rate * remaining
        print "%s: %i/%i ETA: %s delay %f" % (day, done, len(data), eta, delay)
    return downloaded


while True:
    restart = False
    flist = os.listdir('days')
    daylist = []
    for f in flist:
        match = re.match('(\d+-\d+-\d+).json$', f)
        if not match is None:
            date = dateparser.parse(match.group(1)).date()
            #print date
            daylist.append(date)
            
    for day in sorted(daylist, reverse=False):
        while True:
            if doaday(day) == 0:
                break
            else:
                restart = True
        if restart:
            break
    
