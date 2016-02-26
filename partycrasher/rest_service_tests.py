#!/usr/bin/env python

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

"""
Integration tests for PartyCrasher's REST API.

**Assumes ElasticSearch is running and accessible AT localhost:9200!**

Starts a fresh version of PartyCrasher for each test. Note: we DO NOT ever
import PartyCrasher in this test!
"""


import datetime
import os
import random
import signal
import subprocess
import sys
import time
import unittest
import uuid

import requests


# Full path to ./rest_service.py
REST_SERVICE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'rest_service.py')


class RestServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.port = random.randint(5000, 5999)
        self.url = 'http://localhost:' + str(self.port) + '/'

        # Use currently activated Python (system-wide or in virtualenv).
        python_cmd = subprocess.check_output("which python", shell=True).rstrip()

        # Start PartyCrasher REST server.
        self.rest_service = subprocess.Popen([python_cmd, REST_SERVICE_PATH,
                                              str(self.port)],
        # "pre-execute function"
        # os.setsid required to start the server in a new session in Unix;
        # Windows needs something else
                                             preexec_fn=os.setsid)

        # Wait for the REST service to start up.
        time.sleep(1)

    def test_alive(self):
        """
        Can we access the root path?
        """
        response = requests.get(self.url)
        assert response.status_code == 200

    def testAddCrash(self):
        database_id = str(uuid.uuid4())
        response = requests.post(self.url + 'reports',
                                 json={'database_id': database_id})
        assert response.status_code == 201
        assert response.json()['crash']['database_id'] == database_id
        assert response.json()['crash']['bucket'] is not None
        # TODO: bucket url

    def testAddCrashProject(self):
        database_id = str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/reports',
                                 json={'database_id': database_id})
        assert response.status_code == 201
        assert response.json()['crash']['database_id'] == database_id
        assert response.json()['crash']['bucket'] is not None
        assert response.json()['crash']['project'] == 'alan_parsons'
        # TODO: bucket url
        # TODO: ensure if URL project and JSON project conflict HTTP 400
        #       is returned

    def testDryRun(self):
        database_id = str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/reports/dry-run',
                                 json={'database_id': database_id})
        assert response.status_code == 202
        assert response.json()['crash']['database_id'] == database_id
        assert response.json()['crash']['bucket'] is not None
        assert response.json()['crash']['project'] == 'alan_parsons'
        # TODO: bucket url

    def testAddMultiple(self):
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/reports/dry-run',
                                 json=[
                                     {'database_id': database_id_a},
                                     {'database_id': database_id_b},
                                     {'database_id': database_id_c},
                                     ]
                                 )
        assert response.status_code == 201
        assert response.json()['crashes'][0]['database_id'] == database_id_a
        assert response.json()['crashes'][0]['bucket'] is not None
        assert response.json()['crashes'][0]['project'] == 'alan_parsons'
        # TODO: bucket url
        assert response.json()['crashes'][1]['database_id'] == database_id_b
        assert response.json()['crashes'][1]['bucket'] is not None
        assert response.json()['crashes'][1]['project'] == 'alan_parsons'
        # TODO: bucket url
        assert response.json()['crashes'][2]['database_id'] == database_id_c
        assert response.json()['crashes'][2]['bucket'] is not None
        assert response.json()['crashes'][2]['project'] == 'alan_parsons'
        # TODO: bucket url
        # TODO: ensure if URL project and JSON project conflict HTTP 400
        #       is returned

    def testGetCrash(self):
        database_id = str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/reports',
                                 json={'database_id': database_id})
        assert response.status_code == 202
        response = requests.get(self.url + 'alan_parsons/reports/' + database_id)
        assert response.status_code == 200
        assert response.json()['crash']['database_id'] == database_id
        assert response.json()['crash']['bucket'] is not None
        assert response.json()['crash']['project'] == 'alan_parsons'
        # TODO: bucket url

    def testGetCrashProject(self):
        raise NotImplementedError()
        # TODO: ensure if URL project and JSON project conflict HTTP 400
        #       is returned

    def testDeleteCrash(self):
        database_id = str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/reports',
                                 json={'database_id': database_id})
        assert response.status_code == 202
        response = requests.delete(self.url + 'alan_parsons/reports/' + database_id)
        assert response.status_code == 204
        response = requests.get(self.url + 'alan_parsons/reports/' + database_id)
        assert response.status_code == 404

    def testDeleteCrashProject(self):
        raise NotImplementedError()
        # TODO: ensure if URL project and JSON project conflict HTTP 400
        #       is returned

    def testGetProjectConfig(self):
        response = requests.get(self.url + 'alan_parsons/config')
        assert response.status_code == 200
        assert response.json()['default_threshold'] is not None

    def testGetProjectBucket(self):
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        tfidf_trickery= str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/reports/dry-run',
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery},
                                     ]
                                 )
        assert response.status_code == 201
        response = requests.get(self.url + 'alan_parsons/buckets/4.0/' + database_id_a)
        assert response.json()['bucket'] == database_id_a
        assert response.json()['number_of_reports'] == 3
        assert response.json()['top_reports'][0]['tfidf_trickery'] == tfidf_trickery

    def testGetTopBuckets(self):
        now = datetime.datetime.utcnow()
        database_id_a = str(uuid.uuid4())
        database_id_b = str(uuid.uuid4())
        database_id_c = str(uuid.uuid4())
        tfidf_trickery= str(uuid.uuid4())
        response = requests.post(self.url + 'alan_parsons/buckets',
                                 json=[
                                     {'database_id': database_id_a,
                                      'tfidf_trickery': tfidf_trickery},
                                     {'database_id': database_id_b,
                                      'tfidf_trickery': tfidf_trickery},
                                     {'database_id': database_id_c,
                                      'tfidf_trickery': tfidf_trickery},
                                     ]
                                 )
        assert response.status_code == 201
        response = requests.get(self.url + 'alan_parsons/buckets/4.0',
                                params={'since': str(now)})
        assert response.json()['since'] == str(now)
        assert response.json()['top_buckets'][0]['bucket'] == database_id_a
        assert response.json()['top_buckets'][0]['number_of_reports'] == 3

    def tearDown(self):
        # This should really be the subprocess.Popen.terminate() behavior by default...
        os.killpg(os.getpgid(self.rest_service.pid), signal.SIGTERM)
        self.rest_service.wait()


if __name__ == '__main__':
    unittest.main()
