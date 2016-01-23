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

import json, uuid, time
from crash import Crash
from es_crash import ESCrash

class Bucketer(object):
    """Superclass for bucketers which require pre-existing data to work."""
    
    def __init__(self, 
                 max_buckets=0, 
                 name=None, 
                 index='crashes',
                 es=None,
                 ):
        self.max_buckets = max_buckets
        if name is None:
            name = self.__class__.__name__.lower()
        self.name = name
        self.index = index
        self.es = es
    
    def bucket(self, crash):
        assert isinstance(crash, Crash)
        raise NotImplementedError("I don't know how to generate a signature for this crash.")
    
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
                        self.name: {
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
                 *args,
                 **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.thresh = thresh
        self.use_aggs = use_aggs
        
    def bucket(self, crash, bucket_field=None):
        if bucket_field is None:
            bucket_field = self.name
        assert isinstance(crash, Crash)
        body={
            '_source': [bucket_field],
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
        matching_buckets=[]
        if self.use_aggs:
            for match in matches['aggregations']['buckets']['buckets']:
                assert match['top']['hits']['max_score'] >= self.thresh
                matching_buckets.append(match['key'])
        else:
            for match in matches['hits']['hits']:
                try:
                    bucket = match['_source'][bucket_field]
                except KeyError:
                    #self.es.indices.flush(index=self.index)
                    #print crash['database_id']
                    #time.sleep(1)
                    #return self.bucket(crash, bucket_field)
                    print json.dumps(matches, indent=4)
                    raise
                if bucket not in matching_buckets:
                    matching_buckets.append(bucket)
        return matching_buckets

    def alt_bucket(self, crash, bucket_field='bucket'):
        return self.bucket(crash, bucket_field)
        

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
