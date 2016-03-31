#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (C) 2016  Eddie Antonio Santos <easantos@ualberta.ca>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from decimal import Decimal

# Python 2/3 non-sense.
try:
    unicode
except NameError:
    StringTypes = (str,)
else:
    StringTypes = (str, unicode)


class Threshold(object):
    """
    A wrapper for a bucket threshold value. Ensures proper serialization
    between ElasticSearch and the JSON API endpoints.
    """
    __slots__ = '_value'

    def __init__(self, value):
        if isinstance(value, Threshold):
            assert isinstance(value._value, Decimal)
            # Clone the other Threshold.
            self._value = value._value
            return
        elif isinstance(value, StringTypes):
            value = value.replace('_', '.')

        self._value = Decimal(value)

    def __str__(self):
        result = str(self._value)
        assert '_' not in result
        # Ensure that rounded values are always displayed with at least one
        # decimal, for aesthetics.
        if '.' not in result:
            return result + '.0'
        return result

    def __repr__(self):
        return "Threshold('" + str(self) + "')"

    def to_float(self):
        """
        Convert the threshold to a floating point number, for comparisons.
        Note that this should NOT be converted back to a threshold, as there
        may be a loss of data by doing the round trip.
        """
        return float(self._value)

    def __getattr__(self, attr):
        # Delegate everything (i.e, comparisons) to the actual Threshold
        # value.
        return getattr(self._value, attr)
    
    def __hash__(self):
        return self._value.__hash__()
    
    def __eq__(self, otter):
        if not isinstance(otter, Threshold):
            return False
        return self._value == otter._value

    def to_elasticsearch(self):
        """
        Converts the threshold to a string, suitable for serialization as an
        ElasticSearch field name. Note that full stops ('.') are verbotten in
        ElasticSearch field names.
        """
        str_value = str(self)
        assert isinstance(self._value, Decimal)
        assert str_value.count('.') == 1, 'Invalid decimal number'
        return str_value.replace('.', '_')



