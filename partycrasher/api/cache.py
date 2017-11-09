#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

import weakref

from partycrasher.api.report_threshold import ReportThreshold
from partycrasher.api.thresholds import Thresholds

cached_thresholds = weakref.WeakValueDictionary()

def cached_threshold(search):
    global cached_thresholds
    if search in cached_thresholds:
        #DEBUG("HIT")
        return cached_thresholds[search]
    else:
        #DEBUG("MISS " + repr(search))
        if search.threshold is None:
            buckets = Thresholds(search)
        else:
            buckets = ReportThreshold(search, search.threshold)
        cached_thresholds[search] = buckets
        return buckets

class WeakRefableDict(dict):
    pass
