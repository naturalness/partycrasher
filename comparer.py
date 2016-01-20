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

from crash import Crash
from bucketer import Bucketer
from es_crash import ESCrash

class Comparer(Bucketer):
    
    def __init__(self, index='crashes', es=None, *args, **kwargs):
        super(Comparer, self).__init__(*args, **kwargs)
        self.index = index
        self.es = es

    def get_signature(self, crash):
        assert isinstance(crash, Crash)
        raise NotImplementedError("I don't know how to generate a signature for this crash.")
    
    def compare(self, a, b):
        return (self.get_signature(a) == self.get_signature(b))
    
    def bucket(self, crash):
        assert isinstance(crash, Crash)
        matches = self.es.search(
        index=self.index,
        body={
            'query': {
                'filtered':{
                    'query': {
                        'match_all': {}
                        },
                    'filter': {
                        'term': {
                            self.name: self.get_signature(crash),
                        }
                    }
                }
            },
            'aggregations': {
                'buckets': {
                    'terms': {
                        'field': 'bucket',
                        'size': self.max_buckets
                    }
                }
            }
        })
        matching_buckets=[]
        for match in matches['aggregations']['buckets']['buckets']:
            matching_buckets.append(match['key'])
        return matching_buckets
    
    def save_signature(self, crash):
        savedata = ESCrash(crash, index=self.index)
        savedata[self.name] = self.get_signature(crash)
        return savedata

