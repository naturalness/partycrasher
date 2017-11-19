#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016, 2017 Joshua Charles Campbell

#  This program is free software you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import print_function

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

from types import FunctionType
import re

from six import PY2, PY3, string_types, text_type
import dateparser
import datetime
from collections import Iterable

from partycrasher.pc_exceptions import BadKeyNameError
from partycrasher.pc_encoder import PCEncoder

class PCType(object):
    __slots__ = (
        'checker',
        'converter',
        'jsonable',
        'jsonify',
        'default'
    )
    
    def _cant_jsonify(self, v):
        raise NotImplementedError(
            "can't convert " + checker.__name__ + " to jsonifyalbe type"
            )
    
    def _cant_jsonable(self, v):
        return False
    
    def _call_jsonify(self, v):
        return v.jsonify(v)
    
    def __init__(
        self,
        checker,
        converter=None,
        nullable=True,
        jsonify=None,
        default=None
        ):
        if type(checker) is FunctionType:
            self.checker = checker
        else:
            self.checker = lambda v: isinstance(v, checker)
        self.converter = converter
        self.default = default
        if jsonify is not None:
            self.jsonify = jsonify
            self.jsonable = self.checker
            PCEncoder.types.append(self)
        elif hasattr(checker, 'jsonify'):
            self.jsonify = self._call_jsonify
            self.jsonable = self.checker
        else:
            self.jsonify = self._cant_jsonify
            self.jsonable = self._cant_jsonable
        return
        
    def single(self, value):
        if value is None:
            raise ValueError("Tried to coerce None")
        elif self.checker(value):
            return value
        else:
            if self.converter is None:
                raise ValueError("Value is type %s which is unacceptable"
                                 % (type(value).__name__))
            value = self.converter(value)
            assert self.checker(value)
            return value
        assert False

    __call__ = single
    
class PCMaybeType(PCType):
    __slots__ = tuple()

    def single(self, value):
        if value is None:
            return value
        elif self.checker(value):
            return value
        else:
            if self.converter is None:
                raise ValueError("Value is type %s which is unacceptable"
                                 % (type(value).__name__))
            value = self.converter(value)
            assert self.checker(value)
            return value

    __call__ = single

class PCMultiType(PCType):
    __slots__ = tuple()
    
    def multiple(self, value):
        if value is None:
            return value
        elif isinstance(value, Iterable):
            if len(value) == 0:
                return None
            else:
                return [self.single(i) for i in value]
        elif isinstance(value, string_types):
            return [self.single(i) for i in value.split(',')]
        else:
            return [self.single(value)]

    __call__ = multiple

good_key = re.compile('([\w_-]+)$')

def key_converter(key):
    if not isinstance(key, string_types):
        raise BadKeyNameError(repr(key))
    m = good_key.match(key)
    if m is None:
        raise BadKeyNameError(key)
    if m.group(1) != key:
        raise BadKeyNameError(key)
    return key

def key_checker(key):
    key_converter(key)
    return True

key_type = PCType(checker=key_checker, converter=key_converter)

maybe_key = PCMaybeType(checker=key_checker, converter=key_type)

mustbe_int = PCType(checker=int, converter=int)

maybe_int = PCMaybeType(checker=int, converter=int)

mustbe_string = PCType(checker=string_types, converter=text_type)

maybe_string = PCMaybeType(checker=string_types, converter=text_type)

def parse_utc_date(s):
    return dateparser.parse(s, settings={'TIMEZONE': 'UTC',
                                         'RETURN_AS_TIMEZONE_AWARE': False})
def deparse_utc_date(d):
    return d.isoformat()

mustbe_date = PCType(
    checker=datetime.datetime,
    converter=parse_utc_date,
    jsonify=deparse_utc_date
    )

maybe_date = PCMaybeType(
    checker=datetime.datetime,
    converter=parse_utc_date,
    )

mustbe_float = PCType(checker=float, converter=float)


