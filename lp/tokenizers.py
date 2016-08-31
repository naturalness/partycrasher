#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TOKENIZERS FOR THE TOKENIZING GOD!
"""


from __future__ import unicode_literals, print_function

import regex
import six
import sys


class PatternTokenizer(object):
    """
    A tokenizer based on a splitting regular expression.
    >>> lerch('a little bit of tea') == ['little']
    True
    >>> camel('call MooseX::FTPClass2_beta') == ["call", "Moose", "X", "FTP", "Class", "2", "beta"]
    True
    >>> camel('hello world') == ['hello', 'world']
    True
    """
    def __init__(self, pattern, transform=None,
                 min_length=None, max_length=None):
        self.pattern = regex.compile(pattern, regex.VERSION1)
        self.min = min_length or 0
        self.max = max_length or float('infinity')
        self.transform = transform or (lambda x: x)

    def __call__(self, string):
        #print(string, file=sys.stderr)
        tokens = self.pattern.splititer(self.transform(string))
        min_len = self.min
        max_len = self.max
        return [token for token in tokens
                if token and min_len <= len(token) <= max_len]


# From ES Docs: https://github.com/elastic/elasticsearch/blob/1.6/docs/reference/analysis/analyzers/pattern-analyzer.asciidoc
# 2016-01-27
camel = PatternTokenizer(
    '(?:[^\\p{L}\\d]+)|'
    '(?<=\\D)(?=\\d)|'
    '(?<=\\d)(?=\\D)|'
    '(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|'
    '(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])'
)
lerch = PatternTokenizer('\W+',
                         transform=six.text_type.lower,
                         min_length=4,
                         max_length=2000)
space = PatternTokenizer('\s+')
