#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2016 Joshua Charles Campbell

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

from __future__ import print_function, division

import os
import json
import uuid
import time
import sys
import re
import traceback
import math
import copy
from operator import itemgetter
from sets import Set
from datetime import datetime
from elasticsearch import RequestError
from distutils.util import strtobool


from crash import Crash, Buckets, pretty
from es_crash import ESCrash, ESCrashEncoder
from threshold import Threshold

from base64 import b64encode
def random_bucketid():
    """Generates a random string for a bucket ID"""
    return b64encode(os.urandom(12), ":_")

class IndexNotUpdatedError(Exception):
    """
    When ElasticSearch has not yet propegated a required update. The solution
    to this is usually to just retry the query.
    """

class Bucketer(object):
    """
    Superclass for bucketers which require pre-existing data to work.
    The default analyzer breaks on whitespace.
    """

    def __init__(self, 
                 index=None,
                 elasticsearch=None, 
                 lowercase=False,
                 config=None):

        if elasticsearch is None:
            raise ValueError('No ElasticSearch instance specified!')

        if index is None:
            raise ValueError('No ElasticSearch index specified!')

        if config is None:
            raise ValueError('No configuration specified!')

        self.index = index
        self.es = elasticsearch
        self.lowercase = lowercase
        self.config = config

        self.index_number_of_shards = (
          int(
            self.config.get('partycrasher.elastic', 
                            'number_of_shards')))
        self.index_number_of_replicas = (
          int(
            self.config.get('partycrasher.elastic', 
                            'number_of_replicas')))
        self.index_translog_durability = (
          self.config.get('partycrasher.elastic', 'translog_durability'))
        self.index_throttle_type = (
          self.config.get('partycrasher.elastic', 'throttle_type'))
        self.similarity = (
          self.config.get('partycrasher.elastic', 'similarity'))
        self.similarity_k1 = (
          self.config.get('partycrasher.elastic', 'similarity_k1'))
        self.similarity_b = (
          self.config.get('partycrasher.elastic', 'similarity_b'))

    def bucket(self, crash):
        assert isinstance(crash, Crash)
        raise NotImplementedError("I don't know how to generate a signature for this crash.")

    def create_index(self):
        if self.lowercase:
            filter_ = ['lowercase']
        else:
            filter_ = []

        properties = {
            'buckets': {
                'type': 'string',
                'index': 'not_analyzed'
            }
        }
        properties.update(common_properties())
        self.es.indices.create(index=self.index,
        body={
            'mappings': {
                'crash': {
                    'properties': properties
                }
            },
            'settings': {
                'analysis': {
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'whitespace',
                            'filter': filter_,
                            }
                        }
                    },
                'index': self.index_settings(),
                }
            }
        )
                
    def index_settings(self):
        similarity_config = {}
        if self.similarity == 'BM25':
            similarity_config = {
                'type': 'BM25',
                'k1': float(self.similarity_k1),
                'b': float(self.similarity_b)
            }
        else:
            similarity_config = {
                'type':  self.similarity
            }
        return {
                        'number_of_shards': self.index_number_of_shards,
                        'number_of_replicas': self.index_number_of_replicas,
                        'store.throttle.type': self.index_throttle_type,
                        'translog.durability': self.index_translog_durability,
                        'similarity': {
                            'default': similarity_config,
                        },
               };

    def assign_buckets(self, crash):
        """
        Returns a dictionary of type to value.
        """
        assert 'buckets' not in crash
        if 'force_bucket' in crash:
            buckets = self.bucket(crash)
            print("Warning: overriding buckets to %s with force_bucket!" % (crash['force_bucket']), file=sys.stderr)
            for key in buckets:
                if key != 'top_match':
                    buckets[key] = crash['force_bucket']
            return buckets            
        return self.bucket(crash)

    def assign_save_buckets(self, crash, buckets=None):
        """
        Adds a dictionary of buckets assignments to the given crash in
        ElasticSearch.
        """

        if buckets is None:
            buckets = self.assign_buckets(crash)

        crash["buckets"] = buckets

        saved_crash = ESCrash(crash, index=self.index)


        return saved_crash


class MLT(Bucketer):

    def __init__(self, thresholds=(4.0,), 
                 *args, **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.thresholds = tuple(Threshold(value) for value in sorted(thresholds))
        self.enable_auto_max_query_terms = (
          strtobool(
            self.config.get('partycrasher.bucket', 
                            'enable_auto_max_query_terms')))
        self.initial_mlt_max_query_terms = (
          int(
            self.config.get('partycrasher.bucket', 
                            'initial_mlt_max_query_terms')))
        self.auto_max_query_term_maximum_documents = (
          int(
            self.config.get('partycrasher.bucket', 
                          'auto_max_query_term_maximum_documents')))
        self.auto_max_query_term_minimum_documents = (
          int(
            self.config.get('partycrasher.bucket', 
                          'auto_max_query_term_minimum_documents')))
        self.mlt_min_score = (
          float(
            self.config.get('partycrasher.bucket', 'mlt_min_score')))
        self.strictly_increasing = (
          strtobool(
            self.config.get('partycrasher.bucket', 'strictly_increasing')))
        if self.enable_auto_max_query_terms:
            self.last_max_query_terms = self.initial_mlt_max_query_terms
        self.max_top_match_score = 0
        self.total_top_match_scores = 0
        self.total_matches = 0

    @property
    def thresh(self):
        return self.thresholds[0]

    @property
    def min_threshold(self):
        return self.thresholds[0]
      
    def make_more_like_this_query(self, 
                                  crash, 
                                  max_query_terms,
                                  terminate_after = None):
        body =  {
            # Only fetch database ID, buckets, and project.
            '_source': ['buckets', 'database_id', 'project'],
            'query': {
                'more_like_this': {
                    # NOTE: This style only works in ElasticSearch 1.x...
                    'like': [
                        {
                            '_index': self.index,
                            '_type': 'crash',
                            'doc': crash,
                        }
                    ],
                    # Avoid some ElasticSearch optimizations:
                    #
                    # Search for WAY more terms than ElasticSearch would
                    # normally construct.
                    'max_query_terms': max_query_terms,
                    # Force ElasticSearch to query... like, all the things.
                    'min_term_freq': 0,
                    'min_doc_freq': 0,
                },
            },
            'size': 100,
            'min_score': self.mlt_min_score,
        }
                        
        if terminate_after is not None:
            body['terminate_after'] = terminate_after

        return body

    def make_mlt_query_explain(self,
                                crash,
                                index=None,
                                use_existing=None,
                                max_query_terms=None,
                                terminate_after=None,
                                dont_explain=False):
        """
        Builds the more_like_this query.
        """

        if index is None:
            index = self.index

        if isinstance(crash, basestring):
            crash = Crash(ESCrash(crash, index=index))
            del crash['buckets']
            if use_existing is None:
                use_existing = False # this should be true but ES seems to be broken?
        else:
            if use_existing is None:
                use_existing = False

        body = self.make_more_like_this_query(crash, 
                                              max_query_terms,
                                              terminate_after)
        body["explain"] = (not dont_explain)
        if use_existing:
            # Prevent crash from being its own highest match when its already in ES
            del body["query"]["more_like_this"]["like"][0]["doc"]
            body["query"]["more_like_this"]["like"][0]["_id"] = crash["database_id"]
        
        skip_fields = Set([
          'database_id',
          'buckets',
          'force_bucket',
          'depth',
          'date',
        ])
        
        def all_but_skip_fields(c, prefix=""):
          fields = Set()
          if isinstance(c, dict):
            for k, v in c.iteritems():
              #print(prefix + k, file=sys.stderr)
              if k not in skip_fields:
                fields.add(prefix + k)
                subfields = all_but_skip_fields(v, prefix + k + ".")
                #print(len(fields))
                fields.update(subfields)
          elif isinstance(c, list):
            for i in c:
                subfields = all_but_skip_fields(i, prefix)
                fields.update(subfields)
          elif isinstance(c, basestring) or c is None:
            pass
          elif isinstance(c, datetime):
            pass
          else:
            raise NotImplementedError("all_but_fields can't handle " + c.__class__.__name__)
          return fields
        
        fields = list(all_but_skip_fields(crash))
        # including the extra field seems to improve recall at the expense of precision
        # overall F-score seems to go down so I'm not sure this is worthwhile
        #if 'stacktrace.function' in fields:
        #    fields.append('stacktrace.function.whole')
        for field in fields:
            assert "buckets" not in field
        
        body["query"]["more_like_this"]["fields"] = fields
        
        #self.ensure_field_mappings(fields)
        
        #print(json.dumps(fields, indent=2), file=sys.stderr)
        
        return body
        
        
    def get_explanation_from_response(self, response):
        try:
          explanation = response['hits']['hits'][0]['_explanation']['details']
        except:
          print(json.dumps(body, indent=2, cls=ESCrashEncoder), file=sys.stderr)
          print(json.dumps(response, indent=2), file=sys.stderr)
          raise
        
        with open('explained', 'wb') as debug_file:
            print(json.dumps(response['hits']['hits'][0]['_explanation'], indent=2), file=debug_file)

        def flatten(explanation):
          flattened = []
          for subexplanation in explanation:
            if subexplanation["description"].startswith("weight"):
              flattened.append(subexplanation)
            else:
              #print(subexplanation["description"])
              if "details" in subexplanation:
                flattened.extend(flatten(subexplanation["details"]))
          return flattened
            
        explanation = flatten(explanation)
        explanation = sorted(explanation, key=itemgetter('value'), reverse=True)
        #with open("explanation", 'w') as f:
          #print(json.dumps(explanation, indent=2), file=f)
          
        summary = []
        for i in explanation:
          #print(i['description'])
          match = re.match(r'^weight\(([^\s:]+):([^\s]+) in .*$', i['description'])
          if match is not None:
            summary.append({'field': match.group(1), 'term': match.group(2), 'value': i['value']})
        #del summary[30:]
        #print(json.dumps(summary, indent=2, cls=ESCrashEncoder), file=sys.stderr)
        
        return summary
      
    def bucket_auto_max_query_terms(self, crash, use_existing, dont_explain=False):
        max_query_terms = self.last_max_query_terms
        max_query_terms_lb = 1
        max_query_terms_ub = self.initial_mlt_max_query_terms
        response_at_least_one_hit = None
        while True:
            body = self.make_mlt_query_explain(crash,
                      use_existing=use_existing,
                      max_query_terms=max_query_terms,
                      terminate_after=self.auto_max_query_term_maximum_documents,
                      dont_explain=dont_explain)
            response = self.es.search(index=self.index, body=body)
            if response['hits']['total'] > 1:
                response_at_least_one_hit = response
            if (response['terminated_early'] 
                or (response['hits']['total'] 
                    >= self.auto_max_query_term_maximum_documents)):
                if max_query_terms == max_query_terms_lb:
                    #print("Hit LB", file=sys.stderr)
                    break
                max_query_terms_ub = max_query_terms - 1
                max_query_terms = math.floor(
                    float(max_query_terms+max_query_terms_lb)/2.0)
            elif (response['hits']['total'] 
                <= self.auto_max_query_term_minimum_documents):
                if max_query_terms == max_query_terms_ub:
                    #print("Hit UB", file=sys.stderr)
                    break
                max_query_terms_lb = max_query_terms + 1
                max_query_terms = math.ceil(
                    float(max_query_terms+max_query_terms_ub)/2.0)
            else:
                #print("In range.", file=sys.stderr)
                sys.stderr.flush()
                break
        print("max_query_terms: %i hits: %i" % (
                  max_query_terms,
                  response['hits']['total']),
                  file=sys.stderr)
        sys.stderr.flush()
        self.last_max_query_terms = max_query_terms
        if response_at_least_one_hit is not None:
            return response_at_least_one_hit
        return response
    
    def bucket_explain(self, crash):
        """
        Queries ElasticSearch with MoreLikeThis.
        Returns the explanation of the top hit.
        """
        if self.enable_auto_max_query_terms:
            response = self.bucket_auto_max_query_terms(
              crash,
              use_existing=True)
        else:
            body = self.make_mlt_query_explain(
                crash, 
                use_existing=True, 
                max_query_terms=self.initial_mlt_max_query_terms)
            response = self.es.search(index=self.index, body=body)
        
        return self.get_explanation_from_response(response)
      
    def bucket(self, crash):
        """
        Queries ElasticSearch with MoreLikeThis.
        Returns the bucket assignment for each threshold.
        Returns an OrderedDict of {Threshold(...): 'id'}
        """
        if self.enable_auto_max_query_terms:
            response = self.bucket_auto_max_query_terms(
                crash,
                use_existing=False,
                dont_explain=True)
        else:
            body = self.make_mlt_query_explain(
                crash,
                use_existing=False,
                max_query_terms=self.initial_mlt_max_query_terms,
                dont_explain=True)
            response = self.es.search(index=self.index, body=body)
        
        try:
            matching_buckets = self.make_matching_buckets(
                response,
                default=random_bucketid())
            return matching_buckets
        except IndexNotUpdatedError:
            time.sleep(1)
            return self.bucket(crash)

    def make_matching_buckets(self, matches, default=None):
        if default is None:
            raise ValueError('Must provide a string default bucket name')

        raw_matches = matches['hits']['hits']
        #assert len(raw_matches) in (0, 1), 'Unexpected amount of matches...'

        top_match = { '_score': -1000000 }
        for raw_match in raw_matches:
            assert '_source' in raw_match
            assert 'buckets' in raw_match['_source']
            assert 'top_match' in raw_match['_source']['buckets']
            if raw_match['_source']['buckets']['top_match']:
                prec_score = raw_match['_source']['buckets']['top_match']['score']
            else:
                prec_score = 0
            score = raw_match['_score']
            if (not self.strictly_increasing) or (score >= prec_score):
                top_match = raw_match
                break

        # JSON structure:
        # matches['hit']['hits] ~> [
        #   {
        #       "_score": 8.9,
        #       "_source": {
        #           "buckets": {
        #               "1.0": "***bucket-id-1***",
        #               "9.0": "***bucket-id-2***"
        #           }
        #       }
        #   }

        similarity = top_match['_score']
        #print(similarity);
        assert isinstance(similarity, (float, int))

        # Add the buckets, by threshold.
        matching_buckets = Buckets()
        for threshold in sorted(self.thresholds, key=float):
            if similarity >= float(threshold):
                bucket_id = get_bucket_id(top_match, threshold)
                #print(bucket_id)
                # Assign this report to the existing bucket.
                matching_buckets[threshold] = bucket_id
            else:
                #print("default: " + default)
                # Create a new bucket.
                matching_buckets[threshold] = default

        # Add the top match.
        if '_source' in top_match:
            matching_buckets['top_match'] = {
                'report_id': top_match['_source']['database_id'],
                'project': top_match['_source']['project'],
                'score': top_match['_score']
            }
            self.total_top_match_scores += top_match['_score']
            self.total_matches += 1
            self.max_top_match_score = max(self.max_top_match_score, top_match['_score'])
            print('score %f avg %f max %f' % (
              top_match['_score'],
              self.total_top_match_scores / self.total_matches,
              self.max_top_match_score
              ), file=sys.stderr)
        else:
            matching_buckets['top_match'] = None

        return Buckets(matching_buckets)

    def assign_save_buckets(self, crash):
        buckets = self.assign_buckets(crash)
        assert isinstance(buckets, Buckets)
        return super(MLT, self).assign_save_buckets(crash, buckets)

    def alt_bucket(self, crash):
        return self.bucket(crash)
      
    def compare(self, crash, other_ids):
        """
        Queries ElasticSearch with MoreLikeThis.
        Used for comparing two documents.
        """
        mlt_body = self.make_mlt_query_explain(
            crash, 
            max_query_terms=self.initial_mlt_max_query_terms,
            dont_explain=True)
        mlt_query = mlt_body['query']
        mlt_query['more_like_this']['max_query_terms'] = 19000
        query = {
            'bool': {
                'filter': {
                    'ids': {
                        'values': other_ids
                    }
                },
                'should': mlt_query
            }
        }
        mlt_body['query'] = query
        mlt_body['min_score'] = -1000.0
        mlt_body['size'] = len(other_ids)
        
        response = self.es.search(index=self.index, body=pretty(mlt_body))
        
        if True:
            with open('comparison', 'wb') as debug_file:
                print(pretty(mlt_body), file=debug_file)
                #print(json.dumps(response['hits']['hits'][0]['_explanation'], indent=2), file=debug_file)
                print(json.dumps(response, indent=2), file=debug_file)
        
        results_by_id = {}
        for hit in response['hits']['hits']:
            results_by_id[hit['_source']['database_id']] = hit['_score']
        results = []
        for id_ in other_ids:
            if id_ in results_by_id:
                results.append(results_by_id[id_])
        return results

class MLTStandardUnicode(MLT):
    """MLT with an analyzer breaking on spaces and then lowercasing"""
    def create_index(self):
        if self.lowercase:
            filter_ = ['lowercase']
        else:
            filter_ = []
        print("Creating index: %s" % self.index)
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': common_properties()
                }
            },
            'settings': {
                'analysis': {
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'standard',
                            'filter': filter_,
                            }
                        }
                    },
                'index': self.index_settings(),
                }
            }
        )


class MLTLetters(MLT):
    """MLT with a diffrent analyzer (capture letter strings then optionally make them lowercase)"""
    def create_index(self):
        if self.lowercase:
            tokenizer = 'lowercase'
        else:
            tokenizer = 'letter'
        print("Creating index: %s" % self.index)
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': common_properties()
                }
            },
            'settings': {
                'analysis': {
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': tokenizer,
                            'filter': [],
                            }
                        }
                    },
                'index': self.index_settings(),

                }
            }
        )


class MLTIdentifier(MLT):
    """MLT with an analyzer intended to capture programming words"""
    def create_index(self):
        print("Creating index: %s" % self.index)
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': common_properties()
                }
            },
            'settings': {
                'analysis': {
                    'analyzer': {
                        'default': {
                            'type': 'pattern',
                            'pattern':
                                '([^\\p{L}\\d_]+)'
                                '|(?=0[xX][a-fA-F\\d)]+)'
                                '|(?<!0[xX][a-fA-F\\d)]{0,16})(?<=\\p{L}{3})(?=\\d)'
                                '|(?<!0[xX][a-fA-F\\d)]{0,16})(?<=\\d{3})(?=\\D)(?![xX][a-fA-F\\d)]{0,16})'
                                '|(?<=[\\p{L}&&[^\\p{Lu}]]{2})(?=\\p{Lu})'
                                '|(?<=\\p{Lu}{3})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])'
                                '|(?<=[\\p{L}\\d]{2})(_+)(?=[\\p{L}\\d])'
                                ,
                            'lowercase': self.lowercase,
                           }
                        }
                    },
                'index': self.index_settings(),

                }
            }
        )

class MLTCamelCase(MLT):
    """MLT intended to break up identifiers into sub-words"""
    def create_index(self):
        traceback.print_stack()
        # Ignore 400 -- index already created.
        # /!\ BUG However this will hide IllegalArgumentExceptions also
        self.es.indices.create(index=self.index, ignore=400,
            body={
            'mappings': {
                'crash': {
                    'properties': common_properties(self.thresholds),
                    'dynamic_templates': [
                      {
                        'data': {
                          'match': '*',
                          'match_mapping_type': 'string',
                          'mapping': {
                            'type': 'string',
                            'analyzer': 'default',
                            # The ES documentation indicates this should improve
                            # speed but it doesn't seem to actually do so
                            #'term_vector': 'yes',
                            # This can enable a second tokenizer for every field
                            #'fields': {
                                #'ws': {
                                    #'type': 'string',
                                    #'analyzer': 'whitespace'
                                    #'term_vector': 'yes',
                                #}
                            #}
                            # Disabling field norms does not seem to help anything
                            #'norms': {
                              #'enabled': False
                            #},
                          }
                        }
                      }
                    ]
                }
            },
            'settings': {
                'analysis': {
                    'analyzer': {
                        'default': {
                            'type': 'pattern',
                            # From ES Docs: https://github.com/elastic/elasticsearch/blob/1.6/docs/reference/analysis/analyzers/pattern-analyzer.asciidoc
                            # 2016-01-27
                            'pattern': '([^\\p{L}\\d]+)|(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)|(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])',
                            'lowercase': self.lowercase,
                           }
                        }
                    },
                'index': self.index_settings(),

                }
            }
        )

class MLTLerch(MLT):
    """MLT with an analyzer as described in Lerch, 2013"""
    def create_index(self):
        print("Creating index: %s" % self.index)
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': common_properties()
                }
            },
            'settings': {
                'analysis': {
                    'filter': {
                        'lerch': {
                            'type': 'length',
                            'min': 4,
                            'max': 2000,
                            },
                        },
                    'tokenizer': {
                        'lerch': {
                            'type': 'pattern',
                            'pattern': '\W+',
                            'group': -1,
                            },
                        },
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'lerch',
                            'filter': ['lowercase', 'lerch'],
                            }
                        }
                    },
                'index': self.index_settings(),
                }
            }
        )

class MLTNGram(MLT):
    """MLT with an N-Gram Analyzer"""
    def __init__(self,
                 n=3,
                 *args,
                 **kwargs):
        super(MLTNGram, self).__init__(*args, **kwargs)
        self.n = n

    def create_index(self):
        if self.lowercase:
            filter_ = ['lowercase']
        else:
            filter_ = []
        print("Creating index: %s" % self.index)
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': common_properties()
                }
            },
            'settings': {
                'analysis': {
                    'tokenizer': {
                        'my_ngram_tokenizer': {
                            'type': 'nGram',
                            'min_gram': self.n,
                            'max_gram': self.n,
                            },
                        },
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'my_ngram_tokenizer',
                            'filter': filter_,
                            }
                        }
                    },
                'index': self.index_settings(),
                }
            }
        )


def get_bucket_id(result, threshold):
    """
    Given a crash JSON, returns the bucket field associated with this
    particular threshold.
    """

    crash = result['_source']

    try:
        buckets = crash['buckets']
    except KeyError:
        # We couldn't find the bucket field. ASSUME that this means that
        # its bucket assignment has not yet propegated to whatever shard
        # returned the results.
        message = ('Bucket field {!r} not found in crash: '
                   '{!r}'.format('buckets', crash))
        raise IndexNotUpdatedError(message)

    try:
       return buckets[threshold.to_elasticsearch()]
    except KeyError:
        message = ('Crash does not have an assignment for '
                   '{!s}: {!r}'.format(threshold, match))
        # TODO: Custom exception for this?
        raise Exception(message)


def common_properties(thresholds):
    """
    Returns properties common to all indexes;
    must provide the threshold values
    """

    string_not_analyzed = {
        'type': "string",
        'index': 'not_analyzed',
    }

    string_no = {
        'type': "string",
        'index': 'no',
    }

    bucket_properties = {
        threshold.to_elasticsearch(): {
            'type': "string",
            'index': 'not_analyzed',
        } for threshold in thresholds
    }

    bucket_properties['top_match'] = {
        'dynamic': 'strict',
        'properties': {
            'report_id': string_not_analyzed,
            'href': string_not_analyzed,
            'project': string_not_analyzed,
            'score': {
                'type': 'float',
                'index': 'not_analyzed'
            }
        }
    }

    # Database ID, the primary bucket, and the project,
    # and the version are all literals.
    return {
        # TODO: convert into _id
        'database_id': {
            'type': 'string',
            'index': 'not_analyzed'
        },
        'buckets': {
            # Do not allow arbitrary properties being added to buckets...
            "dynamic" : "strict",
            # Create all the subfield appropriate for buckets
            "properties": bucket_properties
        },
        'project': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'date': {
            'type': 'date',
            # Do not index, because our analysis has not studied this yet!
            # Plus, Elastic won't index anyway...
            'index': 'not_analyzed'
        },
        'stacktrace': { 'properties': {
        'function': {
            'type': 'string',
            'analyzer': 'default',
            # Enable a second tokenizer
            # This is used for chopping off the tops of stacks automatically
            'fields': {
                'whole': {
                    'type': 'string',
                    'analyzer': 'keyword'
                    #'term_vector': 'yes',
                }
            }
        }}}
    }
