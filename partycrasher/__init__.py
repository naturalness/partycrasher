from flask import Flask, jsonify, request
import ConfigParser
from elasticsearch import Elasticsearch, NotFoundError
from partycrasher.crash import Crash
from partycrasher.es_crash import ESCrash
from partycrasher.bucketer import MLTCamelCase


config = ConfigParser.SafeConfigParser({'elastic': ''})
esServers = config.get('DEFAULT', 'elastic').split()
if len(esServers) < 1:
    esServers = ['localhost']
es = Elasticsearch(esServers)

bucketer = MLTCamelCase(thresh=4.0, lowercase=False, only_stack=False, index='crashes', es=es, name="bucket")
bucketer.create_index()


__version__ = "0.0.1"

app = Flask("partycrasher")

@app.route('/')
def status():
    return jsonify(partycrasher={'version':__version__, 
                                 'elastic':esServers,
                                 'elastic_health':es.cluster.health()})

# TODO catch duplicate and return 303
# TODO multi-bucket multi-threshold mumbo-jumbo
def ingest(crash):
    try:
        return bucketer.assign_save_bucket(Crash(crash))
    except NotFoundError as e:
        raise Exception(' '.join([e.error, str(e.status_code), repr(e.info)]))

# TODO catch duplicate and return 303
def dryrun(crash):
    try:
        return bucketer.assign_bucket(Crash(crash))
    except NotFoundError as e:
        raise Exception(' '.join([e.error, str(e.status_code), repr(e.info)]))
    
def getcrash(database_id):
    try:
        return ESCrash(database_id, index='crashes')
    except NotFoundError as e:
        raise Exception(' '.join([e.error, str(e.status_code), repr(e.info)]))
    
def delcrash(database_id):
    # TODO: we have to call ES directly here, theres nothing in Crash/ESCrash or Bucketer to handle this case
    # maybe ESCrash(database_id).delete()
    raise NotImplementedError("BUT WHY~!~~~~")


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        posted = request.get_json(force=True)
        return jsonify(post=posted, headers=dict(request.headers), crash=ingest(posted))
    if request.method == 'GET':
        raise NotImplementedError()

@app.route('/<project>/reports', methods=['GET', 'POST'])
def project_reports(project=None):
    if request.method == 'POST':
        posted = request.get_json(force=True)
        posted['project'] = project
        return jsonify(post=posted, headers=dict(request.headers))
    if request.method == 'GET':
        raise NotImplementedError()

@app.route('/<project>/config', methods=['GET', 'PATCH'])
def project_config(project=None):
    if request.method == 'PATCH':
        raise NotImplementedError()
    if request.method == 'GET':
        return jsonify(default_threshold=4.0)

if __name__ == '__main__':
    app.run(debug=True)