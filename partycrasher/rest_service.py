#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2016 Joshua Charles Campbell
#  Copyright (C) 2016 Eddie Antonio Santos

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

import sys
import os

from flask import Flask, jsonify, request, url_for
from flask.ext.cors import CORS

# Hacky things to add PartyCrasher to the path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import partycrasher

from partycrasher.rest_api_utils import BadRequest, jsonify_list, href

app = Flask('partycrasher')
CORS(app)
crasher = partycrasher.PartyCrasher()


@app.errorhandler(BadRequest)
def on_bad_request(error):
    """
    Handles BadRequest exceptions; sends status 400 back to the client,
    along with a message sent as JSON.
    """
    return error.make_response(), 400


@app.route('/')
def root():
    """
    .. api-doc-order: 0

    Conventions
    ===========

    Resource Links
    --------------

    Resources may be projects, buckets, reports, and other such entities.

    A resources contains its hyperlink reference (i.e., URL), acceptable HTTP
    methods, and (sometimes) its `link relation`_.

    .. _link relation: http://www.iana.org/assignments/link-relations/link-relations.xhtml

    ``methods`` lists any allowable HTTP methods *in addition* to ``OPTIONS``.
    The same information can be obtained by issuing an ``OPTIONS`` request to
    the ``href`` and parsing the ``ALLOW`` field in the response.

    .. code-block:: json

        {
            "resource": {
                "href": "http://domain.tld/path/to/resource",
                "rel": "",
                "methods": [
                    "GET"
                ]
            }
        }

    .. code-block:: none

        partycrasher
        ├── alan_parsons
        │   ├── buckets
        │   ├── config
        │   └── reports
        │       └── dry_run
        ├── buckets
        ├── config
        └── reports
            └── dry_run

    .. The root route; I'm really rooting for it.

    """

    # This should be a tree for all of the services available.
    return jsonify(partycrasher=
                   {
                       'version': partycrasher.__version__,
                       'elastic': crasher.esServers,
                       'elastic_health': crasher.es.cluster.health()
                   },
                   self=dict(href('root'), rel='canonical'),
                   projects="NOT-IMPLEMENTED",
                   config={
                       'default_threshold': 4.0
                   })


@app.route('/reports', methods=['POST'])
@app.route('/<project>/reports', methods=['POST'])
def add_report(project=None):
    """
    .. api-doc-order: 1
    .. _upload-single:

    Upload a new report
    ===================

    ::

        POST /:project/reports HTTP/1.1

    or

    ::

        POST /reports HTTP/1.1

    Uploads a new report. The report should be sent as a JSON Object with at
    least a unique ``database_id`` property. If uploaded to
    ``/:project/reports``, the ``project`` property will automatically be set.

    The response contains the bucket assignments, as well as the canonical URL
    to access the report.

    ::

        HTTP/1.1 201 Created
        Location: https://your.host/<project>/report/<report-id>/

    .. code-block:: JSON

        {
            "id": "<report-id>",
            "self": {
                "href": "https://domain.tld/<project>/reports/<bucket-id>"
            },
            "bucket": {
                "id": "<bucket-id>",
                "href": "https://domain.tld/<project>/buckets/<T=[default]>/<bucket-id>"
                "rel": "canonical"
            }
        }

    Errors
    ------

    When an *identical* (not just duplicate) report is posted::

        HTTP/1.1 303 See Other
        Location: https://domain.tld/<project>/report/<report-id>/

    When a report is posted to a ``:project/`` URL, but the report declares it
    belongs to a different project::

        HTTP/1.1 400 Bad Request


    Upload multiple new reports
    ===========================

    ::

        POST /:project/reports HTTP/1.1

    or

    ::

        POST /reports HTTP/1.1

    Send multiple reports (formatted as in :ref:`upload-single`) bundled up
    in a JSON Array (list). The response is a JSON Array of report results.
    Similar errors and statuses apply.

    ::

        HTTP/1.1 201 Created

    .. code-block:: json

        [
            {
                "id": "<report-id 1>",
                "bucket_id": "<bucket-id 1>",
                "bucket_url": "https://domain.tld/<project>/buckets/<T=[default]>/<bucket-id 1>"
            },
            {
                "id": "<report-id 2>",
                "bucket_id": "<bucket-id 2>",
                "bucket_url": "https://domain.tld/<project>/buckets/<T=[default]>/<bucket-id 2>"
            }
        ]

    Errors
    ------

    When an *identical* (not just duplicate) report is posted::

        HTTP/1.1 303 See Other
        Location: https://domain.tld/<project>/report/<report-id>/

    When a report is posted to a ``:project/`` URL, but the report declares it
    belongs to a different project::

        HTTP/1.1 400 Bad Request
    """

    report = request.get_json()

    if isinstance(report, list):
        return jsonify_list(ingest_multiple(report, project)), 201
    else:
        report, url = ingest_one(report, project)
        return jsonify(report), 201, {
            'Location': url
        }


@app.route('/reports/<report_id>',
           defaults={'project': None},
           endpoint='view_report_no_project')
@app.route('/<project>/reports/<report_id>')
def view_report(project=None, report_id=None):
    """
    .. api-doc-order: 2

    Get information on a report
    ===========================

    ::

        GET /:project/reports/:report_id HTTP/1.1

    or

    ::

        GET /reports/:report_id HTTP/1.1

    ::

        HTTP/1.1 200 OK
        Link: <https://domain.tld/<project>/buckets/<T=[default]>/<bucket-id>; rel="related"

    .. code-block:: json

        {
            "id": "<report-id>",
            "buckets": {
                "3.5": {
                    "id": "<bucket-id, T=3.5>",
                    "url": "https://domain.tld/<project>/buckets/3.5/<bucket-id>"
                },
                "4.0": {
                    "id": "<bucket-id, T=4.0>",
                    "url": "https://domain.tld/<project>/buckets/4.0/<bucket-id>"
                },
                "4.5": {
                    "id": "<bucket-id, T=3.5>",
                    "url": "https://domain.tld/<project>/buckets/4.5/<bucket-id>"
                }
            },
            "threads": [
                {
                    "stacktrace": ["..."]
                }
            ],
            "comment": "<some flattering and not-at-all insulting comment about your software>",
            "os": "<os>",
            "platform": "<x86/arm, etc.>"
        }

    """
    # Ignore project.
    assert report_id is not None

    try:
        report = crasher.get_crash(report_id)
    except partycrasher.ReportNotFoundError:
        return jsonify(not_found=report_id), 404
    else:
        return jsonify(report)


@app.route('/<project>/reports/')
def reports_overview(project=None):
    raise NotImplementedError()


@app.route('/<project>/config')
def get_project_config(project=None):
    """
    .. api-doc-order: 100

    View per-project configuration
    ==============================

    ::

        GET /:project/config HTTP/1.1

    ::

        HTTP/1.1 200 OK

    .. code-block:: json

        {
            "default_threshold": 4.0
        }

    """

    return jsonify(default_threshold=4.0)


@app.route('/<project>/config', methods=['PATCH'])
def update_project_config(project=None):
    """
    .. api-doc-order: 100.0

    Set per-project configuration
    =============================

    ::

        PATCH /:project/config HTTP/1.1

    Data:

    .. code-block:: json

        {
            "default-threshold": 3.5
        }

    ::

        HTTP/1.1 200 OK

    .. code-block:: json

        {
            "default-threshold": 3.5
        }

    """
    raise NotImplementedError()

#############################################################################
#                                 Utilities                                 #
#############################################################################


def ingest_one(report, project_name):
    """
    Returns a tuple of ingested report and its URL.
    """

    raise_bad_request_if_project_mismatch(report, project_name)
    # Graft the project name onto the report.
    report.setdefault('project', project_name)

    report = crasher.ingest(report)
    url = url_for('view_report',
                  project=report['project'],
                  report_id=report['database_id'])
    return report, url


def ingest_multiple(reports, project_name):
    """
    Same as ingest_one, but takes a list of reports, and returns a list of
    reports.
    """
    return [ingest_one(report, project_name)[0] for report in reports]


def raise_bad_request_if_project_mismatch(report, project_name):
    """
    Checks if the project in the report and the given project name are the
    same.
    """
    if 'project' not in report:
        if project_name is None:
            # No project name anywhere. This is not good...
            raise BadRequest('Missing project name',
                             error="missing_project")
    elif project_name and project_name != report['project']:
        message = ("Project name mismatch: "
                   "Posted a report to '{0!s}' "
                   "but the report claims it's from '{1!s}'"
                   .format(project_name, report['project']))
        raise BadRequest(message,
                         error="name_mismatch",
                         expected=project_name,
                         actual=report['project'])


def main():
    if len(sys.argv) > 1:
        app.run(debug=True, port=int(sys.argv[1]))
    else:
        app.run(debug=True)


if __name__ == '__main__':
    main()
