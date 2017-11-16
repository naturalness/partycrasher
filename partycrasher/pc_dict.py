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
import re

from six import PY2, PY3, string_types
if PY3:
    from collections.abc import MutableMapping, MutableSequence
elif PY2:
    from collections import MutableMapping, MutableSequence

from frozendict import frozendict
    
from partycrasher.pc_exceptions import BadKeyNameError

good = re.compile('([\w_-]+)$')
    
class PCDict(MutableMapping):
    """
    Proxy object for a dictionary adding some canonicalization features
    to ensure consistency.
    """
    
    __slots__ = ('_d',)

    synonyms = {}
    
    canonical_fields = {}
    
    def __init__(self, *args, **kwargs):
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
    
    def maybe_coerce(self, key, val):
        if self.canonical_fields[key]['converter'] is not None:
            #DEBUG(self.canonical_fields[key]['converter'])
            return (
                self.canonical_fields[key]['converter'](val))
        else:
            raise ValueError(key + " must be of type " +
                        self.canonical_fields[key]['type'].__name__)

    def __setitem__(self, key, val):
        # TODO: figure out how to fix this
        #if (not key in self._d) and hasattr(self, key):
            #raise BadKeyNameError(key)

        # Force strings to be unicoded
        if not isinstance(key, string_types):
           raise BadKeyNameError(repr(key))
            
        # Now do conversions.
        if key in self.synonyms:
            key = self.synonyms[key]
        
        if key in self.canonical_fields:
            # Check if the value has the type we require.
            if isinstance(val, self.canonical_fields[key]['type']):
                # It's the right type. No need to convert, just set.
                return self._d.__setitem__(key, val)
            elif (isinstance(val, list)
                  and self.canonical_fields[key].get('multi', False)):
                for i in range(0, len(val)):
                    if isinstance(val[i], self.canonical_fields[key]['type']):
                        continue
                    else:
                        val[i] = maybe_coerce(key, val[i])
                return self._d.__setitem__(key, val)
            else:
                # Coerce to the required type.
                return self._d.__setitem__(
                    key,
                    self.maybe_coerce(key, val)
                    )
        else:
            m = good.match(key)
            if m is None:
                raise BadKeyNameError(key)
            if m.group(1) != key:
                raise BadKeyNameError(key)
            return self._d.__setitem__(key, val)
        assert False

    def __delitem__(self, key):
        return self._d.__delitem__(key)

    def __iter__(self):
        return self._d.__iter__()
      
    def __len__(self):
        return self._d.__len__()
      
    def as_dict(self):
        return dict(self._d)
    
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
        self._d = frozendict(self._d)
    
    def as_hashable(self):
        return tuple(self._d.items())
    
    def __hash__(self):
        return hash(self.as_hashable())
    
    def check(self):
        for k, v in self._d.items():
            if k in self.canonical_fields:
                assert isinstance(v, self.canonical_fields[k]['type'])

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
            k: v['default'] for k, v in self.canonical_fields.items()
            }
        for k, v in d.items():
            self[k] = v
