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

import copy, os, datetime, time
import requests
import dateutil.parser as dateparser
import json_store

uuids_at_once = 1000

uuids_query_url = 'https://crash-stats.mozilla.com/api/SuperSearch/'
uuids_query = {
    '_columns': ['uuid', 'date'],
    'sort': 'date',
    '_facets_size': 1,
    '_results_number': uuids_at_once,
}

last_total_uuids = 2450724

delay = 1.0

last_query = datetime.datetime.utcnow()


def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        serialized = obj.isoformat()
        return serialized
    else:
        raise TypeError(repr(obj) + " is not JSON serializable or a date!")


def json_deserializer(d):
    for k, v in d.iteritems():
        if isinstance(v, basestring):
            d[k] = dateparser.parse(v)
    return d

def attempt():
    global last_total_uuids
    global last_query
    global delay
    
    days = dict()

    results_position = 0
  
    starttime = datetime.datetime.utcnow()

    session = requests.Session()

    while results_position <= last_total_uuids:
        uuids_page_query = copy.deepcopy(uuids_query)
        uuids_page_query['_results_offset'] = results_position
        while True:
            now = datetime.datetime.utcnow()
            sleep_time = (last_query - now).total_seconds() + delay
            if sleep_time > 0.0:
                time.sleep(sleep_time)
            last_query = datetime.datetime.utcnow()
            response = session.get(uuids_query_url, params=uuids_page_query)
            if response.status_code == 429:
                print "429'd :((("
                time.sleep(60)
                delay = delay * 1.1
            else:
                break
        try:
            assert response.status_code == 200
            assert 'application/json' in response.headers['content-type']
        except:
            print response.status_code
            print response.text
            raise
        responsedata = response.json()
        newuuids = 0
        results = 0
        for hit in responsedata['hits']:
            uuid = hit['uuid']
            crashts = dateparser.parse(hit['date'])
            date = crashts.date()
            if not date in days:
                days[date] = json_store.JSONStore("days/%s.json" % (str(date)),
                    json_kw={'default':json_serializer},
                    object_hook=json_deserializer,
                    )
            if not uuid in days[date]:
                newuuids += 1
                days[date][uuid] = crashts
            results += 1
        prev_total_uuids = last_total_uuids
        last_total_uuids = int(responsedata['total'])
        total_uuids_delta = abs(last_total_uuids - prev_total_uuids)
        if (total_uuids_delta > results/2):
            print "Results set shifting too fast :("
        # force the results windows to overlap :(
        # this is to prevent shifting result set from 
        # causing gaps
        results_position += int(results/2)
        if (newuuids > 0):
            for day, daydata in days.iteritems():
                daydata.sync()
        now = datetime.datetime.utcnow()
        dt = now - starttime
        rate = dt/results_position
        eta = rate*(last_total_uuids-results_position)
        total_have = 0
        for day, daydata in days.iteritems():
            total_have += len(daydata)
        print "%s %i/%i, %i uuids total in %i days\n\t    ETA %s delay %f" % (
                now.isoformat(),
                results_position, 
                last_total_uuids, 
                total_have,
                len(days),
                str(eta),
                delay
            )
        daylist = sorted(days.keys())
        for day in daylist:
            print "\t%s: %i" % (day, len(days[day]))

while True:
    started = datetime.datetime.utcnow().date()
    attempt()
    finished = datetime.datetime.utcnow().date()
    print "Started on %s" % (started.isoformat())
    print "Finished on %s" % (finished.isoformat())
    print "Time: %s" % (finished - started)
    while True:
        nextattempt = started + datetime.timedelta(hours=3)
        if datetime.datetime.utcnow().date() > nextattempt:
            break
        time.sleep(60)