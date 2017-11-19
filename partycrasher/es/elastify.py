#!/usr/bin/env python

#  Copyright (C) 2015, 2016, 2017 Joshua Charles Campbell

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

import json

from six import string_types

from partycrasher.threshold import Threshold
from partycrasher.bucket import Buckets
from partycrasher.project import Project
from partycrasher.pc_encoder import PCEncoder
from collections import OrderedDict


class ESCrashEncoder(PCEncoder):

    @staticmethod
    def hacky_serialize_thresholds(buckets):
        """
        Must serialize thresholds, but ElasticSearch is all like... nah.
        Actually the problem is that python dumps doesn't allow non-string keys?
        """
        assert isinstance(buckets, Buckets)

        new_dict = OrderedDict()
        for key, value in buckets.items():
            if isinstance(key, Threshold):
                # Change threshold to saner value.
                key = key.to_elasticsearch()
                value = value['id']
                new_dict[key] = value
            elif isinstance(key, string_types):
                new_dict[key] = value
                continue
            else:
                raise TypeError()
        return new_dict

    def default(self, o):
        #assert False
        #print(type(o), file=sys.stderr)
        if isinstance(o, Buckets):
            return self.hacky_serialize_thresholds(o)
        else:
            return super(ESCrashEncoder, self).default(o)

def elastify(o, **kwargs):
    return json.dumps(o, cls=ESCrashEncoder, **kwargs)
