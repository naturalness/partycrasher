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

import os
import json
import uuid
import time

from collections import OrderedDict

from crash import Crash
from es_crash import ESCrash
from threshold import Threshold

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

        saved_crash = ESCrash(crash, index=self.index)

        # Learned the hard way that we can't use setdefault...
        saved_buckets = saved_crash.get(self.name, {}).copy()
        saved_buckets.update(buckets)
        saved_crash[self.name] = saved_buckets

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
        debug_print_json(body)
        response = self.es.search(index=self.index, body=body)
        debug_print_json(response, header='🔹 🔷 🔹 🔷 🔹 🔷 🔹 ')
        return self.make_matching_buckets(response, bucket_field,
                                          default=crash['database_id'])

    def make_more_like_this_query(self, crash, bucket_field,
                                  has_zero_threshold=False):
        body =  {
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
                    'max_query_terms': 2500,
                    'min_term_freq': 0,
                    'min_doc_freq': 0,
                },
            },
            'size': 1,
            'min_score': 0,
        }

        if has_zero_threshold:
            body['query'].update(min_score=self.min_threshold.to_float())

        return body

    def make_matching_buckets(self, matches, bucket_field, default=None):
        if default is None:
            raise ValueError('Must provide a string default bucket name')

        matching_buckets = OrderedDict()

        # Have the matches in ascending order.
        raw_matches = list(sorted(matches['hits']['hits'], key=by_score))

        # DEBUG STUFF
        if raw_matches:
            first = raw_matches[0]
            report_id = first['_source']['database_id']
            project = first['_source']['project']
            score = str(first['_score'])
            matching_buckets['__debug__'] = ':'.join((score, project, report_id))
        else:
            matching_buckets['__debug__'] = 'None'

        # Make a stack of thresholds, in ascending order
        thresholds_left = list(sorted(self.thresholds))

        while raw_matches and thresholds_left:
            threshold = thresholds_left[0]
            match = None

            # Discard all matches lower than this threshold.
            while raw_matches:
                match = raw_matches[0]
                if match['_score'] < threshold.to_float():
                    raw_matches.pop(0)
                else:
                    break

            # We may have discarded all matches in the previous step.
            if len(raw_matches) == 0:
                break

            # At this point, we must have the first match.
            assert match is not None
            assert match['_score'] >= threshold.to_float()

            # Fail if we can't find the bucket field
            try:
                bucket = match['_source'][bucket_field][threshold.to_elasticsearch()]
            except KeyError:
                raise Exception('Matching crash does not have an assignment '
                                'for {!s}: {!r}'.format(threshold, match))

            matching_buckets[threshold] = bucket
            # This threshold has been assigned! Remove it!
            thresholds_left.pop(0)

        # Make this crash the start of a new bucket for all unfulfilled
        # threshold values.
        if not raw_matches and thresholds_left:
            for threshold in thresholds_left:
                matching_buckets[threshold] = default

        return matching_buckets

    def assign_save_buckets(self, crash):
        buckets = self.assign_buckets(crash)
        assert isinstance(buckets, dict)
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

def by_score(match):
    """
    Sorting key function. Matches by MoreLikeThis score.
    """
    return match['_score']

def common_properties(thresholds):
    """
    Returns properties common to all indexes;
    must provide the threshold values
    """

    bucket_properties = {
        threshold.to_elasticsearch(): {
            'type': "string",
            'index': 'not_analyzed',
        } for threshold in thresholds
    }

    bucket_properties['__debug__'] = {
        'type': 'string',
        'index': 'not_analyzed'
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
        'date_bucketed': {
            'type': 'date',
            # Do not index, because our analysis has not studied this yet!
            # Plus, Elastic won't index anyway...
            'index': 'not_analyzed'
        }
    }

def debug_print_json(body, header='🔅 🔆 🔅 🔆 🔅 🔆 🔅 '):
    import sys, json
    # Write the query!
    sys.stderr.write('\n{header}\n\n'
                     '{json}\n\n'.format(header=header,
                                         json=json.dumps(body, indent=4, default=repr)))



