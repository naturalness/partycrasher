#!/usr/bin/env python

#  Copyright (C) 2016 Joshua Charles Campbell

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

from flask import Flask, json, jsonify, request, make_response, url_for
from flask.ext.cors import CORS

# Hacky things to add this PartyCrasher to the path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import partycrasher


app = Flask('partycrasher')
CORS(app)
crasher = partycrasher.PartyCrasher()


class BadRequest(RuntimeError):
    """
    Raised and handled when something funky happens.
    """


@app.route('/')
def status():
    return jsonify(partycrasher={'version': partycrasher.__version__,
                                 'elastic': crasher.esServers,
                                 'elastic_health': crasher.es.cluster.health()})


@app.route('/reports', methods=['POST'])
@app.route('/<project>/reports', methods=['POST'])
def add_report(project=None):
    """
    ===================
    Upload a new report
    ===================

    ::

        POST /:project/reports HTTP/1.1

    or

    ::

        POST /reports HTTP/1.1

    ::

        HTTP/1.1 201 Created
        Location: https://domain.tld/<project>/report/<report-id>/

    .. code-block:: JSON

        {
            "id": "<report-id>",
            "bucket_id": "<bucket-id>",
            "bucket_url": "https://domain.tld/<project>/buckets/<T=[default]>/<bucket-id>"
        }

    ---------------
    Possible errors
    ---------------

    When an identical (not just duplicate) crash is posted::

        HTTP/1.1 303 See Other
        Location: https://domain.tld/<project>/report/<report-id>/

    When a project URL is used but the project field in the crash report
    reports a it belongs to a different project::

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
    # Ignore project.
    assert report_id is not None

    try:
        report = crasher.get_crash(report_id)
    except partycrasher.ReportNotFoundError:
        return jsonify(not_found=report_id), 404
    else:
        return jsonify(report)


@app.route('/<project>/reports')
def reports_overview(project=None):
    raise NotImplementedError()


@app.route('/<project>/config', methods=['GET', 'PATCH'])
def project_config(project=None):
    if request.method == 'PATCH':
        raise NotImplementedError()
    if request.method == 'GET':
        return jsonify(default_threshold=4.0)

#############################################################################
#                                 Utilities                                 #
#############################################################################

def ingest_one(report, project_name):
    """
    Returns a tuple of ingested report and its URL.
    """
    if 'project' not in report:
        if project_name:
            # Graft the project name onto the report:
            report['project'] = project_name
        else:
            # No project name anywhere. This is not good...
            raise BadRequest('Missing project name')
    elif project_name is not None and report['project'] != project_name:
        raise BadRequest("Project name mismatch: "
                         "Posted a report to '{0!s}' "
                         "but the report claims it's from '{1!s}'"
                         .format(project_name, report['project']))

    report = crasher.ingest(report)
    url = url_for('view_report',
                  project=report['project'],
                  report_id=report['database_id'])
    return report, url


@app.errorhandler(BadRequest)
def on_bad_request(error):
    message = error.message if error.message else 'Bad Request'
    return jsonify(message=message), 400


def ingest_multiple(reports, project_name):
    return [ingest_one(report, project_name)[0] for report in reports]


def jsonify_list(seq):
    """
    Same as jsonify, but works on lists.
    """
    # Coerce to list
    if not isinstance(seq, list):
        seq = list(seq)

    should_indent = not (request.headers.get('X-Requested-With', '') ==
                         'XMLHttpRequest')
    body = json.dumps(seq, indent=4 if should_indent else None)

    return make_response((body, None, {'Content-Type': 'application/json'}))


def main():
    if len(sys.argv) > 1:
        app.run(debug=True, port=int(sys.argv[1]))
    else:
        app.run(debug=True)


if __name__ == '__main__':
    main()
