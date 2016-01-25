#!/usr/bin/env python

#  Copyright (C) 2015, 2016 Jshua Charles Campbell

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

import os, sys, pprint, random, time
import crash
from topN import TopN, TopNLoose, TopNAddress, TopNFile
from es_crash import ESCrash
from elasticsearch import Elasticsearch
import elasticsearch.helpers
from bucketer import MLT, MLTf, MLTlc, MLTw
import json

es = ESCrash.es

r = es.search(index='crashes',
    body={
        'size': 0,
        'aggs': {
            'packs': {
                'cardinality': {
                    'field': 'SourcePackage',
                    'precision_threshold': 0
                        }
                }
            }
        })

print json.dumps(r, indent=4)

r = es.search(index='crashes',
    body={
        'size': 0,
        'aggs': {
            'packs': {
                'terms': {
                    'shard_size': 0,
                    'field': 'SourcePackage',
                    },
                },
            }
        })

print json.dumps(r, indent=4)