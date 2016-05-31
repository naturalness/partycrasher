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

from __future__ import print_function

import os
import json
import uuid
import time
import sys
import re
from operator import itemgetter
from sets import Set
from datetime import datetime
from elasticsearch import RequestError


from crash import Crash, Buckets
from es_crash import ESCrash, ESCrashEncoder
from threshold import Threshold


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

    def __init__(self, name=None, index='crashes',
                 elasticsearch=None, lowercase=False):

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

    def assign_buckets(self, crash):
        """
        Returns a dictionary of type to value.
        """
        return self.bucket(crash)

    def assign_save_buckets(self, crash, buckets=None):
        """
        Adds a dictionary of buckets assignments to the given crash in
        ElasticSearch.
        """

        if buckets is None:
            buckets = self.assign_buckets(crash)

        ## Learned the hard way that we can't use setdefault...
        saved_buckets = crash.get(self.name, Buckets()).copy()
        saved_buckets.update(buckets)
        crash[self.name] = saved_buckets

        saved_crash = ESCrash(crash, index=self.index)


        return saved_crash


class MLT(Bucketer):

    def __init__(self, thresholds=(4.0,), only_stack=False,
                 *args, **kwargs):
        super(MLT, self).__init__(*args, **kwargs)
        self.thresholds = tuple(Threshold(value) for value in sorted(thresholds))
        self.only_stack = only_stack

    @property
    def thresh(self):
        return self.thresholds[0]

    @property
    def min_threshold(self):
        return self.thresholds[0]
      
    def bucket_explain(self, crash, index=None):
        """
        Queries ElasticSearch with MoreLikeThis and returns information
        from a crash that was significant to the result.
        """

        if index is None:
          index = self.index

        if isinstance(crash, basestring):
            crash = ESCrash(crash, index=index)

        bucket_field = self.name
        
        body = self.make_more_like_this_query(crash, bucket_field)
        body["explain"] = True
        del body["query"]["more_like_this"]["docs"][0]["doc"]
        body["query"]["more_like_this"]["docs"][0]["_id"] = crash["database_id"]
        
        skip_fields = Set([
          'database_id',
          'buckets',
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
        #print(json.dumps(fields, indent=2), file=sys.stderr)
        body["query"]["more_like_this"]["fields"] = fields
        
        try:
          response = self.es.search(index=self.index, 
                                  body=json.dumps(body, cls=ESCrashEncoder)
                                  )
        except RequestError as e:
          print(e.error, file=sys.stderr)
          raise
        
        try:
          explanation = response['hits']['hits'][0]['_explanation']['details']
        except:
          print(json.dumps(body, indent=2, cls=ESCrashEncoder), file=sys.stderr)
          print(json.dumps(response, indent=2), file=sys.stderr)
          raise
        
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
        
      
    def bucket(self, crash, bucket_field=None):
        """
        Queries ElasticSearch with MoreLikeThis.
        Returns the bucket assignment for each threshold.
        Returns an OrderedDict of {Threshold(...): 'id'}
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
        response = self.es.search(index=self.index, body=body)
        

        try:
            matching_buckets = self.make_matching_buckets(response, bucket_field,
                                                          default=crash['database_id'])
            return matching_buckets
        except IndexNotUpdatedError:
            time.sleep(1)
            return self.bucket(crash, bucket_field)

    def make_more_like_this_query(self, crash, bucket_field):
        body =  {
            # Only fetch database ID, buckets, and project.
            '_source': [bucket_field, 'database_id', 'project'],
            'query': {
                'more_like_this': {
                    # NOTE: This style only works in ElasticSearch 1.x...
                    'docs': [
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
                    'max_query_terms': 2500,
                    # Force ElasticSearch to query... like, all the things.
                    'min_term_freq': 0,
                    'min_doc_freq': 0,
                },
            },
            # Must fetch the TOP matching result only.
            'size': 1,
            'min_score': 0,
        }

        return body

    def make_matching_buckets(self, matches, bucket_field, default=None):
        if default is None:
            raise ValueError('Must provide a string default bucket name')

        raw_matches = matches['hits']['hits']
        assert len(raw_matches) in (0, 1), 'Unexpected amount of matches...'

        if len(raw_matches) == 1:
            top_match = raw_matches[0]
        else:
            # Sentinel object; this will never match a threshold.
            top_match = { '_score': -1000000 }

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
                bucket_id = get_bucket_id(top_match, threshold, bucket_field)
                #print(bucket_id)
                # Assign this report to the existing bucket.
                matching_buckets[threshold] = bucket_id
            else:
                #print("default: " + default)
                # Create a new bucket.
                matching_buckets[threshold] = default

        # Add the top match.
        if raw_matches:
            matching_buckets['top_match'] = {
                'report_id': top_match['_source']['database_id'],
                'project': top_match['_source']['project'],
                'score': top_match['_score']
            }
        else:
            matching_buckets['top_match'] = None

        return matching_buckets

    def assign_save_buckets(self, crash):
        buckets = self.assign_buckets(crash)
        assert isinstance(buckets, Buckets)
        return super(MLT, self).assign_save_buckets(crash, buckets)

    def alt_bucket(self, crash, bucket_field='bucket'):
        return self.bucket(crash, bucket_field)


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
                    }
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
                    }
                }
            }
        )


def get_bucket_id(result, threshold, bucket_field='buckets'):
    """
    Given a crash JSON, returns the bucket field associated with this
    particular threshold.
    """

    crash = result['_source']

    try:
        buckets = crash[bucket_field]
    except KeyError:
        # We couldn't find the bucket field. ASSUME that this means that
        # its bucket assignment has not yet propegated to whatever shard
        # returned the results.
        message = ('Bucket field {!r} not found in crash: '
                   '{!r}'.format(bucket_field, crash))
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
        # TODO: convert into _type
        'project': {
            'type': 'string',
            'index': 'not_analyzed',
        },
        'date': {
            'type': 'date',
            # Do not index, because our analysis has not studied this yet!
            # Plus, Elastic won't index anyway...
            'index': 'not_analyzed'
        }
    }
