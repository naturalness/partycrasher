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

from __future__ import print_function, division

from six import string_types

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

from elasticsearch import TransportError
from elasticsearch import ElasticsearchException

from partycrasher.threshold import Threshold
from partycrasher.more_like_this import MoreLikeThis
from partycrasher.es.elastify import elastify
from partycrasher.pc_exceptions import ESError

class ESIndex(object):
    """
    Superclass for bucketers which require pre-existing data to work.
    The default analyzer breaks on whitespace.
    """

    def __init__(self, 
                 esstore,
                 config,
                 tokenization,
                 thresholds):
        
        self.index_base = config.ElasticSearch.indexbase
        self.esstore = esstore
        self.config = config
        self.tokenization = tokenization
        self.thresholds = thresholds

        self.index_number_of_shards = self.config.ElasticSearch.number_of_shards
        self.index_number_of_replicas = self.config.ElasticSearch.number_of_replicas
        self.index_translog_durability = self.config.ElasticSearch.translog_durability
        self.index_throttle_type = self.config.ElasticSearch.throttle_type
        self.similarity = self.config.ElasticSearch.similarity
        self.similarity_k1 = self.config.ElasticSearch.similarity_k1
        self.similarity_b = self.config.ElasticSearch.similarity_b
        
        
    @property
    def es_index(self):
        """
        Configured ES index
        """
        return self.index_base

    @property
    def allow_delete_all(self):
        """
        Whether or not the instance should allow all data to be deleted at once
        """
        return self.config.ElasticSearch.allow_delete_all


    def _create_index(self):
        index_config={
            'mappings': {
                'crash': {
                    'properties': self.common_properties(),
                    'dynamic_templates': [
                      {
                        'data': {
                          'match': '*',
                          'match_mapping_type': 'string',
                          'mapping': {
                            'type': 'text',
                            'analyzer': 'default',
                            # The ES documentation indicates this should improve
                            # speed but it doesn't seem to actually do so
                            #'term_vector': 'yes',
                            # This can enable a second tokenizer for every field
                            #'fields': {
                                #'ws': {
                                    #'type': 'text',
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
                        'default': self.tokenization.analyzer()
                        }
                    },
                'index': self.index_settings(),
                }
            }
        # allow tokenization to set up more things that its analyzer needs
        if hasattr(self.tokenization, 'filter'):
            index_config['settings']['analysis']['filter'] = (
                self.tokenization.filter())
        if hasattr(self.tokenization, 'tokenizer'):
            index_config['settings']['analysis']['tokenizer'] = (
                self.tokenization.tokenizer())
        tokenization_name = self.tokenization.__class__.__name__
        warn("Creating index %s using tokenization %s" % (self.index_base,
                                                          tokenization_name
                                                          ))
        try:
            return self.esstore.indices.create(index=self.index_base, 
                                               body=index_config)
        except TransportError as e:
            error(e.info)
            raise
                
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
    
    def delete_and_recreate_index(self):
        """
        Deletes the entire index and recreates it. This destroys all of the
        reports.
        """
        assert self.allow_delete_all
        self.esstore.yellow()
        self.esstore.indices.delete(index=self.index_base)
        self.esstore.yellow()
        self._create_index()
        self.esstore.yellow()
    
    def ensure_index_exists(self):
        if not self.esstore.indices.exists(self.index_base):
            self._create_index();
        
    @property
    def thresh(self):
        return self.thresholds[0]

    @property
    def min_threshold(self):
        return self.thresholds[0]

    def common_properties(self):
        """
        Returns properties common to all indexes;
        must provide the threshold values
        """
        thresholds = self.thresholds

        string_not_analyzed = {
            'type': 'keyword',
        }

        bucket_properties = {
            threshold.to_elasticsearch(): string_not_analyzed
                for threshold in thresholds
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
        properties = {
            # TODO: convert into _id
            'database_id': string_not_analyzed,
            'buckets': {
                # Do not allow arbitrary properties being added to buckets...
                "dynamic" : "strict",
                # Create all the subfield appropriate for buckets
                "properties": bucket_properties
            },
            'project': string_not_analyzed,
            'type': string_not_analyzed,
            'date': {
                'type': 'date',
            },
            'stacktrace': { 
                'properties': {
                    'function': {
                        'type': 'text',
                        'analyzer': 'default',
                        # Enable a second tokenizer
                        # This is used for chopping off the tops of stacks
                        # automatically
                        'fields': {
                            'whole': {
                                'type': 'keyword',
                                # Documentation suggests this would be helpful
                                # for performance but doesn't seem to actually
                                # improve performance
                                #'term_vector': 'yes',
                                }
                            }
                        }
                    }
                }
            }
        for f in self.config.UserInterface.fixed_summary_fields.keys():
            properties[f] = string_not_analyzed
        return properties
    
   
    # SMURT Proxy to the ES API
    def search(self, body, **kwargs):
        assert 'index' not in kwargs
        if isinstance(body, string_types):
            pass
        else:
            body=elastify(body)
        tries = 0
        while True:
            tries += 1
            try:
                return self.esstore.es.search(
                    index=self.index_base,
                    body=body,
                    **kwargs)
            except ElasticsearchException as e:
                if (tries <= 1):
                    self.esstore.yellow()
                else:
                    raise ESError(e)
            
    
    def get(self, **kwargs):
        assert 'index' not in kwargs
        return self.esstore.es.get(index=self.index_base, **kwargs)

    def create(self, **kwargs):
        assert 'index' not in kwargs
        return self.esstore.es.create(index=self.index_base, **kwargs)

    @property
    def name(self):
        return self.index_base
