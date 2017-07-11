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

class PartyCrasherError(Exception):
    http_code = 500
    description = "An error occured within PartyCrasher."
    
    def __init__(self, message):
        self.message = message
        super(PartyCrasherError, self).__init__(message)
        
    def get_extra(self):
        return {}

class IdenticalReportError(PartyCrasherError):
    http_code = 409
    description = "Attempted to ingest a database ID more than once."
    """
    The second argument must be the crash
    """
    def __init__(self, report, message=None):
        if message is None:
            message = "Attempted to add an identical report with id %s" % report['database_id']
        super(IdenticalReportError, self).__init__(message)
        self.report = report

    def get_extra(self):
        return {'report':  self.report}

class ReportNotFoundError(PartyCrasherError):
    http_code = 404
    description = "A crash could not be found."
    
    def __init__(self, database_id, message=None):
        if message is None:
            message = "Couldn't find the report with ID: %s" % database_id
        super(ReportNotFoundError, self).__init__(message)
        self.database_id = database_id
        
    def get_extra(self):
        return {'database_id':  self.database_id}

class MissingBucketError(PartyCrasherError):
    http_code = 500
    description = "A matching crash is missing bucket information for a threshold. This usually happens if the config changed."

class BucketNotFoundError(PartyCrasherError):
    http_code = 404
    description = "A bucket could not be found."
    
    def __init__(self, bucket_id, threshold, message=None):
        if message is None:
            message = "The bucket with threshold %s and id %s could not be found." % (
                threshold,
                bucket_id)
        super(BucketNotFoundError, self).__init__(message)
        self.bucket_id = bucket_id
        self.threshold = threshold

    def get_extra(self):
        return {'bucket_id': self.bucket_id,
                'threshold': self.threshold}

class BadKeyNameError(PartyCrasherError):
    http_code = 400
    description = "Invalid key-value pair in crash data. Keys cannot contain period '.' characters."
    
    def __init__(self, key_name, message=None):
        if message is None:
            message = "Bad key name: %s" % key_name
        super(BadKeyNameError, self).__init__(message)
        self.key_name = key_name

    def get_extra(self):
        return {'key_name': self.key_name}
