#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016, 2017 Joshua Charles Campbell

#  This program is free software; you can reditext_typeibute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is ditext_typeibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import partycrasher
from partycrasher.context import Context
from partycrasher.bucket import Bucket
from partycrasher.crash import pretty

# These imports are all the public API
from partycrasher.api.report import Report
from partycrasher.api.search import Search, Results
from partycrasher.api.report_bucket import ReportBucket
from partycrasher.api.report_threshold import ReportThreshold
from partycrasher.api.report_project import ReportProject
from partycrasher.api.projects import Projects
from partycrasher.api.thresholds import Thresholds

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

class PartyCrasher(object):
    """Public API root and config file loader."""
    def __init__(self, config_file=None):
        self.context = Context(config_file)
        self.null_search = Search(context=self.context)
        
    @property
    def config(self):
        return self.context.config
    
    @property
    def default_threshold(self):
        return self.context.default_threshold
        
    def report(self, crash, project=None, dry_run=True, explain=False):
        """Factory for reports."""
        return Report(search=self.null_search,
                      crash=crash,
                      project=project, 
                      dry_run=dry_run,
                      explain=explain
                      )
    
    def report_bucket(self, 
                      threshold,
                      bucket_id,
                      from_=None, size=None, **kwargs):
        """Factory for report buckets."""
        assert threshold is not None
        assert bucket_id is not None
        search = Search(context=self.context, **kwargs)
        bucket = Bucket(threshold=threshold, id=bucket_id)
        return ReportBucket(search=search, result=bucket, from_=from_, size=size)
    
    def report_threshold(self,
                         threshold,
                         from_=None, size=None,
                         **kwargs):
        search = Search(context=self.context, 
                        threshold=threshold,
                        **kwargs)
        return ReportThreshold(
            search=search, 
            result=threshold, 
            from_=from_, size=size)
    
    def report_project(self,
                         project,
                         from_=None, size=None,
                         **kwargs):
        search = Search(context=self.context, 
                        project=project,
                        **kwargs)
        return ReportProject(
            search=search, 
            project=project, 
            from_=from_, size=size)
    

    def bucket_search(self, threshold, **kwargs):
        """Factory for groups of report buckets."""
        threshold = Threshold(threshold)
        assert threshold in self.context.thresholds, (threshold)
        return BucketSearch(context=self.context,
                            threshold=threshold, 
                            **kwargs)
    
    def report_search(self, from_=None, size=None, **kwargs):
        """Factory for report buckets."""
        search = Search(context=self.context, **kwargs)
        return Results(search=search, from_=from_, size=size)
    
    @property
    def projects(self):
        """Get the projects."""
        return Projects(self.null_search)
    
    @property
    def thresholds(self):
        """Get the thresholds."""
        return Thresholds(self.null_search)
    
    @property
    def buckets(self):
        return self.thresholds

    @property
    def reports(self):
        """Get the reports."""
        return Results(self.null_search)

    @property
    def es_store(self):
        """Get the reports."""
        return self.context.es_store

    def restify(self):
        """Force computation of dynamic properties to a dictionary."""
        d = {
            'projects': self.projects,
            'buckets': self.thresholds,
            'config': self.config,
            'reports': self.reports,
            'version': partycrasher.__version__,
            'store': self.es_store,
            'default_threshold': self.context.default_threshold
            }
        return d

    @property
    def allow_delete_all(self):
        return self.context.allow_delete_all
    
    def delete_and_recreate_index(self):
        return self.context.index.delete_and_recreate_index()
    
