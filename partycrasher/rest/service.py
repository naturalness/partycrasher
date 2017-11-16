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
from partycrasher.api.report import Report

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


@app.route('/reports', methods=['POST'], endpoint='add_report')
def add_report(project=None):
    """
    .. api-doc-order: 1
    .. _upload-single:

    Upload a new report
    ===================

    ::

        POST /reports HTTP/1.1

    Uploads a new report. The report should be sent as a JSON Object with at
    least a unique ``database_id`` property. 
    The ``project`` and ``type`` properties are mandatory.

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
        Location: https://your.host/report/<report-id>/

    .. code-block:: JSON

        {
            "report": {
                "database_id": "<report-id>",
                "project": "<project>",
                "href": "https://domain.tld/reports/<report-id>",
                "buckets": {
                    "4.0": {
                        "bucket_id": "<bucket-id @ 4.0>",
                        "href": "https://domain.tld/buckets/4.0/<bucket-id @ 4.0>"
                    }
                }
        }

    Errors
    ------

    When an *identical* (not just duplicate) report is posted::

        HTTP/1.1 303 See Other
        Location: https://domain.tld/report/<report-id>/


    Upload multiple new reports
    ===========================

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
                    "href": "https://domain.tld/reports/<report-id 1>",
                    "buckets": {
                        "4.0": {
                            "bucket_id": "<bucket-id @ 4.0>",
                            "href": "https://domain.tld/buckets/4.0/<bucket-id @ 4.0>"
                        }
                    }
                }
            },
            {
                "report": {
                    "database_id": "<report-id 2>",
                    "project": "<project>",
                    "href": "https://domain.tld/reports/<report-id 2>",
                    "buckets": {
                        "4.0": {
                            "bucket_id": "<bucket-id @ 4.0>",
                            "href": "https://domain.tld/buckets/4.0/<bucket-id @ 4.0>"
                        }
                    }
                }
            }
        ]

    Errors
    ------

    When an *identical* (not just duplicate) report is posted::

        HTTP/1.1 303 See Other
        Location: https://domain.tld/report/<report-id>/

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
        reports = [crasher.report(crasher.null_search,
                                  crash=i, 
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
        report = crasher.report(crasher.null_search,
                                crash=report_or_reports, 
                                dry_run=dry_run)
        try:
            report.search(explain)
            if dry_run:
                report.assign_buckets()
            else:
                report.save()
        except IdenticalReportError as error:
            # Ingested a duplicate report.
            return '', 303, { 'Location': auto_url_for(report) }
        else:
            assert isinstance(report, Report)
            return (
                jsonify_resource(report), 
                success_code, 
                {'Location': auto_url_for(report)}
                )
    else:
        raise BadRequest("Report must be a list or object.")


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
    if k is not None: # last unpaired item in path
        wanted = k
    else:
        wanted = None
    if 'reports' in params:
        wanted = 'report'
        report = params['reports']
        del params['reports']
    s = make_search(args=params)
    s = make_search(args=request.args, **s)
    #
    if wanted == 'reports':
        return jsonify(crasher.report_search(**s)(logdf=True))
    elif wanted == 'buckets':
        return jsonify(crasher.bucket_search(**s)())
    elif wanted == 'report':
        return jsonify(crasher.report(
            search=s, 
            crash=report, 
            explain=True, 
            logdf=True
            ))
    else:
        return jsonify({'params': params, 'wanted': wanted, 'search': dict(**s)})


#############################################################################
#                                 Utilities                                 #
#############################################################################

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
    
    #global app
    if kwargs['profile']:
        profile = True
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30],
                                          profile_dir="profile")
    else:
        profile = False
    del kwargs['profile']
    return app.run(**kwargs)
    if profile:
        import cProfile
        global run_kwargs
        run_kwargs = kwargs
        cProfile.run('app.run(**run_kwargs)', sort='cumtime')
    else:
        return app.run(**kwargs)


if __name__ == '__main__':
    main()
