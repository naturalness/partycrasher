#!/usr/bin/env python

#  Copyright (C) 2016 Joshua Charles Campbell

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

# This is a seperate module because rest_service.py is meant to be run as
# __main__.

import os, subprocess, signal, sys, requests, unittest, time, random

class RestServiceTestCase(unittest.TestCase):
    
    def setUp(self):
        self.port = random.randint(5000, 5999)
        self.url = 'http://localhost:' + str(self.port) + '/'
        python_cmd = subprocess.check_output("which python", shell=True).rstrip()
        print python_cmd
        # preexec_fn=os.setid required for process group on unix, windows needs something else
        self.rest_service = subprocess.Popen([python_cmd, "rest_service.py", str(self.port)], preexec_fn=os.setsid)
        time.sleep(1)
    
    def testAlive(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        
    def tearDown(self):
        # This should really be the subprocess.Popen.terminate() behavior by default...
        os.killpg(os.getpgid(self.rest_service.pid), signal.SIGTERM)
        self.rest_service.wait()
        
if __name__ == '__main__':
    unittest.main()