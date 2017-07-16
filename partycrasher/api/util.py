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

from six import string_types

from datetime import datetime
from dateparser import parse as parse_date

from partycrasher.pc_exceptions import BadDateError
from partycrasher.threshold import Threshold
from partycrasher.project import Project
from partycrasher.bucket import Bucket

def maybe_threshold(v):
    if v is not None:
        return Threshold(v)
    else:
        return v

def maybe_bucket(v):
    if v is not None:
        return Bucket(v)
    else:
        return v

def maybe_project(v):
    if v is not None:
        return Project(v)
    else:
        return v

def maybe_int(v):
    if v is not None:
        return int(v)
    else:
        return v

def maybe_text(v):
    if v is not None:
        return int(v)
    else:
        return v

def maybe_date(v):
    if v is None:
        return v
    elif isinstance(v, datetime):
        return v
    elif isinstance(v, string_types):
        d = parse_date(v)
        if d is None:
            raise BadDateError(v)
    else:
        return v

def maybe_parse_date(s):
    if isinstance(s, datetime):
        return s
    return dateparser.parse(s.replace('-', ' '))
