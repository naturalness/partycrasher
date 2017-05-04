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

from collections import namedtuple, OrderedDict

class Bucket(namedtuple('Bucket', 'id project threshold total top_reports first_seen')):
    """
    Data class for buckets. Contains two identifiers:
     - id: The bucket's ID;
     - total: how many reports are currently in the bucket.
    """

    def to_dict(self, *args, **kwargs):
        """
        Converts the current object into a dictionary;
        Any arguments are treated as in the `dict` constructor.
        """
        kwargs.update(self._asdict())
        for arg in args:
            kwargs.update(arg)

        # HACK: remove empty top_reports, first_seen.
        if kwargs['top_reports'] is None:
            del kwargs['top_reports']

        if kwargs['first_seen'] is None:
            del kwargs['first_seen']

        return kwargs


class Buckets(object):
    """Proxy for OrderedDict"""
    def __init__(self, *args, **kwargs):
        self._od = OrderedDict(*args, **kwargs)

    def __getattr__(self, a):
        return getattr(self._od, a)

    def __setitem__(self, *args, **kwargs):
        return self._od.__setitem__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._od.__getitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self._od.__delitem__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, Buckets):
            return self._od.__eq__(other._od)
        else:
            return self._od.__eq__(other)

    def copy(self, *args, **kwargs):
        new = Buckets()
        new._od = self._od.copy()
        return new
    
    def keys(self, *args, **kwargs):
        return self._od.keys(*args, **kwargs)

    def iterkeys(self, *args, **kwargs):
        return self._od.iterkeys(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self._od.__iter__(*args, **kwargs)

    # TODO: automatically convert keys of wrong type to Threshold
