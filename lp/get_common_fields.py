#!/usr/bin/env python

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

from __future__ import division

import os, sys, pprint, random, time, operator, math, json
import crash
from es_crash import ESCrash
from elasticsearch import Elasticsearch
import elasticsearch.helpers

es = ESCrash.es

counts = {}

mappings = es.indices.get_field_mapping(field='*', index='crashes', doc_type='crash')
fields = mappings['crashes']['mappings']['crash'].keys()
#print json.dumps(fields, indent=4)
for field in fields:
    matches = es.search(
        index='crashes',
        body={
            'query': {
                'filtered':{
                    'query': {
                        'match_all': {}
                        },
                    'filter': {
                        'exists': {
                            'field': field,
                        }
                    }
                }
            },
        })
    count = matches['hits']['total']
    counts[field] = count
sorted_counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
sorted_counts = [c[0] for c in sorted_counts if c[1] > 200]
print json.dumps(sorted_counts, indent=4)