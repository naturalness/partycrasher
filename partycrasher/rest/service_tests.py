#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2016 Joshua Charles Campbell
#  Copyright (C) 2016 Eddie Antonio Santos

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

from __future__ import print_function

"""
Integration tests for PartyCrasher's REST API.

**Assumes ElasticSearch is running and accessible AT localhost:9200!**

Starts a fresh version of PartyCrasher for each test. Note: we DO NOT ever
import PartyCrasher in this test!
"""


import sys
import datetime
import os
import random
import signal
import socket
import subprocess
import time
import unittest
import uuid
import dateparser
import json

# Terrible Python 2/3 hacks
from six import PY2, PY3, text_type, string_types
from six.moves import xrange
from six.moves.urllib.parse import urlparse

import dateparser
import requests

from partycrasher import sample_crashes
from partycrasher.es.crash import parse_es_date

# Full path to ./rest_service.py
SOURCE_ROUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY_ROUTE = os.path.dirname(SOURCE_ROUTE)
REST_SERVICE_PATH = os.path.join(SOURCE_ROUTE, 'rest', 'service.py')
CONFIG_FILE = os.path.join(REPOSITORY_ROUTE, 'partycrasher', 'rest', 'test_config.py')
UTC = parse_es_date('now').tzinfo

# TODO: database_id => id.

class RestServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        requests.delete('http://localhost:9200/crashes')

    def setUp(self):
        self.port = random.randint(5001, 5999)
        self.origin = 'http://localhost:' + str(self.port)

        # Use currently activated Python (system-wide or in virtualenv).
        python_cmd = subprocess.check_output("which python",
                                             shell=True).rstrip()

        # Start PartyCrasher REST server.
        # Note: preexec_fn is "pre-execute function"
        #
        # os.setsid() is required to start the server in a new session in
        # Unix; Windows needs something else...
        self.rest_service = subprocess.Popen([python_cmd, REST_SERVICE_PATH,
                                              '--port', str(self.port),
                                              '--debug',
                                              '--config', CONFIG_FILE,
                                              ],
                                             preexec_fn=os.setsid)

        # Wait for the REST service to start up.
        wait_for_service_startup(self.port)

    #################
    # Test Utilites #
    #################

    @property
    def root_url(self):
        """
        The root URL of the REST service.
        """
        return self.origin + '/'

    def path_to(self, *args):
        """
        Create a URL path, relative to the current origin.
        """
        return '/'.join((self.origin,) + args)

    #########
    # Tests #
    #########

    def test_alive(self):
        """
        Can we access the root path?
        """
        response = requests.get(self.root_url)
        assert response.status_code == 200

    def test_basic_cors(self):
        """
        Can we send a pre-flight header?
        Does it state that *any* origin can make non-idempotent requests?
        """
        assert is_cross_origin_accessible(self.root_url)

    def test_absolute_url(self):
        """
        Does the server return absolute URIs?

        Relies on the root returing a ``self`` object.
        """

        response = requests.get(self.root_url)

        resource = response.json().get('href')
        assert resource is not None

        href = urlparse(resource)
        # Test in decreasing order of likely correctness:
        # Path => Domain => Scheme
        assert href.path == '/'
        # Get the origin name, minus the scheme.
        assert href.netloc == urlparse(self.origin).netloc
        assert href.scheme == 'http'

        resource = response.json().get('buckets').get('1.0')
        href = urlparse(resource)
        assert href.path.endswith('buckets/1.0')

    def test_absolute_url_behind_older_proxy(self):
        """
        Does the server return User-Agent-facing absolute URIs behind proxies?

        Using older, de facto standards:
        https://en.wikipedia.org/wiki/X-Forwarded-For

        Relies on the root returing a ``self`` object.
        """

        proxy_headers = {
            'Front-End-Https': 'on',
            'X-Forwarded-Host': 'example.org',
            'X-Forwarded-By': 'localhost',
            'X-Forwarded-Proto': 'https',
            'X-Forwarded-Ssl': 'on',
            'X-Forwarded-For': '0.0.0.0, 127.0.0.1'
        }
        response = requests.get(self.root_url, headers=proxy_headers)

        resource = response.json().get('href')
        assert resource is not None, response.text

        href = urlparse(resource)
        # Test in decreasing order of likely correctness:
        # Path => Domain => Scheme
        assert href.path == '/'
        assert href.netloc == 'example.org'
        assert href.scheme == 'https'

    def test_absolute_url_behind_newer_proxy(self):
        """
        Does the server return User-Agent-facing absolute URIs behind proxies?

        Using the Forwarded HTTP Extension:
        https://tools.ietf.org/html/rfc7239

        Relies on the root returing a ``self`` object.
        """

        proxy_headers = {
            'Forwarded': ('for = 127.0.0;'
                          'host = example.org;'
                          'proto = https, for=198.51.100.17')
        }
        response = requests.get(self.root_url, headers=proxy_headers)

        resource = response.json().get('href')
        assert resource is not None

        href = urlparse(resource)
        # Test in decreasing order of likely correctness:
        # Path => Domain => Scheme
        assert href.path == '/'
        assert href.netloc == 'example.org'
        assert href.scheme == 'https'

    def test_add_crash(self):
        """
        Add a single crash, globally;
        it must return its default bucket assignment.
        """
        assert is_cross_origin_accessible(self.path_to('reports'))

        # Make a new, unique database ID.
        database_id = str(uuid.uuid4())
        response = requests.post(self.path_to('reports'),
                                 json={'database_id': database_id,
                                       'project': 'alan_parsons',
                                       'date': datetime.datetime.utcnow().isoformat()})

        report_url = self.path_to('alan_parsons', 'reports', database_id)
        assert response.headers.get('Location') == report_url
        assert response.status_code == 201
        report = response.json().get('report')
        assert report.get('database_id').endswith(database_id)
        assert report.get('project').get('name') == 'alan_parsons'
        buckets = report.get('buckets')
        assert buckets is not None
        assert isinstance(buckets, dict)
        assert len(buckets) >= 3
        assert isinstance(buckets.get('3.8'), dict)
        assert isinstance(buckets.get('3.8').get('id'), string_types)
        assert buckets.get('3.8').get('href', '').startswith('http://')

        insert_date = report.get('date')
        assert insert_date is not None

    def test_add_crash_to_project(self):
        """
        Add a single crash to a project;
        it must return its default bucket assignment
        """

        url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(url)

        # Make a new, unique database ID.
        database_id = str(uuid.uuid4())
        response = requests.post(url, json={'database_id': database_id,
                                            'date': '2017-01-05T08:18:45'})

        assert response.status_code == 201
        report = response.json().get('report')
        assert report.get('database_id').endswith(database_id)
        assert report.get('project').get('name') == 'alan_parsons'
        assert isinstance(report.get('buckets'), dict)
        buckets = report.get('buckets')
        assert buckets.get('3.8', {}).get('href', '').startswith('http://')

    def test_add_identical_crash_to_project(self):
        """
        Adds an IDENTICAL report to a project;
        this must redirect to the existing report.
        """

        url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(url)

        # Make a new, unique database ID.
        database_id = str(uuid.uuid4())
        report = {
            'database_id': database_id,
            'platform': 'xbone',
            'date': '2017-01-05T08:18:45'
        }
        response = requests.post(url, json=report)

        # Check that it's created.
        assert response.status_code == 201
        report = response.json().get('report')
        assert report.get('database_id').endswith(database_id)
        assert report.get('project').get('name') == 'alan_parsons'
        assert isinstance(report.get('buckets'), dict)
        buckets = report.get('buckets')
        assert buckets.get('3.8', {}).get('href', '').startswith('http://')

        report_url = response.headers.get('Location')
        assert report_url is not None

        # After inserts, gotta wait...
        wait_for_elastic_search()

        # Now insert it again!
        # Note: allow_redirect must be False; Requests will automatically
        # follow redirects if not explictly told not to!
        response = requests.post(url, json=report, allow_redirects=False)

        # Must be a redirect.
        assert response.status_code == 303
        assert response.headers.get('Location') == report_url, response.headers.get('Location')

    def test_add_crash_project_name_mismatch(self):
        """
        Add a single crash to the _wrong_ project.
        It should fail without create a database entry.
        """
        create_url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(create_url)

        # Make a new, unique database ID.
        database_id = str(uuid.uuid4())
        response = requests.post(create_url,
                                 json={'database_id': database_id,
                                       'project': 'manhattan'})

        # The request should have failed.
        assert response.status_code == 400
        assert response.json().get('error') == 'ProjectMismatchError'
        assert response.json().get('project') == 'alan_parsons'
        assert (response.json().get('crash').get('project').get('name')
                == 'manhattan' 
            ),(response.text)

        # Now try to fetch it from either project
        assert 404 == requests.get(self.path_to('alan_parsons', 'reports',
            database_id)).status_code, response.text
        assert 404 == requests.get(self.path_to('manhattan', 'reports',
                                               database_id)).status_code

    def test_bad_key_name(self):
        """
        Add a single crash to the _wrong_ project.
        It should fail without create a database entry.
        """
        create_url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(create_url)

        # Make a new, unique database ID.
        database_id = str(uuid.uuid4())
        response = requests.post(create_url,
                                 json={'database_id': database_id,
                                       'dmi.decode': 'bogus'})

        # The request should have failed.
        assert response.status_code == 400
        assert response.json().get('error') == 'BadKeyNameError'
        assert 'period' in response.json().get('description'), response.text

        # Now try to fetch it from either project
        assert 404 == requests.get(self.path_to('alan_parsons', 'reports',
                                               database_id)).status_code
    def test_add_identical_ids_to_different_project(self):
        """
        Adds an IDENTICAL ID to two different projects project.
        This MUST accept the crash, but return the same ID as before.
        """


        # Make a new, unique database ID.
        database_id = str(uuid.uuid4())

        # Figure out the URLs.
        project_1 = self.path_to('alan_parsons', 'reports')
        project_2 = self.path_to('manhattan', 'reports')
        crash_1_url = self.path_to('alan_parsons', 'reports', database_id)
        crash_2_url = self.path_to('manhattan', 'reports', database_id)

        assert crash_1_url != crash_2_url

        # Post one crash.
        report = {
            'database_id': database_id,
            'platform': 'xbone',
            'date': '2017-01-05T08:18:45'
        }
        response = requests.post(project_1, json=report)

        # Check that it's created.
        assert response.status_code == 201
        report = response.json().get('report')
        assert report.get('database_id').endswith(database_id)
        assert report.get('project').get('name') == 'alan_parsons'
        assert crash_1_url in response.headers.get('Location')

        # After inserts, gotta wait...
        wait_for_elastic_search()

        # Post the same crash, but in a different project.
        response = requests.post(project_2, json=report,
                                 allow_redirects=False)

        # Check that this one's not created.
        assert response.status_code == 303
    
    def test_add_multiple(self):
        """
        Add multiple crashes to a single project;
        it must return a summary list of bucket assignments.
        """
        url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(url)

        # Make a bunch of unique database IDs
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        response = requests.post(url,
                                 json=[
                                     {'database_id': database_id_a,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_b,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_c,
                                      'date': '2017-01-05T08:18:45'},
                                 ])

        assert response.status_code == 201
        assert len(response.json()) == 3
        
        assert response.json()[0]['report']['database_id'].endswith(database_id_a)
        assert response.json()[0]['report']['project']['name'] == 'alan_parsons'
        assert isinstance(response.json()[0]['report'].get('buckets'), dict)
        buckets = response.json()[0]['report'].get('buckets')
        assert buckets.get('3.8', {}).get('href', '').startswith('http://')

        assert response.json()[1]['report']['database_id'].endswith(database_id_b)
        assert response.json()[1]['report']['project']['name'] == 'alan_parsons'
        assert isinstance(response.json()[1]['report'].get('buckets'), dict)
        buckets = response.json()[1]['report'].get('buckets')
        assert buckets.get('3.8', {}).get('href', '').startswith('http://')


        assert response.json()[2]['report']['database_id'].endswith(database_id_c)
        assert response.json()[2]['report']['buckets'] is not None
        assert response.json()[2]['report']['project']['name'] == 'alan_parsons'
        assert isinstance(response.json()[2]['report'].get('buckets'), dict)
        buckets = response.json()[2]['report'].get('buckets')
        assert buckets.get('3.8', {}).get('href', '').startswith('http://')

        # TODO: ensure if URL project and JSON project conflict HTTP 400
        #       is returned

    def test_multiple_bucketing(self):
        """
        Check if adding an identical crash results in the same bucket
        assignment.
        """

        create_url = self.path_to('ubuntu', 'reports')
        assert is_cross_origin_accessible(create_url)

        first_id = str(uuid.uuid4())
        second_id = str(uuid.uuid4())
        third_id = str(uuid.uuid4())

        # Add a full SAMPLE crash.
        report = sample_crashes.CRASH_1.copy()
        report['database_id'] = first_id
        response = requests.post(create_url, json=report)
        if response.status_code != 201:
            print(response.text)
        assert response.status_code == 201
        j = response.json()
        assert 'report' in j, response.text
        assert 'buckets' in j['report'], response.text
        first_bucket = j['report']['buckets']['1.0']['id']

        # Wait a bit...
        wait_for_elastic_search()

        # Add the SAME crash.
        report = sample_crashes.CRASH_1.copy()
        report['database_id'] = second_id
        response = requests.post(create_url, json=report)
        assert response.status_code == 201

        r = response.json().get('report')
        assert r.get('database_id').endswith(second_id)
        buckets = r.get('buckets')
        assert len(buckets) > 0

        # Get the first (most inclusive) threshold
        first_threshold = next(iter(sorted_thresholds(buckets)))

        # The first crash should matches the second (identical) crash.
        assert first_bucket in buckets[first_threshold].get('id'), \
          'The identical bug was not in the same bucket!  t={0}'.format(first_threshold)

        # Check that it contains top_match with id, project, href, and score
        assert 'top_match' in buckets
        assert buckets['top_match'].get('report_id').endswith(first_id)
        assert first_id in buckets['top_match'].get('href', ()), buckets
        assert buckets['top_match'].get('project').get('name') == 'ubuntu', buckets['top_match'].get('project') 
        assert float(buckets['top_match'].get('score', 'NaN')) > 0
        top_match_score = float(buckets['top_match']['score'])
        for key, value in buckets.items():
            try:
                threshhold = float(key)
            except ValueError:
                threshhold = None
            if threshhold is not None:
                if top_match_score > threshhold:
                    assert value is not None
                    href = buckets['top_match']['href']
                    try:
                        assert value['id'] == self.get_crash_bucket(href, key)
                    except:
                        print(key)
                        print(value)
                        print(self.get_crash_bucket(href, threshhold))
                        print(buckets['top_match']['report_id'])
                        print(threshhold)
                        raise
                else:
                    pass # check bucket size == 1?

        # Wait a bit...
        wait_for_elastic_search()

        # Add a DIFFERENT crash.
        report = sample_crashes.CRASH_2.copy()
        report['database_id'] = third_id
        response = requests.post(create_url, json=report)
        assert response.status_code == 201

        assert (response.json()
                .get('report')
                .get('database_id')
                .endswith(third_id))
        buckets = response.json().get('report').get('buckets')

        assert len(buckets) > 0
        # Get the LAST (pickiest) threshold.
        last_threshold = next(iter(reversed(sorted_thresholds(buckets))))

        # Ensure that it's not in the same bucket as the last two.
        assert first_id != buckets[last_threshold].get('id'), \
          'The different bug was found in the same bucket! t={}'.format(last_threshold)

    def test_get_crash_from_project(self):
        """
        Fetch a report from a project.
        """
        create_url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(create_url)

        # Insert a new crash with a unique database ID.
        database_id = str(uuid.uuid4())
        response = requests.post(create_url, json={'database_id': database_id,
                                                   'date': '2017-03-05T08:18:45'})
        assert response.status_code == 201

        # Wait... because... ElasticSearch... wants us to wait...
        wait_for_elastic_search()

        # Now fetch it!
        report_url = self.path_to('alan_parsons', 'reports', database_id)
        response = requests.get(report_url)
        if response.status_code != 200:
            print(json.dumps(response.json(), indent=2))
        assert response.status_code == 200
        report = response.json().get('report')
        assert report.get('database_id').endswith(database_id)
        assert report.get('project').get('name') == 'alan_parsons'
        assert isinstance(report.get('buckets'), dict)
        buckets = report.get('buckets')
        assert buckets.get('3.8', {}).get('href', '').startswith('http://')

    def test_dry_run(self):
        """
        Returns the bucket assignment were the given crash to be added.
        This crash must NOT be added, however.
        """
        url = self.path_to('alan_parsons', 'reports')
        assert is_cross_origin_accessible(url)

        database_id = str(uuid.uuid4())
        response = requests.post(url, json={'database_id': database_id},
                                 params={'dryrun': True})

        # Things go dramatically wrong if you don't wait for a bit...
        wait_for_elastic_search()

        assert response.status_code == 200
        report = response.json().get('report')
        assert report.get('database_id').endswith(database_id)
        assert report.get('project').get('name') == 'alan_parsons'
        assert isinstance(report.get('buckets'), dict), response.text
        buckets = report.get('buckets')
        assert buckets['3.8'] is None

        # Try to find this crash... and fail!
        response = requests.get(self.path_to('alan_parsons', 'reports',
                                             database_id))
        assert response.status_code == 404

    def test_get_project_bucket(self):
        """
        Fetch a bucket and its contents.
        """

        # Make a bunch of reports with IDENTICAL content!
        database_id_a = str(uuid.uuid4())
        create_url = self.path_to('alan_parsons', 'reports')

        # This is the only content for each report, so there must only be
        # *one* bucket that contains reports A, B, and C!
        tfidf_trickery = str(uuid.uuid4())

        fake_true_date = [{'database_id': str(uuid.uuid4()),
                           'tfidf_trickery': tfidf_trickery,
                           'date': '2017-01-05T08:18:45'}
                          for _ in xrange(5)]
        # Generate a bunch of FAKE data.
        fake_false_data = [{'database_id': str(uuid.uuid4()),
                            'tfidf_trickery':  str(uuid.uuid4()),
                            'date': '2017-01-05T08:18:45'}
                           for _ in xrange(10)]
        response = requests.post(create_url, json=fake_false_data)
        assert response.status_code == 201
        response = requests.post(create_url, json=fake_true_date)
        assert response.status_code == 201

        report_buckets = response.json()[0]['report']['buckets']
        threshold, bucket = get_arbitrary_bucket(report_buckets)
        bucket_url = bucket.get('href')
        assert bucket_url is not None and is_url(bucket_url)

        assert is_cross_origin_accessible(bucket_url)
        response = requests.get(bucket_url)

        assert response.status_code == 200, response.text
        # The bucket is named after the first crash... I guess?
        #assert database_id_a in response.json().get('id')
        assert response.json().get('total') >= 1
        assert response.json().get('threshold') == threshold
        # Look at the top report; it must contain tfidf_trickery.
        assert (response.json().get('top_reports')[0].get('tfidf_trickery') ==
                tfidf_trickery)

    def test_get_buckets(self):
        """
        Get top buckets for a given time frame.
        """

        # Create a bunch of reports with IDENTICAL unique content
        tfidf_trickery = str(uuid.uuid4())

        # These will all go in the Alan Parsons Project
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())

        # This one will go in the Manhattan Project
        database_id_weirdo = str(uuid.uuid4())

        project = 'chilango'

        # Add multiple reports.
        response = requests.post(self.path_to(project, 'reports'),
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date': '2017-01-05T08:18:45.959547'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date': '2017-02-05T08:18:45.959547'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date': '2017-03-05T08:18:45.959547'}
                                 ])
        assert response.status_code == 201

        # Create one duplicate in a completely different project!
        response = requests.post(self.path_to('manhattan', 'reports'),
                                 json={
                                     'database_id': database_id_weirdo,
                                     'tfidf_trickery': tfidf_trickery,
                                     'date': '2017-04-05T08:18:45.959547'
                                 })
        assert response.status_code == 201

        wait_for_elastic_search()

        # We should find our newly created reports as the most populous
        # bucket.
        search_url = self.path_to(project, 'buckets', '3.8')
        response = requests.get(search_url, 
            params={'since': '2017-01-01T00:00:00.000000',
                    'until': '2525'
                    })
        assert response.json().get('since') == '2017-01-01T00:00:00', response.content
        until = dateparser.parse(response.json().get('until'))
        assert datetime.datetime(2524, 12, 30) < until
        assert datetime.datetime(2525, 12, 30) > until
        assert len(response.json().get('buckets')) >= 2

        # Get the top bucket.
        top_bucket = response.json().get('buckets')[0]
        assert top_bucket.get('id') is not None
        assert top_bucket.get('href') is not None
        assert is_url(top_bucket['href'])
        assert top_bucket.get('total') >= 1
        assert 'first_seen' in top_bucket
        try:
            dateparser.parse(top_bucket['first_seen'])
        except:
            raise AssertionError("Can't parse date")

        first_seen = parse_es_date(top_bucket['first_seen'])
        print(repr(first_seen))
        assert parse_es_date('2017-01-05T08:00:00') < first_seen 
        assert first_seen < parse_es_date('now')

        #TODO: test adding things with various dates and check that
        # since/until actually filter stuff out adn let the right stuff
        # in

    def test_buckets_invalid_queries(self):
        """
        Send some invalid queries to top buckets.
        """

        search_url = self.path_to('alan_parsons', 'buckets', '3.8')

        # Search an invalid date -- 2015 was not a leap year!
        response = requests.get(search_url, params={'since': '2015-02-29'})
        assert response.status_code == 400, response.text

        # Search a junk value.
        response = requests.get(search_url, params={'since': 'herp'})
        assert response.status_code == 400

    def test_buckets_default_query(self):
        """
        Does it produce reasonable results for the default query?
        """

        # Upload at least one report, to ensure the database has
        # at least one bucket.
        response = requests.post(self.path_to('alan_parsons', 'reports'),
                                 json=[{'database_id': str(uuid.uuid4()),
                                        'date': datetime.datetime.utcnow().isoformat(),
                                        }])
        assert response.status_code == 201
        wait_for_elastic_search()
        # Just GET the top buckets!
        search_url = self.path_to('alan_parsons', 'buckets', '3.8')
        response = requests.get(search_url)
        assert response.status_code == 200, response.text

        # There should be at least one top bucket...
        assert len(response.json().get('buckets')) >= 1, response.text
        # It should send back a proper since date.
        assert len(response.json().get('since')) is not None

    def test_get_project_config(self):
        """
        Fetch per-project configuration.
        """
        response = requests.get(self.path_to('alan_parsons', 'config'))
        assert response.status_code == 200
        assert 0.0 <= float(response.json().get('default_threshold')) <= 10.0

    @unittest.skip('This feature is incomplete and under-specified')
    def test_change_project_config(self):
        """
        Patch the project's default threshold.
        """
        raise NotImplementedError
      
    def test_free_search(self):
        now = datetime.datetime.utcnow()

        # Create a bunch of reports with IDENTICAL unique content
        tfidf_trickery = str(uuid.uuid4())

        # These will all go in the hamburger palace
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())

        project = 'hamburgerpalace'

        # Add multiple reports.
        response = requests.post(self.path_to(project, 'reports'),
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date' : '2016-01-15T00:00:00Z'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date' : '2016-02-15T00:00:00Z'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date' : '2016-03-15T00:00:00Z'}])
        assert response.status_code == 201
        
        # Search for the tf.idf trickery.
        response = requests.get(self.path_to(project, 'search'), params={
                'q': tfidf_trickery,
            })
        
        assert response.status_code == 200
        r = response.json().get('reports')

        # It should get back the three IDs we just inserted.
        assert len(r) == 3
        
        database_urls = [
          "http://localhost:" + str(self.port) + "/hamburgerpalace/reports/" + database_id_a,
          "http://localhost:" + str(self.port) + "/hamburgerpalace/reports/" + database_id_b, 
          "http://localhost:" + str(self.port) + "/hamburgerpalace/reports/" + database_id_c
          ]
        
        print(r[0]['href'])
        
        assert r[0].get('href', '') in database_urls
        assert r[1].get('href', '') in database_urls
        assert r[2].get('href', '') in database_urls
        
        # Test date filtering
        response = requests.get(self.path_to(project, 'search'), params={
                'q': tfidf_trickery,
                'since': '2016-01-01',
                'until': '2016-02-01'
            })
        assert response.status_code == 200
        r = response.json().get('reports')
        assert len(r) == 1
        assert r[0].get('href', '') == ("http://localhost:" 
          + str(self.port) 
          + "/hamburgerpalace/reports/" 
          + database_id_a)

        response = requests.get(self.path_to(project, 'search'), params={
                'q': tfidf_trickery,
                'since': '2016-02-01',
                'until': '2016-03-01'
            })
        assert response.status_code == 200
        r = response.json().get('reports')
        assert len(r) == 1
        assert r[0].get('href', '') == ("http://localhost:" 
          + str(self.port) 
          + "/hamburgerpalace/reports/" 
          + database_id_b)

        response = requests.get(self.path_to(project, 'search'), params={
                'q': tfidf_trickery,
                'since': '2016-03-01',
                'until': '2016-04-01'
            })
        assert response.status_code == 200
        r = response.json().get('reports')
        assert len(r) == 1
        assert r[0].get('href', '') == ("http://localhost:" 
          + str(self.port) 
          + "/hamburgerpalace/reports/" 
          + database_id_c)
        
    def test_buckets_query_and_date(self):
        now = datetime.datetime.utcnow()

        # Create a bunch of reports with IDENTICAL unique content
        tfidf_trickery = str(uuid.uuid4())
        tfidf_trickery_2 = str(uuid.uuid4())

        # These will all go in the hamburger palace
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        database_id_d = str(uuid.uuid4())
        #print(database_id_a)
        #print(database_id_b)
        #print(database_id_c)
        #print(database_id_d)

        project = 'X'

        # Add multiple reports.
        response = requests.post(self.path_to(project, 'reports'),
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date' : '2016-01-15T00:00:00Z'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date' : '2016-02-15T00:00:00Z'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'date' : '2016-03-15T00:00:00Z'}, 
                                     {'database_id': database_id_d,
                                      'tfidf_trickery': tfidf_trickery_2,
                                      'date' : '2016-03-15T00:00:00Z'}]) 
        assert response.status_code == 201
        database_urls = []
        for c in response.json():
            database_urls.append(
                "http://localhost:" + str(self.port) + "/X/buckets/11.0/" 
                + c['buckets']['11.0']['id'])
        
        # Search for the tf.idf trickery.
        response = requests.get(self.path_to(project, 'buckets', '11.0'),
                                params={
                                    'q': tfidf_trickery,
                                    'since': '2000',
                                })
        assert response.status_code == 200
        r = response.json().get("buckets")
        
        #print(json.dumps(r, indent=2))
        #assert False

        # It should get back the three IDs we just inserted.
        assert len(r) == 3, response.content
        
        print(r[0]['href'])
        
        assert r[0].get('href', '') in database_urls, database_urls
        assert r[1].get('href', '') in database_urls
        assert r[2].get('href', '') in database_urls
        
        # Test date filtering
        response = requests.get(self.path_to(project, 'buckets', '11.0'), params={
                'q': tfidf_trickery,
                'since': '2016-01-01',
                'until': '2016-02-01'
            })
        assert response.status_code == 200
        r = response.json().get("buckets")
        assert len(r) == 1
        assert r[0].get('href', '') == database_urls[0]

        response = requests.get(self.path_to(project, 'buckets', '11.0'), params={
                'q': tfidf_trickery,
                'since': '2016-02-01',
                'until': '2016-03-01'
            })
        assert response.status_code == 200
        r = response.json().get("buckets")
        assert len(r) == 1
        assert r[0].get('href', '') == database_urls[1]

        response = requests.get(self.path_to(project, 'buckets', '11.0'), params={
                'q': tfidf_trickery,
                'since': '2016-03-01',
                'until': '2016-04-01'
            })
        assert response.status_code == 200
        r = response.json().get("buckets")
        assert len(r) == 1
        assert r[0].get('href', '') == database_urls[2]
        
    def test_summary(self):
        create_url = self.path_to('ubuntu', 'reports')

        first_id = str(uuid.uuid4())
        second_id = str(uuid.uuid4())
        third_id = str(uuid.uuid4())

        report = sample_crashes.CRASH_1.copy()
        report['database_id'] = first_id
        response = requests.post(create_url, json=report)

        report = sample_crashes.CRASH_2.copy()
        report['database_id'] = second_id
        response = requests.post(create_url, json=report)
        
        report = sample_crashes.CRASH_2.copy()
        report['database_id'] = third_id
        response = requests.post(create_url, json=report)
        
        wait_for_elastic_search()
        
        summary_url = self.path_to('ubuntu', 'reports', third_id)
        response = requests.get(summary_url,
                                params={'auto_summary': True})
        assert response.status_code == 200
        stuff = response.json().get('auto_summary')
        assert isinstance(stuff, list)
        for i in stuff:
            assert isinstance(i['field'], string_types)
            assert isinstance(i['term'], string_types)
            assert isinstance(i['value'], float)
    
    def test_ingest_explain(self):
        url = self.path_to('cheeseburger', 'reports')
        assert is_cross_origin_accessible(url)
        # Make a bunch of unique database IDs -- project 1 
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        tfidf_trickery = str(uuid.uuid4()) + " " + str(uuid.uuid4())
        tfidf_trickery2 = str(uuid.uuid4()) + " " + str(uuid.uuid4())

        response = requests.post(url,
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                 ])
        assert response.status_code == 201
        assert len(response.json()) == 3


        url = self.path_to('hamburger', 'reports')
        assert is_cross_origin_accessible(url)
        # Make a bunch of unique database IDs -- project 2
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        response = requests.post(url,
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                 ],
                                     params={'explain': True}
            )
        assert response.status_code == 201
        j = response.json()
        assert len(j) == 3
        for i in j:
            assert 'explanation' in i, response.text

    def test_project_bucket_filter(self):
        url = self.path_to('katy_b', 'reports')
        assert is_cross_origin_accessible(url)
        # Make a bunch of unique database IDs -- project 1 
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        tfidf_trickery = str(uuid.uuid4()) + " " + str(uuid.uuid4())
        tfidf_trickery2 = str(uuid.uuid4()) + " " + str(uuid.uuid4())

        response = requests.post(url,
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                 ])
        assert response.status_code == 201, response.text
        assert len(response.json()) == 3, response.text

        url = self.path_to('jackson', 'reports')
        assert is_cross_origin_accessible(url)
        # Make a bunch of unique database IDs -- project 2
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        response = requests.post(url,
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery,
                                      'tfidf_trickery2': tfidf_trickery2,
                                      'date': '2017-01-05T08:18:45'},
                                 ],
                                     params={'explain': True})
        assert response.status_code == 201, response.text
        assert len(response.json()) == 3
        assert response.json()[0]['report']['buckets']['top_match'] is not None
        
        buckets_url = self.path_to('jackson', 'buckets', '1.0')
        response = requests.get(buckets_url,
            params={'since': '2017-01-01T00:00:00.000000',
                    'until': '2525'
                    })

        j = response.json()
        assert 'buckets' in j, response.text
        assert len(j['buckets']) == 1, response.text
        assert j['buckets'][0]['total'] == 3

    def tearDown(self):
        # Kill the ENTIRE process group of the REST server.
        # This should really be the subprocess.Popen.terminate() behavior by
        # default...
        os.killpg(os.getpgid(self.rest_service.pid), signal.SIGTERM)
        self.rest_service.wait()

    def get_crash_bucket(self, href, threshhold):
        """
        Fetch a report and then return the bucket id
        """

        # Now fetch it!
        response = requests.get(href)
        try:
            assert response.status_code == 200
            report = response.json().get('report')
            assert report.get('buckets').get(threshhold) is not None
        except:
            print(href)
            print(response.json() and response.json()
                  .get('report')
                  .get('buckets'))
            raise
        return report.get('buckets').get(threshhold).get('id')

######################
# More Test Utilites #
######################


def is_cross_origin_accessible(path, origin='http://example.org'):
    """
    Returns True if the path is accessible at the given origin
    (default: example.org).

    Raises AssertionError otherwise.
    """

    response = requests.options(path, headers={'Origin': origin})
    assert response.status_code == 200
    assert is_allowed_origin(origin, response)

    return True


def is_allowed_origin(origin, response):
    """
    Returns True when origin is allowed by the OPTIONS response.

    Raises AssertionError otherwise.
    """
    assert 'Access-Control-Allow-Origin' in response.headers

    # Either we're allowing ALL...
    raw_origins = response.headers['Access-Control-Allow-Origin']
    if raw_origins.strip() == '*':
        return True

    # Or we're explicitly allowing this host.
    allowed_origins = [o.strip() for o in raw_origins.split()]
    assert origin in allowed_origins
    return True


def is_url(text):
    """
    Returns True when ``text`` is a web URL.

    Raises AssertionError otherwise.
    """
    parse_result = urlparse(text)

    assert parse_result.scheme in ('http', 'https')
    assert parse_result.netloc
    assert parse_result.path.startswith('/')
    return True


def sorted_thresholds(buckets):
    return sorted((key for key in buckets if key != 'top_match'), key=float)

def get_arbitrary_bucket(buckets):
    """
    Given buckets, returns a random bucket.
    """
    assert isinstance(buckets, dict),\
        "Buckets does not appear to be a dict"
    assert len(buckets) >= 3,\
        "Not enough buckets to sample from"
    buckets = buckets.copy()

    try:
        del buckets['top_match']
    except KeyError:
        pass

    return random.choice(list(buckets.items()))


def wait_for_elastic_search():
    time.sleep(2.5)


# Adapted from: http://stackoverflow.com/a/19196218
def wait_for_service_startup(port, timeout=5.0, delay=0.25,
                             hostname='127.0.0.1'):

    start_time = time.time()
    max_time = start_time + timeout
    while time.time() < max_time:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if 0 == sock.connect_ex((hostname, port)):
            # Connected!
            return
        time.sleep(delay)
        sock.close()

    raise RuntimeError('Could not connect to {}:{}'.format(hostname, port))

if __name__ == '__main__':
    unittest.main()
