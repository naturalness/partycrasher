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


class IdenticalReportError(Exception):
    """
    Raised when a database ID is ingested more than once.

    The first argument must be the crash
    """
    def __init__(self, report):
        self.report = report

class ReportNotFoundError(KeyError):
    """
    Raised when... the crash is not found!
    """

class MissingBucketError(KeyError):
    """
    If the matching crash is missing bucket fields. This usually happens
    if the config is changed.
    """

class BucketNotFoundError(KeyError):
    """
    When a particular bucket cannot be found.
    """
