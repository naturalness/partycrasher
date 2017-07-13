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

from __future__ import print_function

import sys
import json
import math
from datetime import datetime
from collections import defaultdict
from pydoc import locate
from runpy import run_path

from six import string_types

# Some of these imports are part of the public API...
from partycrasher.crash import Crash, Stacktrace, Stackframe, pretty
from partycrasher.es.crash import ESCrash
from partycrasher.pc_exceptions import ReportNotFoundError, BucketNotFoundError
from partycrasher.threshold import Threshold
from partycrasher.config_loader import Config
from partycrasher.project import Project
from partycrasher.es.store import ESStore
from partycrasher.es.index import ESIndex
from partycrasher.report import Report
from partycrasher.report_search import ReportBucket, ReportSearch
from partycrasher.bucket_search import BucketSearch
from partycrasher.pc_dict import PCDict

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

class PartyCrasher(object):
    """Public API root and config file loader."""
    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.thresholds = list(
            map(Threshold, self.config.Bucketing.thresholds)
            )
        self.esstore = ESStore(self.config.ElasticSearch)
        self.strategy_class = locate(self.config.Bucketing.Strategy.strategy)
        self.tokenization_class = locate(self.config.Bucketing.Tokenization.tokenization)
        self.tokenization = self.tokenization_class(self.config.Bucketing.Tokenization)
        self.index = ESIndex(self.esstore,
                             self.config,
                             self.tokenization,
                             self.thresholds)
        self.index.ensure_index_exists()
        self.strategy = self.strategy_class(config=self.config.Bucketing.Strategy,
                                            index=self.index)
    
    @property
    def search_config(self):
        """Pull configuration details needed for search and fix it up."""
        fixed_summary_fields = self.config.UserInterface.fixed_summary_fields
        fixed_summary_fields["project"] = "Project"
        return PCDict(
            fixed_summary_fields=fixed_summary_fields)
        
    @property
    def default_threshold(self):
        """
        Default threshould to use if none are provided.
        """
        # TODO: determine from static/dynamic configuration
        return Threshold(self.config.Bucketing.default_threshold)

    def report(self, crash, project, dry_run=True):
        """Factory for reports."""
        return Report(crash, project, self.strategy, self.thresholds, self.index, dry_run)
    
    def report_bucket(self, threshold, **kwargs):
        """Factory for report buckets."""
        threshold = Threshold(threshold)
        assert threshold in self.thresholds
        return ReportBucket(index=self.index, 
                            config=self.search_config,
                            threshold=threshold, 
                            **kwargs)
    
    def bucket_search(self, threshold, **kwargs):
        """Factory for groups of report buckets."""
        threshold = Threshold(threshold)
        assert threshold in self.thresholds, (threshold)
        return BucketSearch(index=self.index, 
                            config=self.search_config,
                            threshold=threshold, 
                            **kwargs)
    
    def report_search(self, **kwargs):
        """Factory for report buckets."""
        return ReportSearch(index=self.index, 
                            config=self.search_config,
                            **kwargs)

