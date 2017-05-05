#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2016, 2017 Joshua Charles Campbell

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

from partycrasher.threshold import Threshold
from partycrasher.bucket import Bucket, Buckets

class ESBuckets(Buckets):
    def __init__(self, raw_buckets):
        super(ESBuckets, self).__init__()
        self.raw_buckets = raw_buckets
        for k, v in raw_buckets.items():
            threshold = Threshold(k)
            bucket = Bucket({'id': v, 'threshold': threshold})
            self[threshold] = bucket

    def __getitem__(self, threshold):
        """
        Given a crash JSON, returns the bucket field associated with this
        particular threshold.
        """
        try:
          return super(ESBuckets, self).__getitem__(threshold)
        except KeyError:
            message = ('Crash does not have an assignment for '
                      '{!s}'.format(threshold))
            # TODO: Custom exception for this?
            raise Exception(message)
