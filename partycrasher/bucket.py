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
from copy import copy, deepcopy
from decimal import Decimal

from six import text_type

from partycrasher.pc_dict import PCDict, FixedPCDict
from partycrasher.pc_type import (
    PCType,
    PCMaybeType,
    mustbe_string,
    mustbe_int,
    mustbe_float,
    mustbe_date,
    key_type
    )
from partycrasher.threshold import Threshold, mustbe_threshold
from partycrasher.project import mustbe_project

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from base64 import b64encode
def random_bucketid():
    """Generates a random text_typeing for a bucket ID"""
    return b64encode(os.urandom(12), b"-_").decode("ascii")

class Bucket(PCDict):
    """
    namedtuple('Bucket', 'id threshold total top_reports first_seen')
    Data class for buckets. Contains two identifiers:
     - id: The bucket's ID;
     - total: how many reports are currently in the bucket.
    """
    __slots__ = tuple()
    
    canonical_fields = {
        'id': key_type,
        'threshold': mustbe_threshold,
        'first_seen': mustbe_date,
        'last_seen': mustbe_date,
        'total': mustbe_int,
    }
        
    #def __init__(self, *args, **kwargs):
        #super(Bucket, self).__init__(*args, **kwargs)
        #assert 'id' in self
        #assert 'threshold' in self
    
    @classmethod
    def new(cls, threshold, **kwargs):
        kwargs['threshold'] = threshold
        assert 'id' not in kwargs
        kwargs['id'] = random_bucketid()
        return Bucket(**kwargs)
    
    def jsonify(self):
        return self.as_dict()
    
mustbe_bucket = PCType(Bucket, Bucket)

maybe_bucket = PCMaybeType(Bucket, Bucket)
    
class TopMatch(FixedPCDict):
    __slots__ = tuple()

    canonical_fields = {
        'report_id': key_type,
        'score': mustbe_float,
        'project': mustbe_project,
    }
    
    def jsonify(self):
        return self.as_dict()

mustbe_top_match = PCType(TopMatch, TopMatch)

class Buckets(object):
    __slots__ = ('_od',)
    
    """Proxy for OrderedDict"""
    def __init__(self, _initial_d=None, **kwargs):
        self._od = dict()
        for k, v in kwargs.items():
            self._od[k] = v
        if _initial_d is not None:
            for k, v in _initial_d.items():
                self._od[k] = v
        #self._od = OrderedDict(sorted(self._od))
        
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
                assert v['threshold'] == k
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

    def __copy__(self):
        new = Buckets()
        new._od = self._od.__copy__()
        return new
    
    def keys(self):
        return self._od.keys()

    def iterkeys(self):
        return self._od.iterkeys()

    def __iter__(self):
        return self._od.__iter__()
    
    def __deepcopy__(self, memo):
        for k, v in self._od.items():
            assert not isinstance(k, Decimal)
            assert not isinstance(v, Decimal)
        new = self.__class__()
        new._od = deepcopy(self._od, memo)
        for k, v in new._od.items():
            assert not isinstance(k, Decimal)
            assert not isinstance(v, Decimal)
        return new

    def jsonify(self):
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
        
mustbe_buckets = PCType(checker=Buckets, converter=Buckets)
