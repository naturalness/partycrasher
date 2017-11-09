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

from __future__ import print_function

from six import string_types

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from copy import copy, deepcopy

from partycrasher.crash import Crash, Stacktrace, Stackframe
from partycrasher.es.crash import ESCrash
from partycrasher.context import Context
from partycrasher.pc_exceptions import ProjectMismatchError
from partycrasher.bucket import Buckets, Bucket
from partycrasher.project import Project


# python2 and six don't support enums

class Report(object):
    """Object representing the API functionality for an individual crash."""    
    
    def __init__(self,
                 search,
                 crash,
                 project=None,
                 dry_run=True,
                 explain=False,
                 saved=False,
                 ):
        self.came_from = search
        context = search.context
        self.context = context
        if isinstance(crash, string_types):
            self.crash = ESCrash(self.context.index, crash)
            self.saved = True
        elif isinstance(crash, dict):
            self.crash = Crash(crash)
            self.saved = saved
        elif isinstance(crash, ESCrash):
            self.crash = crash
            self.saved = True
        elif isinstance(crash, Crash):
            self.crash = crash
            self.saved = saved
        self.strategy = context.strategy
        self.dry_run = dry_run
        self.ran = False
        self.validate()
        self.project = project
        self.fix_project()
        self.thresholds = context.thresholds
        self.index = context.index
        self.explain = explain
        self.fix_crash()
            
    def fix_crash(self):
        if isinstance(self.crash, ESCrash):
            self.crash = self.crash.as_crash()
        from partycrasher.api.report_bucket import ReportBucket
        from partycrasher.api.report_project import ReportProject
        from partycrasher.api.report_type import ReportType
        from partycrasher.api.search import Search
        assert isinstance(self.context, Context), context.__class__.__name__

        self.crash['project'] = ReportProject(
            search=Search(context=self.context),
            project=self.crash['project'])
        self.crash['type'] = ReportType(
            search=Search(context=self.context),
            report_type=self.crash['type'])
        if 'buckets' in self.crash:
            for k, v in list(self.crash['buckets'].items()):
                if isinstance(v, Bucket):
                    self.crash['buckets'][k] = ReportBucket(
                        search=Search(context=self.context),
                        id=v.id,
                        threshold=v.threshold)
        
    def fix_project(self):
        crash_project = None
        if 'project' in self.crash:
            if isinstance(self.crash['project'], Project):
                crash_project = self.crash['project'].name
            else:
                crash_project = self.crash['project']
        if crash_project is None:
            if self.project is None:
                raise NoProjectSpecifiedError(self.project, self.crash)
            else:
                self.crash['project'] = self.project
                return self.project
        else:
            if self.project is None:
                self.project = crash_project
                return crash_project
            else: # both not none
                if crash_project != self.project:
                    raise ProjectMismatchError(self.project, self.crash)
                else:
                    return self.project
    
    def validate(self):
        """Do some extra runtime checking that should be unnecessary if the Crash class is operating correctly."""
        true_crash = self.crash
        if 'stacktrace' in true_crash:
            assert isinstance(true_crash['stacktrace'], Stacktrace)
            assert isinstance(true_crash['stacktrace'][0], Stackframe)
            if 'address' in true_crash['stacktrace'][0]:
                assert isinstance(true_crash['stacktrace'][0]['address'], string_types), (
                    "address must be a string instead of %s" 
                    % (true_crash['stacktrace'][0]['address'].__class__))
    
    def search(self, explain=None):
        """Run the search."""
        #error("Searching with explain=" + str(explain))
        if explain is not None:
            self.explain = explain
        del explain
        if not self.ran:
            if (not self.explain) and self.saved:
                raise RuntimeError("Requested search but there was no reason to search")
            self.es_result = self.strategy.query(self.crash, self.explain)
            self.ran = True
            return self.es_result
    
    def save(self):
        """Save the crash with assigned buckets to ES."""
        assert not self.dry_run
        assert not self.saved
        if 'buckets' not in self.crash:
            self.assign_buckets()
        self.crash['buckets'].create()
        saved_crash = ESCrash(crash=self.crash, index=self.index)
        assert saved_crash is not None
        self.crash = saved_crash
        self.saved = True
        return saved_crash
    
    def assign_buckets(self):
        """Assigns buckets to this crash and returns the assigned buckets."""
        assert 'buckets' not in self.crash
        self.search()
        buckets = self.strategy.matching_buckets(self.thresholds,
                                                 self.es_result)
        if 'force_bucket' in self.crash:
            warn("Warning: overriding buckets to %s with force_bucket!" % (self.crash['force_bucket']))
            for key in buckets:
                if key != 'top_match':
                    buckets[key] = self.crash['force_bucket']
        assert isinstance(buckets, Buckets)
        assert 'top_match' in buckets
        self.crash["buckets"] = buckets
        return buckets
    
    @property 
    def assigned_buckets(self):
        """Returns the buckets assigned to this crash."""
        buckets = None
        if 'buckets' not in self.crash:
            return self.assign_buckets()
        else:
            return self.crash['buckets']
    
    @property 
    def explanation(self):
        """
        Returns the explanation of why it would be bucketed now the way it would.
        This is not necessarily the original bucketing.
        """
        if self.explain:
            self.search()
            return self.es_result.explanation
        else:
            return None
    
    @property
    def auto_summary(self):
        """
        Returns the summary of theexplanation of why it would be bucketed now the way it would.
        This is not necessarily the original bucketing.
        """
        if self.explain:
            self.search()
            return self.es_result.explanation_summary
        else:
            return None
    
    @property
    def compare(self, other_report):
        """
        Returns an explanation summary comparing two reports.
        """
        raise NotImplementedError("Report comparisons not currently implemented.")
        if self.explain:
            self.search()
            return self.es_result.explanation_summary()
        else:
            return None
    
    @property
    def crash_with_termvectors(self):
        """Returns the crash with logdf information included."""
        assert self.saved
        assert isintance(self.crash, ESCrash)
        database_id = self.crash['database_id']
        response = self.es.termvectors(index=self.es_index, doc_type='crash',
                                  id=database_id,
                                  fields='stacktrace.function.whole',
                                  term_statistics=True,
                                  offsets=False,
                                  positions=False)
        
        #with open('termvectors', 'wb') as termvectorsfile:
            #print(json.dumps(response, indent=2), file=termvectorsfile)
        
        if 'stacktrace.function.whole' in response['term_vectors']:
            vectors = response['term_vectors']['stacktrace.function.whole']
            
            all_doc_count = float(vectors['field_statistics']['doc_count'])
            
            crash = self.crash.as_crash()
            
            # Sometimes there's extra functions on top of the stack for 
            # logging/cleanup/handling/rethrowing/whatever that get called 
            # after the fault but before the trace is generated, and are 
            # present for multiple crash locations. So except on the 
            # full detail page, we don't want to display them. 
            # This is for that.
            for frame in crash['stacktrace']:
                if 'function' in frame and frame['function']:
                    function = frame['function']
                    term = vectors['terms'][function]
                    relativedf = float(term['doc_freq'])/all_doc_count
                    logdf = -1.0 * math.log(relativedf, 2)
                    #print(logdf, file=sys.stderr)
                    frame['logdf'] = logdf
          
        return crash

    def restify_(self):
        assert self.project is not None
        d = {
            'report': self.crash,
            'saved': self.saved,
            }
        if self.explain:
            d['explanation'] = self.explanation
            d['auto_summary'] = self.auto_summary
        return d

    @property
    def database_id(self):
        return self.crash.database_id
