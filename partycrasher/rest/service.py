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
#  You should have received a copy the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import print_function, division

import os
import sys
import time
import argparse
import traceback
import logging
from logging import error, debug, warn, info
ERROR=error
DEBUG=debug
WARN=warn
INFO=info

from flask import current_app, json, jsonify, request, url_for, redirect
from flask import render_template, send_file, send_from_directory, Flask
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions, HTTPException

import partycrasher

# Hacky things to add PartyCrasher to the path.
REPOSITORY_ROUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPOSITORY_ROUTE)
from partycrasher.api.partycrasher import PartyCrasher

from partycrasher.rest.api_utils import (
    BadRequest,
    jsonify_list,
    redirect_with_query_string,
    full_url_for,
    str_to_bool,
    make_search,
    json_exception
)
from partycrasher.rest.resource_encoder import (ResourceEncoder,
                                                auto_url_for)
from partycrasher.pc_exceptions import (
  PartyCrasherError, 
  IdenticalReportError
  )
from partycrasher.crash import pretty

# Create and customize the Flask app.
app = Flask('partycrasher', template_folder='../ui/app')
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

@app.before_first_request
def before_first_request():
    print("before first request", file=sys.stderr)
    print(logging.getLogger("gunicorn.error").handlers, file=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    #logging.getLogger("elasticsearch").setLevel(logging.INFO)
    logging.getLogger("urllib3.util.retry").setLevel(logging.INFO)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
    app.logger.setLevel(logging.DEBUG)
    if len(logging.getLogger("gunicorn.error").handlers) > 0:
        logging.getLogger("gunicorn.error").handlers[0].setFormatter(
          logging.Formatter("%(asctime)s [%(process)d] [%(levelname)s] [%(name)s] %(message)s"))
        logging.getLogger().handlers = logging.getLogger("gunicorn.error").handlers
        #app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)
        app.logger.handlers = []
        ERROR("before first request error")
        DEBUG("before first request debug")
        

@app.errorhandler(Exception)
def on_crasher_crash(ex):
    (t, v, tb) = sys.exc_info()
    response = jsonify(json_exception(t, v, tb))
    del tb
    if hasattr(ex, 'http_code'):
        response.status_code = ex.http_code
    elif hasattr(ex, 'code'):
        response.status_code = ex.code
    else:
        response.status_code = 500
    return response

for code in default_exceptions.keys():
    app.register_error_handler(code, on_crasher_crash)

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

    # This should be a tree for all of the services available.
    root = crasher.restify()
    root['href'] = full_url_for('root')
    return jsonify(root)


@app.route('/ui/bower_components/<path:filename>', methods=['GET'])
def bower_components(filename):
    return send_from_directory(relative('ui/bower_components/'), filename)

@app.route('/ui/node_modules/<path:filename>', methods=['GET'])
def node_modules(filename):
    return send_from_directory(relative('ui/node_modules/'), filename)


@app.route('/ui/<path:filename>', methods=['GET'])
@app.route('/ui/')
def home(filename=None):
    context = dict(
        bower=full_url_for('home') + 'bower_components',
        node_modules=full_url_for('home') + 'node_modules',
        project_names=[proj for proj in crasher.projects],
        type_names=[t for t in crasher.types],
        thresholds=[str(thresh) for thresh in crasher.thresholds],
        basehref=full_url_for('home'),
        restbase=full_url_for('root'),
        default_threshold=str(crasher.default_threshold)
    )
    if filename and os.path.exists(relative('ui/app/', filename)):
        if 'main.css' in filename:
            css = current_app.response_class(
                render_template(filename, **context),
                mimetype="text/css")
            return css
        else:
            # It's a static file.
            return send_from_directory(relative('ui/app/'), filename)
    elif filename and 'views/' in filename and filename.endswith('.html'):
        # 404 on missing view...
        # If this is not here, Angular could try to load the index page in
        # an infinite loop. Which is bad.
        return '', 404

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
    
    The report may also have a ``force_bucket`` property which will force
    the report to be bucketed in a particular bucket. This is only useful
    for testing purposes.

    ::

        HTTP/1.1 201 Created
        Location: https://your.host/<project>/report/<report-id>/

    .. code-block:: JSON

        {
            "report": {
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
                "report": {
                    "database_id": "<report-id 1>",
                    "project": "<project>",
                    "href": "https://domain.tld/<project>/reports/<report-id 1>",
                    "buckets": {
                        "4.0": {
                            "bucket_id": "<bucket-id @ 4.0>",
                            "href": "https://domain.tld/<project>/buckets/4.0/<bucket-id @ 4.0>"
                        }
                    }
                }
            },
            {
                "report": {
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
    report_or_reports = request.get_json()
    explain = str_to_bool(request.args.get('explain'), False)
    assert isinstance(explain, bool)
    dry_run = str_to_bool(request.args.get('dryrun'), False)
    assert isinstance(dry_run, bool)
    if not report_or_reports:
        raise BadRequest('No usable report data provided.',
                         error='no_report_data_provided')
    if dry_run:
        success_code = 200
    else:
        success_code = 201

    if isinstance(report_or_reports, list):
        reports = [crasher.report(crash=i, 
                                  project=project, 
                                  dry_run=dry_run)
                   for i in report_or_reports]
        for report in reports:
            report.search(explain)
            if dry_run:
                report.assign_buckets()
            else:
                report.save()
        assert reports[0].explain == explain
        return jsonify_list(reports), success_code
    elif isinstance(report_or_reports, dict):
        ERROR("project in crash? " + str("project" in report_or_reports))
        report = crasher.report(crash=report_or_reports, 
                                project=project, 
                                dry_run=dry_run)
        try:
            report.search(explain)
            if dry_run:
                report.assign_buckets()
            else:
                report.save()
        except IdenticalReportError as error:
            # Ingested a duplicate report.
            return '', 303, { 'Location': auto_url_for(error.report) }
        else:
            return (
                jsonify_resource(report), 
                success_code, 
                {'Location': auto_url_for(report)}
                )
    else:
        raise BadRequest("Report must be a list or object.")


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
    auto_summary = str_to_bool(request.args.get('auto_summary'), False)

    report = crasher.report(report_id, project, explain=auto_summary)
    return jsonify_resource(report)

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
    s = make_search(request.args, bucket_id=bucket_id, threshold=threshold)

    return jsonify_resource(crasher.report_bucket(**s))


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
    s = make_search(args=request.args,
        threshold=threshold,
        project=project)
    threshold = crasher.report_threshold(**s)

    return jsonify(threshold)

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

    return jsonify(crasher)

@app.route('/project/<project>')
def view_project(project=None):
    """
    .. api-doc-order: 100

    View project reports and buckets
    ==============================

    ::

        GET /project/:project HTTP/1.1

    ::

        HTTP/1.1 200 OK

    .. code-block:: json

        {
        ...
        }

    """
    assert project is not None
    s = make_search(args=request.args,
        project=project)
    project = crasher.report_project(**s)
    return(jsonify(project))

@app.route('/search',
           defaults={'project': None},
           endpoint='search_no_project')
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
    
    if project == '*':
        project = None
    
    if request.args.get('order') is not None:
        raise NotImplementedError("sort order feature was deimpemented!")
        if not (order == "asc" or order == "desc"):
            raise BadRequest('Couldn\'t understand sort order. Should be'
                            'asc or desc.')

    if request.args.get('sort') is not None:
        raise NotImplementedError("sort feature was deimpemented!")
    
    s = make_search(request.args, project=project)

    return jsonify_resource(crasher.report_search(**s))

@app.route('/<path:path>/', methods=['GET'])
def view(path=None):
    params = {}
    if path is not None:
        path = path.split('/')
        k = None
        for i in range(0, len(path)):
            if (i % 2) == 0:
                k = path[i]
            else:
                params[k] = path[i]
                k = None
    if k is not None:
        wanted = k
    else:
        wanted = None
    #if type_ == '*':
        #type_ = None
    #if project == '*':
        #project = None
    #s = make_search(args=request.args,
        #type_=type_,
        #project=project)
    #results = crasher.report_search(**s)
    return(jsonify({'params': params, 'wanted': wanted}))



#############################################################################
#                                 Utilities                                 #
#############################################################################

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
    base = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    DEBUG("Basedir is %s" % base)
    return os.path.join(base, *args)

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
                          os.path.join(REPOSITORY_ROUTE, 'config.py'),
                        help='specify location of PartyCrasher config file')
    parser.add_argument('--allow-delete-all', action='store_true',
                        help='allow users of the REST interface to delete all data')

    kwargs = vars(parser.parse_args())

    
    crasher = PartyCrasher(kwargs['config_file'])
    del kwargs['config_file']

    if kwargs['allow_delete_all']:
        crasher.config.ElasticSearch.allow_delete_all = True
    del kwargs['allow_delete_all']

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
