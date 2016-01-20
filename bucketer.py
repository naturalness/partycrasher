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

import json
from crash import Crash 

class Bucketer(object):
    """Superclass for bucketers which require pre-existing data to work."""
    
    def __init__(self, max_buckets=0):
        self.max_buckets = max_buckets
    
    def bucket(self, crash):
        assert isinstance(crash, Crash)
        raise NotImplementedError("I don't know how to generate a signature for this crash.")
    
class MLT(Bucketer):
    
    def __init__(self, index='crashes', es=None, thresh=1.0, *args, **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.index = index
        self.es = es
        self.thresh = thresh
        
    def bucket(self, crash):
        assert isinstance(crash, Crash)
        matches = self.es.search(
        index=self.index,
        body={
            '_source': False,
            'min_score': self.thresh,
            'query': {
            'more_like_this': {
                'docs': [{
                    '_index': self.index,
                    '_type': 'crash',
                    'doc': crash,
                    }]
                },
                },
            'aggregations': {
                'buckets': {
                    'terms': {
                        'field': 'bucket',
                        'size': self.max_buckets
                    },
                    'aggs': {
                        'top': {
                            'top_hits': {
                                'size': 1,
                                '_source': {
                                    'include': ['database_id'],
                                    }
                                }
                            }
                        }
                }
            }
        })
        matching_buckets=[]
        for match in matches['aggregations']['buckets']['buckets']:
            assert match['top']['hits']['max_score'] >= self.thresh
            matching_buckets.append(match['key'])
        return matching_buckets
