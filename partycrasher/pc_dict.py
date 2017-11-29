#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from __future__ import print_function

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

import sys
from copy import copy, deepcopy

from six import PY2, PY3, string_types, text_type
if PY3:
    from collections.abc import (
        MutableMapping, MutableSequence, Mapping, Sequence)
elif PY2:
    from collections import (
        MutableMapping, MutableSequence, Mapping, Sequence)

from frozendict import frozendict

from partycrasher.pc_type import PCType, key_type
    
class PCDict(MutableMapping):
    """
    Proxy object for a dictionary adding some canonicalization features
    to ensure consistency.
    """
    
    __slots__ = ('_d','frozen')

    synonyms = {}
    
    canonical_fields = {}
    
    default_dict_type = dict
    default_list_type = Sequence
    frozen_dict_type = frozendict
    frozen_list_type = tuple
    
    def __init__(self, *args, **kwargs):
        self.frozen = False
        if (len(args) == 1):
            assert len(kwargs) == 0
            if isinstance(args[0], PCDict):
                d = args[0]._d
            elif isinstance(args[0], dict):
                d = args[0]
            else:
                raise TypeError("Expected %s but got %s" % 
                                (PCDict, repr(args[0])))
        else:
            d = dict(*args, **kwargs)
        self._d = dict()
        for k, v in d.items():
            self[k] = v
    
    def __eq__(self, other):
        if not isinstance(other, PCDict):
            return False
        return self._d.__eq__(other._d)

    def __getitem__(self, key):
        if key in self.synonyms:
            return self._d.__getitem__(synonyms[key])
        else:
            return self._d.__getitem__(key)
    
    def __setitem__(self, key, val):
        # Now do conversions.
        if key in self.synonyms:
            key = self.synonyms[key]
        
        if key in self.canonical_fields:
            try:
                val = self.canonical_fields[key](val)
            except ValueError as e:
                raise ValueError(
                    str(e) + " Key " + str(key) + " Value " + str(val)
                    )
            return self._d.__setitem__(key, val)
        else:
            key = key_type(key)
        return self._d.__setitem__(key, val)

    def __delitem__(self, key):
        return self._d.__delitem__(key)

    def __iter__(self):
        return self._d.__iter__()
      
    def __len__(self):
        return self._d.__len__()
      
    def as_dict(self):
        return self._d
    
    def __copy__(self):
        """Implements a shallow copy operation. Note that this will call __init__, so it will reconvert everything."""
        return self.__class__(self._d)
        
    def __deepcopy__(self, memo):
        return self.__class__(deepcopy(self._d, memo))
    
    def set_d(self, d):
        self._d = d
    
    def keys(self):
        return self._d.keys()
    
    def freeze(self):
        for k, v in self._d.items():
            if (isinstance(v, self.default_list_type)
                and not isinstance(v, string_types)
                ):
                self._d[k] = self.frozen_list_type(v)
            elif isinstance(v, self.default_dict_type):
                self._d[k] = self.frozen_dict_type(v)
        self._d = frozendict(self._d)
        self.frozen = True
    
    def as_hashable(self):
        return tuple(self._d.items())
    
    def __hash__(self):
        return hash(self.as_hashable())
    
    def check(self):
        for k, v in self._d.items():
            if k in self.canonical_fields:
                assert self.canonical_fields[k].checker(v)

class PCList(MutableSequence):
    
    __slots__ = ('_l',)
  
    member_type = None
    member_converter = None
    
    def conv(self, item):
        if isinstance(item, self.member_type):
            return item
        else:
            return self.member_converter(item)
    
    def __init__(self, *args):
        self._l = [self.conv(i) for i in list(*args)]
        
    def __getitem__(self, i):
        return self._l.__getitem__(i)
    
    def __setitem__(self, i, v):
        return self._l.__setitem__(i, self.conv(v))
    
    def __delitem__(self, i):
        return self._l.__delitem__(i)
    
    def __len__(self):
        return self._l.__len__()
    
    def insert(self, i, v):
        return self._l.insert(i, self.conv(v))
    
    def __copy__(self):
        return self.__class__(copy(self._l))
        
    def __deepcopy__(self, memo):
        return self.__class__(deepcopy(self._l, memo))

class FixedPCDict(PCDict):
    def __init__(self, *args, **kwargs):
        super(FixedPCDict, self).__init__(*args, **kwargs)
        for k in self.canonical_fields:
            if not k in self:
                raise ValueError("Missing keyword argument " + k)
    
    def __setitem__(self, k, v):
        if k not in self.canonical_fields:
            raise KeyError(k)
        return super(FixedPCDict, self).__setitem__(k, v)

    def __delitem__(self, k):
        raise NotImplementedError

class PCDefaultDict(PCDict):
    def __init__(self, *args, **kwargs):
        d = dict(*args, **kwargs)
        self._d = {
            k: v.default for k, v in self.canonical_fields.items()
            }
        for k, v in d.items():
            self[k] = v
