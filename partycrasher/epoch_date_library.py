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

import datetime
import re
import time

import dateutil.parser


class InvalidDateError(ValueError):
    """
    Raised when a date appears invalid.
    """

class DateParsingError(ValueError):
    """
    Raised when a date could not be parsed.
    """

def milliseconds_since_epoch(then):
    """
    Given an datetime object, returns the milliseconds since the Unix epoch,
    in the UTC timezone. This scheme should be used extensively and consistently
    for all dates in the database.

    http://stackoverflow.com/a/8160307
    """
    return int(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)


def parse_absolute_or_relative_time(text):
    """
    Returns a `datetime` object or raises:

     * DateParsingError -- could not rase
     * InvalidDateError

    """

    try:
        value = parse_absolute_date(text) or parse_relative_date(text)
    except ValueError as e:
        raise InvalidDateError(e.message)

    if value is None:
        raise DateParsingError()
    else:
        return value


def parse_absolute_date(text):
    """
    Returns a `datetime` object if succesfully parsed date.
    Returns None if the object cannot be parsed.

    May still return ValueError if datetime is unsuccessful.
    """

    try:
        return dateutil.parser.parse(text)
    except ValueError as e:
        if e.message.startswith('Unknown string format'):
            # Unknown string format means parsing failed
            return None
        else:
            # Something with datetime failed!
            raise e


def parse_relative_date(text):
    """
    Returns a datetime object, or returns None.
    """
    now = datetime.datetime.utcnow()

    matches = re.match(r'''
        # Matches 'yesterday'
        yesterday |

        # Matches 'last {whatever}'
        last-(week|month|year) |

        # If I really want to be pointless, I could add "score" and
        # "fortnight" and other antiquated measures of age

        # Matches '{some} {somethings} ago'
        (an?|\d+)-(minute|hour|day|week|month|year)s?-ago
    ''', text, re.VERBOSE)

    if not matches:
        return None
    else:
        raise NotImplementedError(matches)
