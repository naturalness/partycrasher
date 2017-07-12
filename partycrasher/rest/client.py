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

import requests

from partycrasher.crash import Crash


class RestClient:
    
    def __init__(self, root_url="http://localhost:5000/"):
        self.origin = root_url.rstrip('/')

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

    def get_a_bunch_of_crashes(self, date_range_start, limit):
      bunch = []
      step = 100
      for from_ in range(0, limit, step):
          query = {
            'from': from_,
            'since': date_range_start,
            'size': step,
          }
          response = requests.get(self.path_to('*', 'search'), params=query)
          response.raise_for_status()
          for crash in response.json():
              crash = Crash(crash)
              bunch.append(crash)
      return bunch
    
    def compare(self, id_, others):
        response = requests.get(self.path_to('reports', id_, 'compare'), json=others)
        response.raise_for_status()
        responsedata = response.json()
        return responsedata
        return response.json()
