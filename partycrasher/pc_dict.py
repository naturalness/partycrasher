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

import sys
if (sys.version_info > (3, 0)):
    from collections.abc import MutableMapping, MutableSequence
else:
    from collections import MutableMapping, MutableSequence

class PCDict(MutableMapping):
    """
    Proxy object for a dictionary adding some canonicalization features
    to ensure consistency.
    """

    synonyms = {}
    
    cannonical_fields = {}
    
    def __init__(self, *args, **kwargs):
        d = dict(*args, **kwargs)
        self._d = {}
        for k, v in d.items():
            self[k] = v
    
    def __eq__(self, other):
        if not isinstance(other, PCDict):
            return False
        if not other.__class__ == self.__class__:
            return False
        return (self._d == other._d)
      
    def _get(self, key):
        return self._d[key]
    
    def __getitem__(self, key):
        if key in self.synonyms:
            return self._get(synonyms[key])
        else:
            return self._get(key)

    def __setitem__(self, key, val):
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
    
    def copy(self):
        return self.__class__(self._d)

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
