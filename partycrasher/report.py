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

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from copy import copy, deepcopy

from partycrasher.crash import Crash
from partycrasher.es_crash import ESCrash

# python2 and six don't support enums

class Report(object):
    """Object representing the API functionality for an individual crash."""    
    
    def __init__(self, 
                 crash, 
                 strategy, 
                 dry_run=True
                 ):
        if instance(crash, string_types):
            self.crash = ESCrash(crash)
            self.saved = True
        elif isinstance(crash, dict):
            self.crash = Crash(crash)
            self.saved = False
        elif ininstance(crash, ESCrash):
            self.crash = crash
            self.saved = True
        elif ininstance(crash, Crash):
            self.crash = crash
            self.saved = False
        self.strategy = strategy
        self.dry_run = dry_run
        self.ran = False
        self.validate()
    
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
    
    def search(self, explain=False):
        """Run the search."""
        if not self.ran:
            if (not self.explain) and self.saved:
                # No reason to search...
                return None
            self.explain = explain
            self.es_result = self.strategy.query(crash, explain)
            self.ran = True
            return self.es_result
    
    def save(self):
        """Save the crash with assigned buckets to ES."""
        assert not self.dry_run
        assert not self.saved
        if 'buckets' not in self.crash:
            self.assign_buckets()
        self.crash['buckets'].create()
        saved_crash = ESCrash(crash=crash, index=self.index)
        assert saved_crash is not None
        self.saved_crash = saved_crash
        return saved_crash
    
    def assign_buckets(self):
        """Assigns buckets to this crash and returns the assigned buckets."""
        assert 'buckets' not in self.crash
        self.search()
        buckets = self.strategy.matching_buckets(self.thresholds,
                                                 self.es_result)
        if 'force_bucket' in crash:
            warn("Warning: overriding buckets to %s with force_bucket!" % (crash['force_bucket']))
            for key in buckets:
                if key != 'top_match':
                    buckets[key] = crash['force_bucket']
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
            return self.es_result.explanation()
        else:
            return None
    
    @property
    def summary(self):
        """
        Returns the summary of theexplanation of why it would be bucketed now the way it would.
        This is not necessarily the original bucketing.
        """
        if self.explain:
            self.search()
            return self.es_result.explanation_summary()
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
