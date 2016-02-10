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
from flask import Flask, jsonify, request
import partycrasher

app = Flask("partycrasher")

crasher = partycrasher.PartyCrasher()

@app.route('/')
def status():
    return jsonify(partycrasher={'version':partycrasher.__version__, 
                                 'elastic':crasher.esServers,
                                 'elastic_health':crasher.es.cluster.health()})

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        posted = request.get_json(force=True)
        return jsonify(post=posted, headers=dict(request.headers), crash=crasher.ingest(posted))
    if request.method == 'GET':
        raise NotImplementedError()

@app.route('/<project>/reports', methods=['GET', 'POST'])
def project_reports(project=None):
    if request.method == 'POST':
        posted = request.get_json(force=True)
        posted['project'] = project
        return jsonify(post=posted, headers=dict(request.headers), crash=crasher.ingest(posted))
    if request.method == 'GET':
        raise NotImplementedError()

@app.route('/<project>/config', methods=['GET', 'PATCH'])
def project_config(project=None):
    if request.method == 'PATCH':
        raise NotImplementedError()
    if request.method == 'GET':
        return jsonify(default_threshold=4.0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(debug=True, port=int(sys.argv[1]))
    else:
        app.run(debug=True)
