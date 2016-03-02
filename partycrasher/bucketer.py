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
from es_crash import ESCrash


class Bucketer(object):
    """Superclass for bucketers which require pre-existing data to work.
    The default analyzer breaks on whitespace."""

    def __init__(self,
                 max_buckets=1,
                 name=None,
                 index='crashes',
                 es=None,
                 lowercase=False,
                 ):
        self.max_buckets = max_buckets
        if name is None:
            name = self.__class__.__name__.lower()
        self.name = name
        self.index = index
        self.es = es
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
        self.es.indices.create(index=self.index, ignore=400,
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
            bucket = 'bucket:' + crash['database_id'] # Make a new bucket
        return bucket

    def assign_save_bucket(self, crash, bucket=None):
        if bucket is None:
            bucket = self.assign_bucket(crash)
        savedata = ESCrash(crash, index=self.index)
        savedata[self.name] = bucket
        return savedata


class MLT(Bucketer):

    def __init__(self,
                 thresh=1.0,
                 use_aggs=False,
                 only_stack=False,
                 *args,
                 **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.thresh = thresh
        self.use_aggs = use_aggs
        self.only_stack = only_stack

    def bucket(self, crash, bucket_field=None):
        if bucket_field is None:
            bucket_field = self.name
        if self.only_stack:
            crash = {'stacktrace': crash['stacktrace']}
        body={
            #'_source': [bucket_field],
            'size': self.max_buckets,
            # LOOOOL
            #'min_score': self.thresh,
            'query': {
            'more_like_this': {
                'docs': [{
                    '_index': self.index,
                    '_type': 'crash',
                    'doc': crash,
                    }],
                'max_query_terms': 2500,
                'minimum_should_match': 0,
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
            };
        matches = self.es.search(index=self.index,body=body)

        if os.getenv('PARTYCRASHER_DEBUG'):
            from pprint import pprint
            pprint(matches)

        matching_buckets=[]
        if self.use_aggs:
            for match in matches['aggregations']['buckets']['buckets']:
                assert match['top']['hits']['max_score'] >= self.thresh
                matching_buckets.append(match['key'])
        else:
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
                    #print json.dumps(matches, indent=4)
                    #raise
                if bucket not in matching_buckets:
                    matching_buckets.append(bucket)
        return matching_buckets

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


def common_properties():
    """
    Returns properties common to all indexes.
    """
    # Database ID, the primary bucket, and the project,
    # and the version are all literals.
    return {
        # TODO: convert into _id
        'database_id': {
            'type': 'string',
            'index': 'not_analyzed'
        },
        # TODO: Deprecate: use multi-tier bucket... thing.
        'bucket': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        # TODO: convert into _type
        'project': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'date_bucketed': {
            'type': 'date',
            'format': 'epoch_millis',
            # Do not index, because our analysis has not studied this yet!
            # Plus, Elastic won't index anyway...
            'index': 'not_analyzed'
        }
    }
