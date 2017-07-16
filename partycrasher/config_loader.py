#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2017 Joshua Charles Campbell

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
from six import string_types
from runpy import run_path
from inspect import isclass, getmembers, isroutine

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug


class Config(object):
    def __init__(self, file_path):
        self._config = run_path(file_path)
        
    def __getattr__(self, attr):
        return self._config[attr]
    
    def restify_class(self, o):
        if isclass(o):
            d = {}
            for k, v in getmembers(o):
                if '__' not in k:
                    d[k] = self.restify_class(v)
            return d
        else:
            assert (isinstance(o, dict),
                    isinstance(o, float),
                    isinstance(o, list),
                    isinstance(o, int),
                    isinstance(o, string_types)
                    ), o
            return o
    
    def restify(self):
        d = {}
        for k, v in self._config.items():
            if '__' not in k:
                x = self.restify_class(v)
                d[k] = x
        return d
