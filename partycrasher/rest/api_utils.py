#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016  Eddie Antonio Santos <easantos@ualberta.ca>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Utilties used in rest_service; these are kept here to unclutter the API file.
"""

from six import string_types, text_type

import weakref
import re
import distutils
import sys
import traceback

from flask import json, jsonify, request, redirect, make_response, url_for

from partycrasher.pc_encoder import pretty
from partycrasher.pc_exceptions import PartyCrasherError
from partycrasher.pc_type import maybe_date, maybe_int
from partycrasher.project import multi_project
from partycrasher.crash_type import multi_crash_type

import logging
logger = logging.getLogger(__name__)
ERROR = logger.error
WARN = logger.warn
INFO = logger.info
DEBUG = logger.debug

class BadRequest(PartyCrasherError):
    """
    Raised and handled when something funky happens.
    """
    http_code = 400
    
    def __init__(self, *args, **kwargs):
        super(BadRequest, self).__init__(*args)
        self.fields = kwargs

    def get_extra(self):
        return self.fields

class UnknownHostError(PartyCrasherError):
    """
    Raised when we could not determine the original host.
    """

class KeyConflictError(BadRequest):
    """
    Raised when the user provides a search with conflicting parameters.
    """

def jsonify_list(seq):
    """
    Same as jsonify, but works on lists. Flask's JSONify doesn't support this
    because attackers can override Array's constructor to collect data when
    JSON is transferted as application/javascript.
    """
    # Coerce to list
    assert isinstance(seq, list)

    should_indent = not (request.headers.get('X-Requested-With', '') ==
                         'XMLHttpRequest')
    body = json.dumps(seq, indent=4 if should_indent else None)

    return make_response((body, None, {'Content-Type': 'application/json'}))

def redirect_with_query_string(url, *args, **kwargs):
    """
    Like `flask.redirect` but appends the query string.

    Requires an active request context.
    """

    query_string = request.environ.get('QUERY_STRING')
    full_url = url + '?' + query_string if query_string else url
    return redirect(full_url, *args, **kwargs)

cached_urls = {}

def full_url_for(route, **kwargs):
    """
    Like url_for(), but returns a fully qualified external-facing URL for the
    service.
    """
    global cached_urls
    for k, v in kwargs.items():
        assert v is not None
        assert k is not None
    assert route is not None
    host = determine_user_agent_facing_host()
    urlh = tuple([route] + list(kwargs.items()))
    if urlh in cached_urls:
        path = cached_urls[urlh]
    else:
        path = url_for(route, **kwargs)
        if len(cached_urls) > 100000:
            cached_urls = {}
        cached_urls[urlh] = path
    # TODO: List allowed methods, so we don't have to do an OPTIONS request. 
    return host + path
  

# So that `determine user agent facing host` only needs to figure out the host
# once, even it gets called 1000s of times per request.
# Once the request leaves the system, the entry will automatically be popped
# out of this dictionary.
HOST_CACHE = weakref.WeakKeyDictionary()


def determine_user_agent_facing_host():
    """
    Determines the host for the active request as seen by the User-Agent
    (client), assuming proxies along the way have been being truthful.
    """

    # Request is a proxy object, and cannot be weakly-referenced; instead,
    # get a reference to true object.
    true_request = request._get_current_object()
    if true_request in HOST_CACHE:
        return HOST_CACHE[true_request]
    else:
        host = calculate_user_agent_facing_host()
        HOST_CACHE[true_request] = host
        return host


def calculate_user_agent_facing_host():
    """
    Does the hard work of determining the true host. Lots of string parsing
    and string concatenation be here.
    """
    if 'Forwarded' in request.headers:
        return host_from_forwarded_header(request.headers['Forwarded'])
    elif 'X-Forwarded-Host' in request.headers:
        return host_from_legacy_headers(request.headers)
    else:
        return request.url_root.rstrip('/')


def host_from_forwarded_header(content):
    """
    Parses according to [RFC7239]

    https://tools.ietf.org/html/rfc7239#section-5
    """
    pairs = parse_forwarded_header(content)

    try:
        hostname = pairs['host']
        scheme = pairs['proto']
    except KeyError:
        raise UnknownHostError("Forwarded header does not contain host "
                               "and/or protocol")
    return scheme + '://' + hostname


def host_from_legacy_headers(headers):
    try:
        scheme = first_of(headers,
                          'X-Forwarded-Proto',
                          'X-Forwarded-Protocol')
        hostname = headers['X-Forwarded-Host']
    except KeyError:
        raise UnknownHostError('Could not determine host from legacy '
                               'forwarding headers')
    return scheme + '://' + hostname


def parse_forwarded_header(content):
    """
    Broken parser for RFC 7239 Section 5
    Won't work if the quotes contain commas semicolons or equals
    """
    proxies = content.split(',')
    proxy = proxies[0]
    pairs = proxy.split(';')
    parameters = {}
    for pair in pairs:
        (left, right) = pair.split('=')
        left = re.sub(r'[\s"]+', '', left).lower()
        right = re.sub(r'[\s"]+', '', right).lower()
        parameters[left] = right
    return parameters

def first_of(dictionary, *keys):
    for key in keys:
        if key in dictionary:
            return dictionary[key]
    raise KeyError(keys)

def str_to_bool(s, default):
    if s is None:
        return default
    assert isinstance(s, string_types)
    return bool(distutils.util.strtobool(s.lower()))

def maybe_set(d, k, v):
    if k in d:
        if v is None:
            pass
        elif d[k] is None:
            d[k] = v
        elif d[k] != v:
            raise KeyConflictError(key=k,
                                   value_a=d[k],
                                   value_b=v)
    else:
        d[k] = v
    return d

def merge(d, dest, src):
    if dest in d:
        if src in d:
            raise KeyConflictError(key=dest,
                                   value_a=d[dest],
                                   value_b=d[src])
        else:
            pass
    else:
        if src in d:
            d[dest]=d[src]
            del d[src]
        else:
            pass

def make_search(args, **kwargs):
    s = kwargs
    merge(args, 'from', 'from_')
    maybe_set(s, 'from', maybe_int(args.get('from', None)))
    maybe_set(s, 'size', maybe_int(args.get('size', None)))
    maybe_set(s, 'query_string', args.get('q', None))
    maybe_set(s, 'since', maybe_date(args.get('since', None)))
    maybe_set(s, 'until', maybe_date(args.get('until', None)))
    merge(args, 'project', 'projects')
    maybe_set(s, 'project', multi_project(args.get('project', None)))
    merge(args, 'type', 'type_')
    merge(args, 'type', 'types')
    maybe_set(s, 'type', multi_crash_type(args.get('type', None)))
    merge(args, 'threshold', 'thresholds')
    maybe_set(s, 'threshold', args.get('threshold', None))
    merge(args, 'bucket_id', 'buckets')
    merge(args, 'bucket_id', 'bucket')
    maybe_set(s, 'bucket_id', args.get('bucket_id', None))
    return s

def json_exception(t, v, tb):
    for line in traceback.format_exception(t, v, tb):
        ERROR(line.rstrip())
    details = {
        'message': str(v),
        'error': t.__name__,
        'stacktrace': tb,
        }
    if hasattr(v, 'get_extra'):
        details.update(v.get_extra())
    return details

    
