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
import re
import traceback
import math
import copy
from datetime import datetime
from elasticsearch import RequestError
from distutils.util import strtobool

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from partycrasher.crash import Crash, Buckets, pretty
from partycrasher.es_crash import ESCrash, ESCrashEncoder
from partycrasher.threshold import Threshold
from partycrasher.more_like_this import MoreLikeThis
from partycrasher.bucket import Bucket
from partycrasher.more_like_this_response import MissingBucketError


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

        self.index_number_of_shards = self.config.ElasticSearch.number_of_shards
        self.index_number_of_replicas = self.config.ElasticSearch.number_of_replicas
        self.index_translog_durability = self.config.ElasticSearch.translog_durability
        self.index_throttle_type = self.config.ElasticSearch.throttle_type
        self.similarity = self.config.ElasticSearch.similarity
        self.similarity_k1 = self.config.ElasticSearch.similarity_k1
        self.similarity_b = self.config.ElasticSearch.similarity_b

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
            error("Warning: overriding buckets to %s with force_bucket!" % (crash['force_bucket']))
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
        
        buckets.create()
        crash["buckets"] = buckets

        saved_crash = ESCrash(crash=crash, index=self.index)
        assert saved_crash is not None

        return saved_crash


class MLT(Bucketer):

    def __init__(self, thresholds, 
                 *args, **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.thresholds = tuple(Threshold(value) for value in sorted(thresholds))
        self.searcher = MoreLikeThis(self.es, self.index, self.config.Bucketing.MLT)
        self.max_top_match_score = 0
        self.total_top_match_scores = 0
        self.total_matches = 0

    @property
    def thresh(self):
        return self.thresholds[0]

    @property
    def min_threshold(self):
        return self.thresholds[0]
    
    def bucket_explain(self, crash):
        """
        Queries ElasticSearch with MoreLikeThis.
        Returns the explanation of the top hit.
        """
        assert crash is not None
        return self.searcher.explain(ESCrash(self.index, crash))
      
    def bucket(self, crash):
        """
        Queries ElasticSearch with MoreLikeThis.
        Returns the bucket assignment for each threshold.
        Returns an OrderedDict of {Threshold(...): 'id'}
        """
        result = self.searcher.query(crash)
        
        #try:
        return result.matching_buckets(self.thresholds)
        #except MissingBucketError:
            #time.sleep(1)
            #return self.bucket(crash)

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
