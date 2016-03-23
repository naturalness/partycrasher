#!/usr/bin/env python

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

import os
import json
import uuid
import time

from crash import Crash
from es_crash import ESCrash, Threshold


class Bucketer(object):
    """
    Superclass for bucketers which require pre-existing data to work.
    The default analyzer breaks on whitespace.
    """

    def __init__(self, max_buckets=1, name=None, index='crashes',
                 elasticsearch=None, lowercase=False):

        self.max_buckets = max_buckets

        # Autogenerate the name from the class's name.
        if name is None:
            name = self.__class__.__name__.lower()

        if elasticsearch is None:
            raise ValueError('No ElasticSearch instance specified!')

        self.name = name
        self.index = index
        self.es = elasticsearch
        self.lowercase = lowercase

    def bucket(self, crash):
        assert isinstance(crash, Crash)
        raise NotImplementedError("I don't know how to generate a signature for this crash.")

    def create_index(self):
        if self.lowercase:
            filter_ = ['lowercase']
        else:
            filter_ = []

        properties = {
            self.name: {
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
                    }
                }
            }
        )

    def assign_bucket(self, crash):
        buckets = self.bucket(crash)
        if len(buckets) > 0:
            bucket = buckets[0]
        else:
            bucket = crash['database_id'] # Make a new bucket
        return bucket

    def assign_save_bucket(self, crash, bucket=None):
        if bucket is None:
            bucket = self.assign_bucket(crash)

        saved_crash = ESCrash(crash, index=self.index)
        saved_crash[self.name] = bucket

        return saved_crash


class MLT(Bucketer):

    def __init__(self, thresholds=(4.0,), use_aggs=False, only_stack=False,
                 *args, **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.thresholds = tuple(Threshold(value) for value in sorted(thresholds))
        self.use_aggs = use_aggs
        self.only_stack = only_stack

    @property
    def thresh(self):
        return self.thresholds[0]

    @property
    def min_threshold(self):
        return self.thresholds[0]

    def bucket(self, crash, bucket_field=None):
        """
        Queries ElasticSearch with MoreLikeThis.
        Returns the bucket assignment for each threshold.
        """
        if bucket_field is None:
            bucket_field = self.name

        # Compare only the stack trace
        if self.only_stack:
            crash = {
                'stacktrace': crash['stacktrace'],
                'database_id': crash['database_id']
            }

        body = self.make_more_like_this_query(crash, bucket_field)
        matches = self.es.search(index=self.index, body=body)

        if self.use_aggs:
            return self.make_matching_buckets_from_aggregations(matches)
        else:
            return self.make_matching_buckets(matches)

    def make_more_like_this_query(self, crash, bucket_field):
        # TODO: make this acknowledge buckets.4_0, buckets.3_5, buckets.4_5,
        # etc..

        body =  {
            '_source': [bucket_field],
            # What do we need max buckets for?
            #'size': self.max_buckets,
            'min_score': self.min_threshold.to_float(),
            'query': {
                'more_like_this': {
                    'docs': [{
                        '_index': self.index,
                        '_type': 'crash',
                        'doc': crash,
                    }],
                    'minimum_should_match': 0,
                    'max_query_terms': 2500,
                    'min_term_freq': 0,
                    'min_doc_freq': 0,
                },
            },
        }

        if self.use_aggs:
            body['aggregations'] ={
                'buckets': {
                    'terms': {
                        'field': bucket_field,
                        'size': self.max_buckets
                    },
                    'aggs': {
                        'top': {
                            'top_hits': {
                                'size': 1,
                                '_source': {
                                    'include': ['database_id'],
                                    }
                                }
                            }
                        }
                }
            }
        return body

    def make_matching_buckets(self, matches):
        matching_buckets = []
        for match in matches['hits']['hits']:
            if match['_score'] < self.thresh:
                continue
            try:
                bucket = match['_source'][bucket_field]
            except KeyError:
                self.es.indices.flush(index=self.index)
                print "Force waiting for refresh on " + crash['database_id']
                time.sleep(1)
                return self.bucket(crash, bucket_field)
            if bucket not in matching_buckets:
                matching_buckets.append(bucket)
        return matching_buckets



    def make_matching_buckets_from_aggregations(self, matches):
        matching_buckets = []
        for match in matches['aggregations']['buckets']['buckets']:
            assert match['top']['hits']['max_score'] >= self.thresh
            matching_buckets.append(match['key'])
        return matching_buckets

    def assign_save_bucket(self, crash):
        bucket = self.assign_bucket(crash)
        assert isinstance(bucket, str)
        bucket = {
            self.thresh.to_elasticsearch(): bucket
        }
        return super(MLT, self).assign_save_bucket(crash, bucket)

    def alt_bucket(self, crash, bucket_field='bucket'):
        return self.bucket(crash, bucket_field)


class MLTStandardUnicode(MLT):
    """MLT with an analyzer breaking on spaces and then lowercasing"""
    def create_index(self):
        if self.lowercase:
            filter_ = ['lowercase']
        else:
            filter_ = []
        print "Creating index: %s" % self.index
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
                    }
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
        print "Creating index: %s" % self.index
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
                    }
                }
            }
        )


class MLTIdentifier(MLT):
    """MLT with an analyzer intended to capture programming words"""
    def create_index(self):
        print "Creating index: %s" % self.index
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
                    }
                }
            }
        )

class MLTCamelCase(MLT):
    """MLT intended to break up identifiers into sub-words"""
    def create_index(self):
        # Ignore 400 -- index already created.
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': common_properties(self.thresholds)
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
                    }
                }
            }
        )

class MLTLerch(MLT):
    """MLT with an analyzer as described in Lerch, 2013"""
    def create_index(self):
        print "Creating index: %s" % self.index
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
                    }
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
        print "Creating index: %s" % self.index
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
                    }
                }
            }
        )


def common_properties(thresholds):
    """
    Returns properties common to all indexes;
    must provide the threshold values
    """
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
            "properties": {
                threshold.to_elasticsearch(): {
                    'type': "string",
                    'index': 'not_analyzed',
                } for threshold in thresholds
            }
        },
        # TODO: convert into _type
        'project': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'date_bucketed': {
            'type': 'date',
            # Do not index, because our analysis has not studied this yet!
            # Plus, Elastic won't index anyway...
            'index': 'not_analyzed'
        }
    }



