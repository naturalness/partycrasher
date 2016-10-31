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
import argparse

from flask import current_app, json, jsonify, request, url_for, redirect
from flask import render_template, send_file, send_from_directory
from flask_cors import CORS

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
    full_url_for
)
from partycrasher.resource_encoder import ResourceEncoder
from partycrasher.pc_exceptions import IdenticalReportError

import dateparser

# Create and customize the Flask app.
app = make_json_app('partycrasher', template_folder='ngapp/app')
CORS(app)
app.json_encoder = ResourceEncoder
# From http://stackoverflow.com/questions/30362950/is-it-possible-to-use-angular-with-the-jinja2-template-engine
jinja_options = app.jinja_options.copy()

jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>'
))
app.jinja_options = jinja_options

crasher = None


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

    A resource contains its hyperlink reference (i.e., URL), and (sometimes)
    its `link relation`_.

    .. _link relation: http://www.iana.org/assignments/link-relations/link-relations.xhtml

    .. code-block:: json

        {
            "resource": {
                "href": "http://domain.tld/path/to/resource"
            }
        }

    Endpoints at a glance
    =====================

    .. code-block:: none

        partycrasher
        ├── <project name>
        │   ├── buckets
        │   |   └── <threshold>
        │   |       └── <bucket id>
        │   ├── config
        │   └── reports
        │       └── dry_run
        ├── buckets
        |   └── <threshold>
        |       └── <bucket id>
        ├── config
        └── reports
            └── dry_run

    """

    projects = crasher.get_projects()

    # This should be a tree for all of the services available.
    return jsonify(self=dict(href('root'), rel='canonical'),
                   partycrasher={
                       'version': partycrasher.__version__,
                       'elastic': crasher.es_servers,
                   },
                   projects=projects,
                   config={
                       'default_threshold': 4.0,
                       'thresholds': crasher.thresholds
                   })


@app.route('/ui/bower_components/<path:filename>', methods=['GET'])
def bower_components(filename):
    return send_from_directory(relative('ngapp/bower_components/'), filename)


@app.route('/ui/<path:filename>', methods=['GET'])
@app.route('/ui/')
def home(filename=None):
    if filename and os.path.exists(relative('ngapp/app/', filename)):
        # It's a static file.
        return send_from_directory(relative('ngapp/app/'), filename)
    elif filename and 'views/' in filename and filename.endswith('.html'):
        # 404 on missing view...
        # If this is not here, Angular could try to load the index page in
        # an infinite loop. Which is bad.
        return '', 404

    context = dict(
        bower=full_url_for('home') + 'bower_components',
        project_names=[proj.name for proj in crasher.get_projects()],
        thresholds=[str(thresh) for thresh in crasher.thresholds],
        basehref=full_url_for('home'),
        restbase=full_url_for('root')
    )

    # Otherwise, it's a route in the web app.
    return render_template('index.html', **context)


@app.route('/reports', methods=['POST'], endpoint='add_report_no_project')
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
    ``/:project/reports``, the ``project`` property will automatically be set;
    otherwise, the ``project`` property is also mandatory.

    The report may also have a ``date`` property, which will be used to group
    crashes by date. If not specified, this is set as the insertion date
    (which may not always be what you want).

    The response contains the bucket assignments, as well as the canonical URL
    to access the report.

    ::

        HTTP/1.1 201 Created
        Location: https://your.host/<project>/report/<report-id>/

    .. code-block:: JSON

        {
            "database_id": "<report-id>",
            "project": "<project>",
            "href": "https://domain.tld/<project>/reports/<report-id>",
            "buckets": {
                "4.0": {
                    "bucket_id": "<bucket-id @ 4.0>",
                    "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                }
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
                "database_id": "<report-id 1>",
                "project": "<project>",
                "href": "https://domain.tld/<project>/reports/<report-id 1>",
                "buckets": {
                    "4.0": {
                        "bucket_id": "<bucket-id @ 4.0>",
                        "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                    }
                }
            },
            {
                "database_id": "<report-id 2>",
                "project": "<project>",
                "href": "https://domain.tld/<project>/reports/<report-id 2>",
                "buckets": {
                    "4.0": {
                        "bucket_id": "<bucket-id @ 4.0>",
                        "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                    }
                }
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

    if not report:
        raise BadRequest('No usable report data provided.',
                         error='no_report_data_provided')

    if isinstance(report, list):
        return jsonify_list(ingest_multiple(report, project)), 201
    else:
        try:
            report, url = ingest_one(report, project)
        except IdenticalReportError as error:
            # Ingested a duplicate report.
            return '', 303, { 'Location': url_for_report(error.report) }
        else:
            return jsonify_resource(report), 201, {
                'Location': url
            }


@app.route('/<project>/reports/<report_id>')
def view_report(project, report_id):
    """
    .. api-doc-order: 2

    Get an existing report
    ======================
    ::

        GET /:project/reports/:report_id HTTP/1.1

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
            "project": "<project>",
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

    try:
        report = crasher.get_crash(report_id, project)
    except partycrasher.ReportNotFoundError:
        return jsonify(not_found=report_id), 404
    else:
        return jsonify_resource(report)

@app.route('/<project>/reports/<report_id>/summary')
def report_summary(project, report_id):
    """
    .. api-doc-order: 2

    Analyse a report and return the most significant bits
    ======================
    ::

        GET /:project/reports/:report_id/summary HTTP/1.1

    Summarises a processed report from the database.

    .. code-block:: json

        {
            "database_id": "<report-id>",
            "project": "<project>",
        }

    """

    try:
        summary = crasher.get_summary(report_id, project)
    except partycrasher.ReportNotFoundError:
        return jsonify(not_found=report_id), 404
    else:
        return jsonify_resource(summary)


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

    Answers the question: “What bucket would this report be assigned to?” This
    does **NOT** store or track the report! Use :ref:`upload-single` to commit
    reports to the database.

    ::

        HTTP/1.1 200 OK

    .. code-block:: JSON

        {
            "database_id": "<report-id>",
            "href": "https://domain.tld/<project>/reports/<report-id>"
            "buckets": {
                "4.0": {
                    "bucket_id": "<bucket-id @ 4.0>",
                    "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                }
            }
        }

    """

    report = request.get_json()
    try:
        assigned_report, _url = ingest_one(report, project, dryrun=True)
    except IdenticalReportError as error:
        # Already ingested report; no need to dry-run.
        return '', 303, { 'Location': url_for_report(error.report) }
    else:
        return jsonify_resource(assigned_report), 200


def not_available_in_this_release():
    @app.route('/reports/<report_id>', methods=['DELETE'],
               defaults={'project': None},
               endpoint='delete_report_no_project')
    @app.route('/<project>/reports/<report_id>', methods=['DELETE'])
    def delete_report(project=None, report_id=None):
        """
        .. api-doc-order: 200

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

    View reports in a bucket
    ========================
    ::

        GET /:project/buckets/:threshold/:bucket_id HTTP/1.1

    Fetches the bucket in given project, for the given threshold.
    Returns with a list of top reports (a semi-arbitrary list), and the amount
    of reports ingested into this bucket.

    Query parameters
    ----------------

    ``from``
        Get page of crash reports starting from this number.
    ``size``
        Get this number of crash reports, starting from ``from``.

    ::

        HTTP/1.1 200 OK

    .. code-block:: JSON

        {
            "id": "<bucket-id>",
            "project": "<project>",
            "href": "http://domain.tld/<project>/buckets/<threshold>/<bucket-id>",
            "threshold": "4.0",
            "top_reports": ["..."],
            "total": 3279
        }

    """
    assert bucket_id is not None
    assert threshold is not None

    from_ = request.args.get('from', None)
    size = request.args.get('size', None)
    
    if from_ is not None:
      from_ = int(from_)
    if size is not None:
      size = int(size)

    try:
        bucket = crasher.get_bucket(threshold, bucket_id, project, from_, size)
    except partycrasher.BucketNotFoundError:
        return jsonify(error="not_found", bucket_id=bucket_id), 404

    return jsonify_resource(bucket)


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

        GET /:project/buckets/:threshold HTTP/1.1

    or

    ::

        GET /buckets/:threshold HTTP/1.1

    Finds the top buckets for a given time-frame. If queried on a ``:project``
    route, implicitly filters by project.

    Query parameters
    ----------------

    ``q``
        Only show buckets, with crashes matching this search query, 
        in lucene search syntax. See
        https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
        for details.
    ``since``
        **Required**. Grab buckets since this date, represented as an ISO 8601
        date/time value (i.e, ``YYYY-MM-DD``), or a relative offset such as
        ``5-hours-ago``, ``3-days-ago`` or ``1-week-ago``, etc.
    ``until``
        Grab buckets with crashes up to but not after this date as represented
        as an ISO 8601 date/time value. Defaults to no limit.
    ``from``
        Get page of results starting from this number.
    ``size``
        Get this number of results, starting from ``from``.

    Example
    -------

    ::

        GET /alan_parsons/buckets/4.0?since=2016-02-29 HTTP/1.1
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
                    "id": "c29a81a0-5a53-4ba0-8123-5e96685a5895",
                    "href": "http://domain.tld/alan_parsons/buckets/4.0/c29a81a0-5a53-4ba0-8123-5e96685a5895",
                    "total": 253,
                    "first_seen": "2016-02-27T14:32:08Z"
                }
            ]
        }

    """
    assert threshold is not None

    query_string = request.args.get('q', None)
    since = request.args.get('since', '3-days-ago')
    from_ = request.args.get('from', None)
    size = request.args.get('size', None)
    upper_bound = request.args.get('until', None)
    
    if from_ is not None:
      from_ = int(from_)
    if size is not None:
      size = int(size)
    
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
    
    if upper_bound is not None:
        try:
            upper_bound = dateparser.parse(upper_bound.replace('-', '_'))
        except ValueError:
            raise BadRequest('Could not understand date format for '
                            '`until=` parameter. '
                            'Supported formats are: ISO 8601 timestamps '
                            'and relative dates. Refer to the API docs for '
                            'more information: '
                            'http://partycrasher.rtfd.org/',
                            until=until)

    buckets = crasher.top_buckets(lower_bound,
                                  project=project,
                                  threshold=threshold,
                                  from_=from_,
                                  size=size,
                                  upper_bound=upper_bound,
                                  query_string=query_string)
    
    if upper_bound is not None:
        upper_bound_ret = upper_bound.isoformat()
    else:
        upper_bound_ret = None

    return jsonify(since=lower_bound.isoformat(),
                   until=upper_bound_ret,
                   threshold=threshold,
                   top_buckets=list(buckets),
                   q=query_string)


@app.route('/reports', methods=['DELETE'])
def delete_reports_no_project():
    """
    .. api-doc-order: 100

    Delete every report in the database
    ==============================

    ::

        DELETE /reports HTTP/1.1

    Deletes every report in the database. Requires that
    ``partycrasher.elastic.allow_delete_all`` be set in the configuration.

    .. warning::

        Issuing this command deletes every report in the database. All of them.

    ::

        HTTP/1.1 200 OK

    """
    if crasher.allow_delete_all:
        crasher.delete_and_recreate_index()
        return jsonify(status="All reports deleted"), 200
    else:
        return jsonify(error="Deleting all reports not enabled"), 403


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


@app.route('/<project>/search')
def search(project):
    """
    .. api-doc-order: 20

    Perform a free-text search
    ======================
    ::

        GET /:project/search?q=:search HTTP/1.1

    Performs a free-text search on all crashes in a project.
    
    Query parameters
    ----------------


    ``q``
        What to search for, in lucene search syntax. See
        https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
        for details.
    ``since``
        Search crashes occuring after this date, represented as an ISO 8601
        date/time value (i.e, ``YYYY-MM-DD``), or a relative offset such as
        ``5-hours-ago``, ``3-days-ago`` or ``1-week-ago``, etc.
    ``until``
        Search crashes occuring before this date as represented
        as an ISO 8601 date/time value. Defaults to no limit.
    ``from``
        Get page of results starting from this number.
    ``size``
        Get this number of results, starting from ``from``.
    ``sort``
        Change how the results are sorted. Specifies a field name such
        as ``date``.
    ``order``
        Should be ``asc`` or ``desc``. Default is ``desc``.
        Determines whether the results should be sorted in 
        ascending or descending order.

    ::
    
        HTTP/1.1 200 OK

    .. code-block:: json

        [
            {
                "database_id": "<report-id>",
                "href": "https://domain.tld/<project>/reports/<report-id>"
                "buckets": {
                    "4.0": {
                        "bucket_id": "<bucket-id @ 4.0>",
                        "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                    }
                }
            },
            {
                "database_id": "<report-id>",
                "href": "https://domain.tld/<project>/reports/<report-id>"
                "buckets": {
                    "4.0": {
                        "bucket_id": "<bucket-id @ 4.0>",
                        "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                    }
                }
            },
            ...
        ]

    """
    
    query_string = request.args.get('q', '*')
    since = request.args.get('since', None)
    until = request.args.get('until', None)
    from_ = request.args.get('from', None)
    size = request.args.get('size', None)
    sort = request.args.get('sort', None)
    order = request.args.get('order', None)
    
    if since is not None:
        try:
            since = dateparser.parse(since.replace('-', '_'))
        except ValueError:
            raise BadRequest('Could not understand date format for '
                            '`until=` parameter. '
                            'Supported formats are: ISO 8601 timestamps '
                            'and relative dates. Refer to the API docs for '
                            'more information: '
                            'http://partycrasher.rtfd.org/',
                            since=since)
    if until is not None:
        try:
            until = dateparser.parse(until.replace('-', '_'))
        except ValueError:
            raise BadRequest('Could not understand date format for '
                            '`until=` parameter. '
                            'Supported formats are: ISO 8601 timestamps '
                            'and relative dates. Refer to the API docs for '
                            'more information: '
                            'http://partycrasher.rtfd.org/',
                            until=until)


    if project == '*':
        project = None
    
    if order is not None:
        if not (order == "asc" or order == "desc"):
            raise BadRequest('Couldn\'t understand sort order. Should be'
                            'asc or desc.')


    r = crasher.search(query_string,
                       since=since,
                       until=until,
                       project=project, 
                       from_=from_, 
                       size=size,
                       sort=sort,
                       order=order)
    return jsonify_resource(r)

#############################################################################
#                                 Utilities                                 #
#############################################################################


def ingest_one(report, project_name, dryrun=False):
    """
    Returns a tuple of ingested report and its URL.

    :raises BadRequest: When project is off.
    :raises IdenticalReportError: When report is identical to existing report.
    """

    raise_bad_request_if_project_mismatch(report, project_name)
    # Graft the project name onto the report.
    report.setdefault('project', project_name)

    report = crasher.ingest(report, dryrun=dryrun)
    url = url_for_report(report)

    return report, url


def ingest_multiple(reports, project_name):
    """
    Same as ingest_one, but takes a list of reports, and returns a list of
    reports.
    """
    return [ingest_one(report, project_name)[0] for report in reports]


def url_for_report(report):
    return url_for('view_report',
                   project=report['project'],
                   report_id=report.id)


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


# Copied from: flask/json.py
def jsonify_resource(resource):
    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
            and not request.is_xhr:
        indent = 2
    return current_app.response_class(json.dumps(resource, indent=indent),
                                      mimetype='application/json')


def relative(*args):
    """
    Return a path relative to the directory containing this very script!
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def main():
    global crasher
    parser = argparse.ArgumentParser(description="Run PartyCrasher REST service.")
    parser.add_argument('--port', type=int, default=5000,
                        help='port to run the REST HTTP service on')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='port to run the REST HTTP service on')
    parser.add_argument('--debug', action='store_true',
                        help='enable Flask debugging mode')
    parser.add_argument('--profile', action='store_true',
                        help='enable profiling')
    parser.add_argument('--config-file', type=str,
                        default=
                          os.path.join(REPOSITORY_ROUTE, 'partycrasher.cfg'),
                        help='specify location of PartyCrasher config file')
    parser.add_argument('--allow-delete-all', action='store_true',
                        help='allow users of the REST interface to delete all data')

    kwargs = vars(parser.parse_args())

    with open(kwargs['config_file']) as config_file:
        crasher = partycrasher.PartyCrasher(config_file)
    del kwargs['config_file']

    if kwargs['allow_delete_all']:
        crasher.config.set('partycrasher.elastic', 'allow_delete_all', 'yes')
    del kwargs['allow_delete_all']

    crasher.ensure_index_created()

    # TODO:
    #  - add parameter: -C [config-setting]

    profile = kwargs['profile']

    #global app
    #if kwargs['profile']:
        #from werkzeug.contrib.profiler import ProfilerMiddleware
        #app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    del kwargs['profile']

    if profile:
        import cProfile
        global run_kwargs
        run_kwargs = kwargs
        cProfile.run('app.run(**run_kwargs)', sort='cumtime')
    else:
        return app.run(**kwargs)


if __name__ == '__main__':
    main()
else:
    with open('partycrasher.cfg') as config_file:
        crasher = partycrasher.PartyCrasher(config_file)
