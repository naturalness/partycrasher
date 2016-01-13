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

import os, sys, re, errno, json, copy, datetime, time
import dateutil.parser as dateparser
import json_store
import requests

crash_query_url = 'https://crash-stats.mozilla.com/api/ProcessedCrash/'
crash_query = {
    'datatype': 'processed',
    }


delay = 0.7

def doaday(day=None):
    global delay
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
    for uuid in sorted(data.keys()):
        uuid_path = path + '/%s.json' % uuid
        if os.path.isfile(uuid_path):
            done += 1
            continue
        crash_query_uuid = copy.deepcopy(crash_query)
        crash_query_uuid['crash_id'] = uuid
        while True:
            time.sleep(delay)
            response = session.get(crash_query_url, params=crash_query_uuid)
            if response.status_code == 429:
                print "Delay reset, was %f" % (delay)
                delay = delay*1.1
                time.sleep(60)
            else:
                #delay = delay*0.99
                break
        try:
            assert response.status_code == 200
            assert 'application/json' in response.headers['content-type']
        except:
            print response.status_code
            print response.text
            raise
        with open(uuid_path, "w") as json_file:
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
        match = re.match('(\d+-\d+-\d+).json', f)
        if not match is None:
            date = dateparser.parse(match.group(1)).date()
            #print date
            daylist.append(date)
            
    for day in sorted(daylist, reverse=True):
        while True:
            if doaday(day) == 0:
                break
            else:
                restart = True
        if restart:
            break
    