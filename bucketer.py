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

import json
from crash import Crash 

class Bucketer(object):
    """Superclass for bucketers which require pre-existing data to work."""
    
    def __init__(self, max_buckets=0):
        self.max_buckets = max_buckets
    
    def bucket(self, crash):
        assert isinstance(crash, Crash)
        raise NotImplementedError("I don't know how to generate a signature for this crash.")
    
    
class MLT(Bucketer):
    
    def __init__(self,
                 index='crashes',
                 es=None,
                 thresh=1.0,
                 use_aggs=False,
                 *args,
                 **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.index = index
        self.es = es
        self.thresh = thresh
        self.use_aggs = use_aggs
        
    def bucket(self, crash):
        assert isinstance(crash, Crash)
        matches = self.es.search(
        index=self.index,
        body={
            '_source': ['bucket'],
            'size': self.max_buckets,
            'min_score': self.thresh,
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
            'aggregations': {
                'buckets': {
                    'terms': {
                        'field': 'bucket',
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
        })
        matching_buckets=[]
        if self.use_aggs:
            for match in matches['aggregations']['buckets']['buckets']:
                assert match['top']['hits']['max_score'] >= self.thresh
                matching_buckets.append(match['key'])
        else:
            for match in matches['hits']['hits']:
                bucket = match['_source']['bucket']
                if bucket not in matching_buckets:
                    matching_buckets.append(bucket)
        return matching_buckets


    def create_index(self):
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': {
                        'database_id': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'bucket': {
                            'type': 'string',
                            'index': 'not_analyzed',
                            },
                        }
                    }
                },
            'settings': {
                'analysis': {
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'whitespace',
                            'filter': [],
                            }
                        }
                    }
                }
            }
        )

class MLTf(MLT):
    """MLT with an analyzer inded to capture CamelCase"""
    def create_index(self):
        print "Creating index: %s" % self.index
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': {
                        'database_id': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'bucket': {
                            'type': 'string',
                            'index': 'not_analyzed',
                            },
                        }
                    }
                },
            'settings': {
                'analysis': {
                    'tokenizer': {
                        'alphanumplus': {
                            'type': 'pattern',
                            'pattern': '([^\\s][^A-Z_:.,\\s]*)',
                            'group': 0,
                            },
                        },
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'alphanumplus',
                            'filter': ['lowercase'],
                            }
                        }
                    }
                }
            }
        )

class MLTlc(MLT):
    """MLT with a diffrent analyzer"""
    def create_index(self):
        print "Creating index: %s" % self.index
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': {
                        'database_id': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'bucket': {
                            'type': 'string',
                            'index': 'not_analyzed',
                            },
                        }
                    }
                },
            'settings': {
                'analysis': {
                    'tokenizer': {
                        'my_ngram_tokenizer': {
                            'type': 'nGram',
                            'min_gram': 1,
                            'max_gram': 3,
                            'token_chars': [],
                            },
                        },
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'lowercase',
                            'filter': [],
                            }
                        }
                    }
                }
            }
        )

class MLTw(MLT):
    """MLT with an analyzer intended to capture programming words"""
    def create_index(self):
        print "Creating index: %s" % self.index
        self.es.indices.create(index=self.index, ignore=400,
        body={
            'mappings': {
                'crash': {
                    'properties': {
                        'database_id': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'bucket': {
                            'type': 'string',
                            'index': 'not_analyzed',
                            },
                        }
                    }
                },
            'settings': {
                'analysis': {
                    'tokenizer': {
                        'alphanum': {
                            'type': 'pattern',
                            'pattern': '([A-Za-z0-9_]+)',
                            'group': 0,
                            },
                        },
                    'analyzer': {
                        'default': {
                            'type': 'custom',
                            'char_filter': [],
                            'tokenizer': 'alphanum',
                            'filter': ['lowercase'],
                            }
                        }
                    }
                }
            }
        )
