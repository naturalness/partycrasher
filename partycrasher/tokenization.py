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

class Tokenization(object):
    def __init__(self, lowercase):
        self.lowercase = lowercase

class StandardUnicode(Tokenization):
    """MLT with an analyzer breaking on spaces and then lowercasing"""
    def analysis(self):
        if self.lowercase:
            filter_ = ['lowercase']
        else:
            filter_ = []
        return {
            'type': 'custom',
            'char_filter': [],
            'tokenizer': 'standard',
            'filter': filter_,
            }

class Letters(Tokenization):
    """MLT with a diffrent analyzer (capture letter strings then optionally make them lowercase)"""
    def analysis(self):
        if self.lowercase:
            tokenizer = 'lowercase'
        else:
            tokenizer = 'letter'
        return {
            'type': 'custom',
            'char_filter': [],
            'tokenizer': tokenizer,
            'filter': [],
            }


class Identifier(Tokenization):
    """MLT with an analyzer intended to capture programming words"""
    def analysis(self):
        return {
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
    
class CamelCase(Tokenization):
    """MLT intended to break up identifiers into sub-words"""
    def create_index(self):
        return {
            'type': 'pattern',
            # From ES Docs: https://github.com/elastic/elasticsearch/blob/1.6/docs/reference/analysis/analyzers/pattern-analyzer.asciidoc
            # 2016-01-27
            'pattern': '([^\\p{L}\\d]+)|(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)|(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])',
            'lowercase': self.lowercase,
            }

class Lerch(Tokenization):
    """MLT with an analyzer as described in Lerch, 2013"""
    def filter(self):
        return {
            'lerch': {
                'type': 'length',
                'min': 4,
                'max': 2000,
                },
            }
    
    def tokenizer(self):
        return {
            'lerch': {
                'type': 'pattern',
                'pattern': '\W+',
                'group': -1,
                },
            }
    
    def analyzer(self):
        return {
            'type': 'custom',
            'char_filter': [],
            'tokenizer': 'lerch',
            'filter': ['lowercase', 'lerch'],
        }
