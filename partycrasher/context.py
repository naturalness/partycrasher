#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015, 2016, 2017 Joshua Charles Campbell

#  This program is free software; you can reditext_typeibute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is ditext_typeibuted in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from copy import copy
from pydoc import locate

# Do not import anything from api
from partycrasher.config_loader import Config
from partycrasher.threshold import Threshold
from partycrasher.es.store import ESStore
from partycrasher.es.index import ESIndex

import logging
logger = logging.getLogger(__name__)
error = logger.error
warn = logger.warn
info = logger.info
debug = logger.debug

class Context(object):
    """Search API context global holder and config file loader."""
    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.thresholds = list(
            map(Threshold, self.config.Bucketing.thresholds)
            )
        self.es_store = ESStore(self.config.ElasticSearch)
        self.strategy_class = locate(
            self.config.Bucketing.Strategy.strategy)
        self.tokenization_class = locate(
            self.config.Bucketing.Tokenization.tokenization)
        self.tokenization = self.tokenization_class(
            self.config.Bucketing.Tokenization)
        self.index = ESIndex(self.es_store,
                             self.config,
                             self.tokenization,
                             self.thresholds)
        self.index.ensure_index_exists()
        self.strategy = self.strategy_class(
            config=self.config.Bucketing.Strategy,
            index=self.index,
            )
        # Pull configuration details needed for search and fix it up.
        self.fixed_summary_fields = dict(
            self.config.UserInterface.fixed_summary_fields)
        self.fixed_summary_fields["project"] = "Project"
        self.default_threshold = Threshold(
            self.config.Bucketing.default_threshold)
        self.search = self.index.search
        self.allow_delete_all = self.config.ElasticSearch.allow_delete_all
