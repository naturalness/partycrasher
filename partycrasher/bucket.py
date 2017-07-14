#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016, 2017 Joshua Charles Campbell

#  This program is free software; you can reditext_typeibute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is ditext_typeibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from collections import namedtuple, OrderedDict
import os
from datetime import datetime

from six import text_type, string_types
import dateparser

from partycrasher.pc_dict import PCDict, FixedPCDict

from partycrasher.threshold import Threshold
from partycrasher.project import Project

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from base64 import b64encode
def random_bucketid():
    """Generates a random text_typeing for a bucket ID"""
    return b64encode(os.urandom(12), b":_").decode("ascii")

def first_seen(o):
    
    if isinstance(o, string_types):
        return dateparser.parse(o)
    return datetime(o)

class Bucket(PCDict):
    """
    namedtuple('Bucket', 'id threshold total top_reports first_seen')
    Data class for buckets. Contains two identifiers:
     - id: The bucket's ID;
     - total: how many reports are currently in the bucket.
    """
    canonical_fields = {
        'id': {
            'type': text_type,
            'converter': text_type,
        },
        'threshold': {
            'type': Threshold,
            'converter': Threshold,
        },
        'first_seen': {
            'type': datetime,
            'converter': first_seen,
        },
        'total': {
            'type': int,
            'converter': int,
         },
    }
        
    def __init__(self, *args, **kwargs):
        super(Bucket, self).__init__(*args, **kwargs)
        assert 'id' in self
        assert 'threshold' in self
    
    @classmethod
    def new(cls, threshold, **kwargs):
        kwargs['threshold'] = threshold
        assert 'id' not in kwargs
        kwargs['id'] = random_bucketid()
        return Bucket(**kwargs)

class TopMatch(FixedPCDict):
    canonical_fields = {
        'report_id': {
            'type': text_type,
            'converter': text_type,
        },
        'score': {
            'type': float,
            'converter': float,
        },
        'project': {
            'type': Project,
            'converter': Project,
        },
    }

class Buckets(object):
    _od = None
    
    """Proxy for OrderedDict"""
    def __init__(self, *args, **kwargs):
        self._od = OrderedDict()
        d = OrderedDict(*args, **kwargs)
        for k, v in d.items():
            self._od[k] = v
        
    def __getattr__(self, a):
        return getattr(self._od, a)

    def __setitem__(self, k, v):
        if k == 'top_match':
            if not (isinstance(v, TopMatch) or v is None):
                v = TopMatch(v)
        else:
            if not isinstance(k, Threshold):
                k = Threshold(k)
            if not (isinstance(v, Bucket) or v is None):
                v = Bucket(v)
            if v is not None:
                assert v.threshold == k
        return self._od.__setitem__(k, v)

    def __getitem__(self, k):
        return self._od.__getitem__(k)

    def __delitem__(self, k):
        return self._od.__delitem__(k)

    def __eq__(self, other):
        if isinstance(other, Buckets):
            return self._od.__eq__(other._od)
        else:
            return self._od.__eq__(other)

    def copy(self, *args, **kwargs):
        new = Buckets()
        new._od = self._od.copy()
        return new
    
    def keys(self):
        return self._od.keys()

    def iterkeys(self):
        return self._od.iterkeys()

    def __iter__(self):
        return self._od.__iter__()
    

    def json_serializable(self):
        d = OrderedDict()
        for k, v in self._od.items():
            k = text_type(k)
            d[k] = v
        return d

    def create(self):
        for k, v in self._od.items():
            if isinstance(k, Threshold):
                if v is None:
                    self[k] = Bucket.new(k)
        
