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

import os
import sys
import time

from flask import jsonify, request, url_for, redirect
from flask.ext.cors import CORS

# Hacky things to add PartyCrasher to the path.
REPOSITORY_ROUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPOSITORY_ROUTE)
import partycrasher

from partycrasher.make_json_app import make_json_app
from partycrasher.rest_api_utils import (
    BadRequest,
    jsonify_list,
    href,
    redirect_with_query_string,
)
from partycrasher.resource_encoder import ResourceEncoder

import dateparser

# Create and customize the Flask app.
app = make_json_app('partycrasher')
CORS(app)
app.json_encoder = ResourceEncoder

# HACK! This shouldn't be hard-coded!
with open(os.path.join(REPOSITORY_ROUTE, 'partycrasher.cfg')) as config_file:
    crasher = partycrasher.PartyCrasher(config_file)


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

    # Projects query:
    #
    #   {"aggs":{"projects":{"terms":{"field":"project"}}}}
    #
    #   result['aggregations']['projects']['buckets']

    # This should be a tree for all of the services available.
    return jsonify(self=dict(href('root'), rel='canonical'),
                   partycrasher={
                       'version': partycrasher.__version__,
                       'elastic': crasher.esServers,
                       'elastic_health': crasher.es.cluster.health()
                   },
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

    Get an existing report
    ======================
    ::

        GET /:project/reports/:report_id HTTP/1.1

    or

    ::

        GET /reports/:report_id HTTP/1.1

    Fetches a processed report from the database.  This includes all data
    originally posted, plus bucket assignments, and the URLs for every
    relevant resource (buckets and project).

    .. warning::

        Due to ElasticSearch's `Near Realtime`_ nature, when you ``GET`` a report
        immediately after a ``POST`` or a ``DELETE`` may not result in what you'd
        expect! Usually, it takes a few seconds for any changes to fully
        propagate throughout the database.

    .. _Near Realtime: https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html#_near_realtime_nrt


    ::

        HTTP/1.1 200 OK
        Link: <https://domain.tld/<project>/buckets/<T=[default]>/<bucket-id>; rel="related"

    .. code-block:: json

        {
            "database_id": "<report-id>",
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


@app.route('/reports/dry-run', methods=['POST'])
@app.route('/<project>/reports/dry-run', methods=['POST'])
def ask_about_report(project=None):
    """
    .. api-doc-order: 1.5

    Upload a report (dry-run)
    =========================

    ::

        POST /:project/reports/dry-run HTTP/1.1

    or

    ::

        POST /reports/dry-run HTTP/1.1

    Answers the question: what bucket would this report be assigned to? This
    does **NOT** store or keep track of the report! Use :ref:`upload-single`
    to commit reports to the database.

    ::

        HTTP/1.1 200 OK

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

    """

    report = request.get_json()
    assigned_report, _url = ingest_one(report, project, dryrun=True)
    return jsonify(assigned_report), 200


@app.route('/reports/<report_id>', methods=['DELETE'],
           defaults={'project': None},
           endpoint='delete_report_no_project')
@app.route('/<project>/reports/<report_id>', methods=['DELETE'])
def delete_report(project=None, report_id=None):
    """
    .. api-doc-order: 3

    Delete an existing report
    =========================
    ::

        DELETE /:project/reports/:report_id HTTP/1.1

    or

    ::

        DELETE /reports/:report_id HTTP/1.1

    Deletes an existing report from the database.

    ::

        HTTP/1.1 200 OK

    """
    # Ignore project.
    assert report_id is not None
    raise NotImplementedError

@app.route('/buckets/<threshold>/<bucket_id>',
           defaults={'project': None},
           endpoint='view_bucket_no_project')
@app.route('/<project>/buckets/<threshold>/<bucket_id>')
def view_bucket(project=None, threshold=None, bucket_id=None):
    """
    .. api-doc-order: 15

    [view bucket documentation pending...]
    """
    assert bucket_id is not None
    assert threshold is not None

    try:
        bucket = crasher.bucket(threshold, bucket_id)
    except partycrasher.BucketNotFoundError:
        return jsonify(not_found=bucket_id), 404

    return jsonify(bucket.to_dict())


# Undoucmented endpoint:
# Automatically redirects to the real endpoint.
@app.route('/buckets',
           defaults={'project': None},
           endpoint='query_default_buckets_no_project')
@app.route('/<project>/buckets')
def query_default_buckets(project=None):
    if project is None:
        appropriate_url = url_for('query_buckets_no_project',
                                  threshold=crasher.default_threshold)
    else:
        appropriate_url = url_for('query_buckets',
                                  threshold=crasher.default_threshold,
                                  project=project)
    # Redirect with "Found" semantics.
    return redirect_with_query_string(appropriate_url, 302)


@app.route('/buckets/<threshold>',
           defaults={'project': None},
           endpoint='query_buckets_no_project')
@app.route('/<project>/buckets/<threshold>')
def query_buckets(project=None, threshold=None):
    """
    .. api-doc-order: 10

    Get the top buckets in the recent past
    ======================================

    ::

        GET /:project/buckets HTTP/1.1

    or

    ::

        GET /:project/buckets HTTP/1.1

    Find top buckets for a given time-frame. If queried  on a ``:project``
    route, implicitly filters by project.

    Query parameters
    ----------------

    .. this is the proposed version of this table:
        +-------------+--------------+-------------------------------------------+
        | Parameter   | Values       | Description                               |
        +-------------+--------------+-------------------------------------------+
        | ``since``   | Start time   | From when to count top buckets.           |
        +-------------+--------------+-------------------------------------------+
        | ``project`` | Project name | Limit to this project only; implied if    |
        |             |              | using a ``/:project/`` endpoint.          |
        +-------------+--------------+-------------------------------------------+
        | ``version`` | Version id   | Limit to this version only.               |
        +------------------------------------------------------------------------+

    +-------------+--------------+-------------------------------------------+
    | Parameter   | Values       | Description                               |
    +-------------+--------------+-------------------------------------------+
    | ``since``   | Start date   | Grab buckets since this date, represented |
    |             |              | as an ISO 8601 date/time value            |
    |             |              | (i.e, YYYY-MM-DD).                        |
    +-------------+--------------+-------------------------------------------+
    | ``project`` | Project name | Limit to this project only; implied if    |
    |             |              | using a ``/:project/`` endpoint.          |
    +-------------+--------------+-------------------------------------------+


    Example
    -------

    ::

        GET /alan_parsons/buckets?since=2016-02-29 HTTP/1.1
        Host: domain.tld

    ::

        HTTP/1.0 200 OK
        Content-Type: application/json

    .. code-block:: JSON

        {
            "since": "2016-02-29T00:00:00",
            "threshold": "4.0",
            "top_buckets": [
                {
                    "href": "http://domain.tld/alan_parsons/buckets/4.0/bucket:c29a81a0-5a53-4ba0-8123-5e96685a5895",
                    "id": "bucket:c29a81a0-5a53-4ba0-8123-5e96685a5895",
                    "method": [ "GET" ],
                    "total": 253
                }
            ]
        }

    """
    assert threshold is not None

    since = request.args.get('since', '3-days-ago')
    try:
        lower_bound = dateparser.parse(since.replace('-', ' '))
    except ValueError:
        lower_bound = None
    if lower_bound is None:
        raise BadRequest('Could not understand date format for '
                         '`since=` parameter. '
                         'Supported formats are: ISO 8601 timestamps '
                         'and relative dates. Refer to the API docs for '
                         'more information: '
                         'http://partycrasher.rtfd.org/',
                         since=since)

    buckets = crasher.top_buckets(lower_bound,
                                  project=project,
                                  threshold=threshold)

    # Reformat the results...
    #top_buckets = [bucket.to_dict(href('view_bucket',
    #                                   project=project,
    #                                   threshold=threshold,
    #                                   bucket_id=bucket.id))
    #               for bucket in buckets]
    top_buckets = list(buckets)

    return jsonify(since=lower_bound.isoformat(),
                   threshold=threshold,
                   top_buckets=top_buckets)


@app.route('/<project>/reports/')
def reports_overview(project=None):
    raise NotImplementedError


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


# This route is not ready for release yet.
if False:
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


def ingest_one(report, project_name, dryrun=False):
    """
    Returns a tuple of ingested report and its URL.
    """

    raise_bad_request_if_project_mismatch(report, project_name)
    # Graft the project name onto the report.
    report.setdefault('project', project_name)

    report = crasher.ingest(report, dryrun=dryrun)
    url = url_for('view_report',
                  project=report['project'],
                  report_id=report['database_id'])

    # Commit things to the index such that any new inserts will bucket
    # properly...
    crasher.es.indices.refresh(index='crashes')
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
    kwargs = {
        # Make the server publically visible.
        'host': '0.0.0.0',
        'debug': True,
    }

    # TODO:
    #  - add parameter: -c [config-file]
    #  - add parameter: -C [config-setting]

    # Add port if required.
    if len(sys.argv) > 1:
        kwargs.update(port=int(sys.argv[1]))

    return app.run(**kwargs)


if __name__ == '__main__':
    main()
