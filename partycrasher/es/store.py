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
#  Foundation, Inc., 51 Franklin Street, Fith Floor, Boston, MA  02110-1301, USA.

import ESCrash

es_store_instance = None

def es_store():
    if es_store_instance is None:
        return ESStore()
    else:
        return es_store_instance

class ESStore(object):
    """Class representing an elasticsearch server or cluster."""
    
    def __init__(self,
                 config)
    
        self.config=config
        self._es = None
        if es_store_instance is None:
            es_store_instance = self
        else:
            raise RuntimeError("Doesn't support multiple ESStore instances.")
    
    @property
    def es_servers(self):
        """
        Configured ES server list
        """
        return self.config.hosts

    @property
    def es(self):
        """
        Instance of the ElasticSearch python library client.
        """
        if not self._es:
            self._connect_to_elasticsearch()
        return self._es

    def connect(self):
        """
        Establishes a connection to ElasticSearch. given configuration.
        """
        self._es = Elasticsearch(self.es_servers,
                                 retry_on_timeout=True,
                                 )

        # XXX: Monkey-patch our instance to the global. This is why we don't
        # support multiple ESStore instances.
        ESCrash.es = self._es
        if not self._checked_index_exists:
            if self._es.indices.exists(self.es_index):
                self._checked_index_exists = True
            else:
                self._bucketer.create_index()
        self.es.cluster.health(wait_for_status='yellow')
        return self._es
    
    @property
    def indices(self):
        """Return the indices API from the Elasticsearch python library."""
        return self.es.indices
    
    def yellow(self):
        """Wait for status yellow/green on cluster."""
         self.es.cluster.health(wait_for_status='yellow')
