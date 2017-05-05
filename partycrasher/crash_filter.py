#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

from __future__ import print_function, division

import os
import json
import uuid
import time
import sys
import re
import traceback
import math
import copy
from datetime import datetime

from partycrasher.crash import Crash, Buckets, pretty
from partycrasher.es_crash import ESCrash, ESCrashEncoder
from partycrasher.threshold import Threshold
from partycrasher.pc_dict import PCDict, PCList
from partycrasher.project import Project

from six import string_types

class CrashFilter(object):
    
    def __init__(self,
                 remove_fields=[],
                 keep_fields=None):
        """ Keep everything in keep except the things in remove,
            if keep is None, keep everything except the things in remove.
            Always removes datetime fields.
        """
        self.remove_fields = set([re.compile(p) for p in remove_fields])
        if keep_fields is None:
            self.keep_fields = None
        else:
            self.keep_fields = set([re.compile(p) for p in keep_fields])
            assert (len(self.keep_fields)>0)
            
    def keep(self, field):
        if self.keep_fields is None:
            pass
        else:
            k = False
            for p in self.keep_fields:
                if p.search(field) is not None:
                    k = True
            if not k:
                return False
        for p in self.remove_fields:
            if p.search(field) is not None:
                return False
        return True
        
    def filter_dict(self, prefix, d):
        newdict = {}
        for k, v in d.items():
            assert "." not in k
            if isinstance(v, dict) or isinstance(v, PCDict):
                fi = self.filter_dict(prefix + "." + k, v)
                if len(fi) > 0:
                    newdict[k] = fi
            elif isinstance(v, list) or isinstance(v, PCList):
                fi = self.filter_list(prefix + "." + k, v)
                if len(fi) > 0:
                    newdict[k] = fi
            elif isinstance(v, string_types) or isinstance(v, int):
                if self.keep(prefix + "." + k):
                    newdict[k] = v
            elif isinstance(v, datetime):
                pass
            elif v is None:
                pass
            else:
                raise NotImplementedError("Crash filter can't handle "
                  + v.__class__.__name__ + " in " + prefix + " . " + k)
        return newdict
      
    def filter_list(self, prefix, l):
        newlist = []
        for i in l:
            if isinstance(i, dict) or isinstance(i, PCDict):
                fi = self.filter_dict(prefix, i)
                if len(fi) > 0:
                    newlist.append(fi)
            elif isinstance(i, list) or isinstance(i, PCList):
                fi = self.filter_list(prefix, i)
                if len(fi) > 0:
                    newlist.append(fi)
            elif isinstance(i, string_types) or isinstance(i, int):
                if self.keep(prefix):
                    newlist.append(i)
            elif isinstance(i, datetime):
                pass
            elif i is None:
                pass
            else:
                raise NotImplementedError("Crash filter can't handle "
                  + v.__class__.__name__ + " in " + prefix)
        return newlist
    
    def filter_crash(self, crash):
        newcrash = {}
        
        for k, v in crash.items():
            assert "." not in k
            if isinstance(v, dict) or isinstance(v, PCDict):
                newdict = self.filter_dict(k, v)
                if len(newdict) > 0:
                    newcrash[k] = newdict
            elif isinstance(v, list) or isinstance(v, PCList):
                newlist = self.filter_list(k, v)
                if len(newlist) > 0:
                    newcrash[k] = newlist
            elif isinstance(v, string_types) or isinstance(v, int):
                if self.keep(k):
                    newcrash[k] = v
            elif isinstance(v, datetime):
                pass # always filter dates
            elif isinstance(v, Buckets):
                pass # always filter dates
            elif isinstance(v, Project):
                newcrash[k] = v # always keep project
            elif v is None:
                pass
            else:
                raise NotImplementedError("Crash filter can't handle "
                  + v.__class__.__name__ + " in " + k)
        return newcrash         