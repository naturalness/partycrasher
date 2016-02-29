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

import re

from flask import json, jsonify, request, make_response, url_for


class BadRequest(RuntimeError):
    """
    Raised and handled when something funky happens.
    """
    def __init__(self, *args, **kwargs):
        super(BadRequest, self).__init__(*args)
        self.fields = kwargs

    def make_response(self):
        message = self.message if self.message else 'Bad Request'
        return jsonify(message=self.message, **self.fields)


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


def href(route, *args, **kwargs):
    """
    Like url_for(), but returns a dictionary, with a key ``href`` which is the
    external-facing URL for the service.
    """

    host = determine_user_agent_facing_host()
    path = url_for(route, *args, **kwargs)
    # TODO: Methods; should also add methods!
    return {'href': host + path, 'method': ['GET']}


def host_from_forwarded_header(content):
    pairs = dict(parse_forwarded_pair(segment)
                 for segment in cleave(';', content))
    try:
        hostname = pairs['host']
        scheme = pairs['proto']
    except KeyError:
        raise UnknownHostError("Forwarded header does not contain host "
                               "and/or proto")
    return scheme + '://' + hostname


def first_of(dictionary, *keys):
    for key in keys:
        if key in dictionary:
            return dictionary[key]
    raise KeyError(keys)


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


def parse_forwarded_pair(pair_text):
    key, value = cleave('=', pair_text.strip(), 2)
    return (key, value.strip('"'))


def cleave(separator, string, maxsplit=0):
    return re.split(r'\s*' + separator + r'\s*', string, maxsplit)


def determine_user_agent_facing_host():
    if 'Forwarded' in request.headers:
        return host_from_forwarded_header(request.headers['Forwarded'])
    elif 'X-Forwarded-Host' in request.headers:
        return host_from_legacy_headers(request.headers)
    else:
        return request.url_root.rstrip('/')
