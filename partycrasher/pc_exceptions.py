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

from copy import copy
from os import linesep
from elasticsearch import TransportError
import sys

class PartyCrasherError(Exception):
    """An error occured within PartyCrasher."""
    http_code = 500
    
    def __init__(self, message=None, **kwargs):
        self.__dict__.update(kwargs)
        if message is None:
            super(PartyCrasherError, self).__init__()
        else:
            super(PartyCrasherError, self).__init__(message)
    
    def get_extra(self):
        extra = dict(self.__dict__)
        #del extra['args']
        extra['description'] = self.__class__.__doc__
        return extra

class IdenticalReportError(PartyCrasherError):
    """Attempted to ingest a database ID more than once."""
    http_code = 409
    
    def __init__(self, report, **kwargs):
        message = ("Attempted to add an identical report with id %s" 
                   % report['database_id'])
        super(IdenticalReportError, self).__init__(message, **kwargs)
        self.report = report

class ReportNotFoundError(PartyCrasherError):
    """A crash could not be found."""
    http_code = 404
    
    def __init__(self, database_id, **kwargs):
        message = "Couldn't find the report with ID: %s" % database_id
        super(ReportNotFoundError, self).__init__(message, **kwargs)
        self.database_id = database_id
        
class MissingBucketError(PartyCrasherError):
    """A matching crash is missing bucket information for a threshold. This usually happens if the config changed."""
    http_code = 500

class BucketNotFoundError(PartyCrasherError):
    """A bucket could not be found."""
    http_code = 404
    
    def __init__(self, bucket_id, threshold, **kwargs):
        message = "The bucket with threshold %s and id %s could not be found." % (
                threshold,
                bucket_id)
        super(BucketNotFoundError, self).__init__(message)
        self.bucket_id = bucket_id
        self.threshold = threshold

class BadKeyNameError(PartyCrasherError):
    """Invalid key-value pair in crash data. Keys must be alphanumeric (including underscores)."""
    http_code = 400
    
    def __init__(self, key_name, **kwargs):
        message = "Bad key name: %s" % key_name
        super(BadKeyNameError, self).__init__(message)
        self.key_name = key_name

class BadProjectNameError(PartyCrasherError):
    """Invalid project name in crash data. Project names must be alphanumeric (including underscores)."""
    http_code = 400
    
    def __init__(self, project_name, **kwargs):
        message = "Bad project name: %s" % project_name
        super(BadProjectNameError, self).__init__(message)
        self.project_name = project_name

class BadTypeNameError(PartyCrasherError):
    """Invalid type in crash data. Types must be alphanumeric (including underscores)."""
    http_code = 400
    
    def __init__(self, type_name, **kwargs):
        message = "Bad type name: %s" % type_name
        super(BadTypeNameError, self).__init__(message)
        self.type_name = type_name

class ProjectMismatchError(PartyCrasherError):
    """Project specified in the API didn't match the project in the crash data. """
    http_code = 400
    
    def __init__(self, project, crash, **kwargs):
        message = "Project %s didn't match project %s in crash." % (project, crash['project'])
        super(ProjectMismatchError, self).__init__(message)
        self.project = project
        self.crash = crash

class NoProjectSpecifiedError(ProjectMismatchError):
    """No project specified in the API."""
    http_code = 400

class BadDateError(PartyCrasherError):
    """
    Supported formats are: ISO 8601 timestamps and relative dates
    accepted by the dateparser library. Refer to the documentation
    for the dateparser library for more information.
    https://dateparser.readthedocs.io/
    """
    http_code = 400
    
    def __init__(self, date, **kwargs):
        message = ('Could not understand date format for '
                       '%s.' % repr(date))
        super(PartyCrasherError, self).__init__(message, **kwargs)
        self.date=date

class ESError(PartyCrasherError):
    """
    ElasticSearch returned an unexpected/unhandled error.
    """
    def __init__(self, ex, **kwargs):
        (t, v, tb) = sys.exc_info()
        message = ('ElasticSearch Exception: '
                       '%s.' % str(ex))
        super(PartyCrasherError, self).__init__(message, **kwargs)
        self.original_traceback = tb
        self.original_type = repr(t)
        self.original_value = repr(v)
        if isinstance(ex, TransportError):
            self.es_status_code = ex.status_code
            self.es_error = ex.error
            self.es_info = ex.info
            self.es_description = str(ex)
            
