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

import weakref
import re

from flask import json, jsonify, request, redirect, make_response, url_for


class BadRequest(RuntimeError):
    """
    Raised and handled when something funky happens.
    """
    def __init__(self, *args, **kwargs):
        super(BadRequest, self).__init__(*args)
        self.fields = kwargs

    def make_response(self):
        if hasattr(self, 'message'):
            message = self.message
        else:
            message = 'Bad Request'
        return jsonify(message=message, **self.fields)


class UnknownHostError(RuntimeError):
    """
    Raised when we could not determine the original host.
    """


def jsonify_list(seq):
    """
    Same as jsonify, but works on lists. Flask's JSONify doesn't support this
    because attackers can override Array's constructor to collect data when
    JSON is transferted as application/javascript.
    """
    # Coerce to list
    if not isinstance(seq, list):
        seq = list(seq)

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

def full_url_for(route, **kwargs):
    """
    Like url_for(), but returns a fully qualified external-facing URL for the
    service.
    """

    host = determine_user_agent_facing_host()
    path = url_for(route, **kwargs)
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
