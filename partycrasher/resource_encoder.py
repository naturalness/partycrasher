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

from datetime import datetime
from collections import OrderedDict
from partycrasher.crash import Crash, CrashEncoder
from partycrasher.project import Project
from partycrasher.threshold import Threshold
from partycrasher.bucket import Bucket, TopMatch
from partycrasher.rest_api_utils import full_url_for

from flask import json, request, redirect, make_response

class ResourceEncoder(CrashEncoder):
    def default(self, o):
        if isinstance(o, Threshold):
            return str(o)
        if isinstance(o, Crash):
            d = super(ResourceEncoder, self).default(o).copy()
            d['href'] = full_url_for('view_report',
                                     project=o.project,
                                     report_id=o.id
                                     )
            return d
        if isinstance(o, Bucket):
            d = super(ResourceEncoder, self).default(o).copy()
            if 'project' in d and d['project'] is not None:
                d['href'] = full_url_for('view_bucket',
                                     threshold=o.threshold,
                                     bucket_id=o.id,
                                     project=o.project
                                     )
            else:
                d['href'] = full_url_for('view_bucket_no_project',
                                     threshold=o.threshold,
                                     bucket_id=o.id
                                     )
            return d
        if isinstance(o, Project):
            d = {
              'name': super(ResourceEncoder, self).default(o),
              'href': full_url_for('query_buckets',
                                     threshold='4.0',
                                     project=o.name
                                     )
            }
            return d
        if isinstance(o, TopMatch):
            d = super(ResourceEncoder, self).default(o).copy()
            d['href'] = full_url_for('view_report',
                                     project=o.project,
                                     report_id=o.report_id
                                     )
            return d
        if isinstance(o, Report):
            d = {
                'report': o.crash,
                'saved': o.saved,
                }
            if o.explain:
                d['explanation'] = o.explanation
            return d
        else:
            return super(ResourceEncoder, self).default(o)

def fix_buckets(crash_dict):
    """
    Fixes the keys from a crash dictionary.
    """
    if 'buckets' not in crash_dict:
        return

    project = crash_dict['project']

    fixed_buckets = {}
    for key, bucket_id in crash_dict['buckets'].items():
        if key == 'top_match':
            fixed_buckets['top_match'] = serialize_top_match(bucket_id)
        else:
            threshold = str(Threshold(key))
            fixed_buckets[threshold] = Bucket(id=bucket_id,
                                              project=project,
                                              threshold=threshold,
                                              total=None,
                                              top_reports=None,
                                              first_seen=None)

    crash_dict['buckets' ] = fixed_buckets


def serialize_top_match(info):
    # See: bucketer.MLT.make_matching_buckets()
    if info is not None:
        match_url = href('view_report',
                         project=info['project'],
                         report_id=info['report_id'])
        return OrderedDict([
            ('report_id', info['report_id']),
            ('href', match_url['href']),
            ('project', info['project']),
            ('score', info['score']),
        ])
    else:
        return None

