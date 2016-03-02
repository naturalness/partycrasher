#!usr/bin/env python
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

import time


def milliseconds_since_epoch(then):
    """
    Given an datetime object, returns the milliseconds since the Unix epoch,
    in the UTC timezone. This scheme should be used extensively and consistently
    for all dates in the database.

    http://stackoverflow.com/a/8160307
    """
    return int(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)
