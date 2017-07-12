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

from elasticsearch import Elasticsearch, NotFoundError, TransportError, RequestError

# Some of these imports are part of the public API...
from partycrasher.crash import Crash, Stacktrace, Stackframe, pretty
from partycrasher.es.crash import ESCrash
from partycrasher.pc_exceptions import ReportNotFoundError, BucketNotFoundError
from partycrasher.threshold import Threshold
from partycrasher.config_loader import Config
from partycrasher.project import Project
from partycrasher.bucket import Bucket
from partycrasher.es.index import ESIndex

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
        self.esstore = ESStore(config.ElasticSearch)
        self.strategy_class = locate(self.config.Bucketing.Strategy.strategy)
        self.tokenization_class = locate(self.config.Bucketing.Tokenization.tokenization)
        self.tokenization = self.tokenization_class(config.Bucketing.Strategy)
        self.index = ESIndex(self.esstore,
                             self.config,
                             self.tokenization,
                             self.thresholds)
        self.index.ensure_index_exists()
        self.strategy = self.strategy_class(config=config.Bucketing.Strategy,
                                            index=self.index)
        
    
    @property
    def default_threshold(self):
        """
        Default threshould to use if none are provided.
        """
        # TODO: determine from static/dynamic configuration
        return Threshold(self.config.Bucketing.default_threshold)

    def report(self, crash, project=None, dry_run=True):
        """Factory for reports."""
        return Report(crash, project, self.strategy, dry_run)
    
    def report_bucket(self, threshold, bucket_id, project=None):
        """Factory for report buckets."""
        return ReportBucket(threshold, bucket_id, project)

    def get_bucket(self, threshold, bucket_id, 
                   project=None, from_=None, size=None):
        """
        Returns information for the given bucket.
        """
        # Coerce to a Threshold object.
        threshold = Threshold(threshold)

        query = {
            "query": { "constant_score": {
            "filter": {
                "term": {
                    "buckets." + threshold.to_elasticsearch(): bucket_id
                }
            }}},
            "sort": { "date": { "order": "desc" }},
        }
                
        if from_ is not None:
            query["from"] = from_;
            query["size"] = size;
            
        if project is not None:
            query['filter']['term']['project'] = project

        response = self.es.search(body=query, index=self.es_index)
        with open('bucket_response', 'w') as debug_file:
            print(json.dumps(response, indent=2), file=debug_file)
        
        reports_found = response['hits']['total']

        # Since no reports were found, assume the bucket does not exist (at
        # least for this project).
        if reports_found < 1:
            raise BucketNotFoundError(bucket_id)

        reports = get_reports_by_bucket(response, threshold).get(bucket_id)
        assert reports

        return Bucket(id=bucket_id,
                      project=project,
                      threshold=threshold,
                      total=reports_found,
                      top_reports=reports)

    def top_buckets(self, 
                    lower_bound, 
                    threshold=None, 
                    project=None, 
                    from_=None, 
                    size=None, 
                    upper_bound=None,
                    query_string=None):
        """
        Given a datetime lower_bound (from date), calculates the top buckets
        in the given timeframe for the given threshold (automatically
        determined if not given). The results can be tailed for a specific
        project if needed.

        Returns a list of {'doc_count': int, 'key': id} dictionaries.
        """

        if not isinstance(lower_bound, datetime):
            raise TypeError('The lower bound MUST be a datetime object.')

        # Get the default threshold.
        if threshold is None:
            threshold = self.default_threshold
        if not isinstance(threshold, Threshold):
            threshold = Threshold(threshold)

        assert threshold in self.thresholds, pretty(self.thresholds)
        
        # Filters by lower-bound by default;
        filters = [{
            "range": {
                "date": {
                    "gt": lower_bound.isoformat()
                }
            }
        }]
        
        if upper_bound is not None:
            filters[0]["range"]["date"]["lt"] = upper_bound.isoformat()

        # May filter optionally by project name.
        if project is not None:
            filters.append({
                "term": {
                    "project": project
                }
            })
        
        # this doesn't work on ES 2.3!
        if query_string is not None:
            print("Query string!", file=sys.stderr)
            filters.append({
                "query_string": {
                    "query": query_string,
                    "default_operator": "AND",
                }
            })

        # Oh, ElasticSearch! You and your verbose query "syntax"!
        query = {
            # Read this inside out:
            "aggs": {
                "top_buckets_filtered": {
                    # Filter the top buckets by date, and maybe by project.
                    "filter": {
                        "bool": { "must": filters }
                    },
                    # Get the top buckets in descending order of size.
                    "aggs": {
                        "top_buckets": {
                            "terms": {
                                "field": "buckets." + threshold.to_elasticsearch(),
                                "order": { "_count": "desc" },
                            },
                            # Get the date of the latest crash per bucket.
                            "aggs": {
                                "first_seen": {
                                    "min": {
                                        "field": "date"
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # Do not send any hits back!
            "size": 0
        }
                                    
        if size is None:
          size = 10
        
        actual_size = size
        
        if from_ is not None:
            assert from_ >= 0
            actual_size = actual_size + from_
        if size is not None:
            assert size >= 0
            (query["aggs"]["top_buckets_filtered"]["aggs"]
                  ["top_buckets"]["terms"]["size"]) = actual_size
        
        try:
            #debug(pretty(query))
            response = self.es.search(body=query, index=self.es_index)
            #debug(pretty(response))
        except RequestError as e:
            print(e.error, file=sys.stderr)
            raise e

        # Oh, ElasticSearch! You and your verbose responses!
        top_buckets = (response['aggregations']
                       ['top_buckets_filtered']
                       ['top_buckets']
                       ['buckets'])
        
        if from_ is not None:
            top_buckets = top_buckets[from_:]

        return [Bucket(id=bucket['key'], project=project, threshold=threshold,
                       total=bucket['doc_count'],
                       first_seen=bucket['first_seen']['value_as_string'],
                       top_reports=None)
                for bucket in top_buckets]

    def get_projects(self):
        """
        Returns the list of all projects found in Elasticsearch.
        """

        query = {
            "aggs": {
                "projects": {
                    "terms": {
                        "field":"project"
                    }
                }
            }
        }

        try:
            results = self.es.search(body=query, index=self.es_index)
        except TransportError:
            # Occurs when the index has just been freshly created.
            return None

        raw_projects = results['aggregations']['projects']['buckets']
        return [Project(project['key']) for project in raw_projects]

    def search(self, query_string,
               since=None,
               until=None,
               project=None, 
               from_=None, 
               size=None,
               sort=None,
               order=None):
        es_query = {
            "query": {
                "bool": { "must": [
                    { "query_string": {
                          "query": query_string,
                          # This is necessary due to how we tokenize things
                          # which is not on whitespace I.E. if the user 
                          # searched for CamelCaseThing it will be interpreted
                          # as a search for Camel AND Case AND Thing rather
                          # than Camel OR Case OR Thing
                          "default_operator": "AND", 
                      }},
                ]}
            }, 
        }
        if sort is not None:
            if order is None:
                order = "desc"
            es_query["sort"] = [{sort: {"order": order}}]
        if project is not None:
            es_query['query']['bool']['must'].append({
                "term": {
                    "project": project
                }
            });
        if (since is not None) or (until is not None):
            date_bounds = {}
            if since is not None:
                date_bounds['gt'] = since.isoformat()
            if until is not None:
                date_bounds['lt'] = until.isoformat()
            es_query['query']['bool']['must'].append({
                "range": {
                    "date": date_bounds
                }
            });
        if from_ is not None:
            es_query["from"] = from_;
        if size is not None:
            es_query["size"] = size;
        try:
            r = self.es.search(index=self.es_index, body=es_query)
        except RequestError as e:
            # TODO: use logger
            print(e.info, file=sys.stderr)
            raise
        except TransportError as e:
            # TODO: use logger
            print(e.info, file=sys.stderr)
            raise

        raw_hits = r['hits']['hits']
        #print(json.dumps(raw_hits, indent=2), file=sys.stderr)
        
        results = []

        for hit in raw_hits:
            report = hit['_source']
            crash = Crash(report)
            results.append(crash)

        return results
     


def get_reports_by_bucket(response, threshold):
    """
    Returns a dictionary mapping bucket_id => reports, from the ElasticSearch response.
    """
    buckets = defaultdict(list)

    raw_hits = response['hits']['hits']

    for hit in raw_hits:
        report = hit['_source']
        crash = Crash(report)
        bucket_id = crash.get_bucket_id(threshold)
        buckets[bucket_id].append(crash)

    return dict(buckets)


