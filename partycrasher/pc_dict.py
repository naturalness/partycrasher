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
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

import sys
from copy import copy, deepcopy

from six import PY2, PY3
if PY3:
    from collections.abc import MutableMapping, MutableSequence
elif PY2:
    from collections import MutableMapping, MutableSequence
    
class Dict(dict):
    pass

class PCDict(MutableMapping):
    """
    Proxy object for a dictionary adding some canonicalization features
    to ensure consistency.
    """

    synonyms = {}
    
    canonical_fields = {}
    
    def __init__(self, *args, **kwargs):
        if (len(args) == 1):
            assert len(kwargs) == 0
            if isinstance(args[0], PCDict):
                self._d = copy(args[0]._d)
                return self
            elif isinstance(args[0], dict):
                d = dict(args[0])
            else:
                raise TypeError("Expected %s but got %s" % 
                                (PCDict, repr(args[0])))
        d = dict(*args, **kwargs)
        self._d = Dict()
        for k, v in d.items():
            self[k] = v
    
    def __eq__(self, other):
        if not isinstance(other, PCDict):
            return False

    def __getitem__(self, key):
        if key in self.synonyms:
            return self._d.__getitem__(synonyms[key])
        else:
            return self._d.__getitem__(key)

    def __setitem__(self, key, val):
        assert key not in self.__dict__
        # Translates key synonyms to their "canonical" key.
        synonyms = self.synonyms

        # First force strings to be unicoded
        if isinstance(key, bytes):
            key = key.decode(encoding='utf-8', errors='replace')
            
        # Now do conversions.
        if key in synonyms:
            key = synonyms[key]
        
        if key in self.canonical_fields:
            # Check if the value has the type we require.
            if isinstance(val, self.canonical_fields[key]['type']):
                # It's the right type. No need to convert, just set.
                return self._d.__setitem__(key, val)
            else:
                # Coerce to the required type.
                if self.canonical_fields[key]['converter'] is not None:
                    return self._d.__setitem__(key,
                        self.canonical_fields[key]['converter'](val))
                else:
                    raise ValueError(key + " must be of type " +
                             self.canonical_fields[key]['type'].__name__)
        else:
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
    
    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        elif '_d' in self.__dict__ and k in self._d:
            return self._d[k]
        else:
            raise AttributeError(k)
    
    def __setattr__(self, k, v):
        if '_d' in self.__dict__:
            assert k not in self.__dict__['_d']
        return super(PCDict, self).__setattr__(k, v)
    
    def set_d(self, d):
        if not isinstance(d, Dict):
            d = Dict(d)
        self._d = d

class PCList(MutableSequence):
  
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
            k: v['default'] for k, v in self.canonical_fields.items()
            }
        for k, v in d.items():
            self[k] = v
