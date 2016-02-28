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

from flask import json, jsonify, request, make_response


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
