import flask
import glob
import json
import os
import subprocess
import urllib2

app = flask.Flask(__name__, template_folder='')

@app.route('/action/<script>')
def action(script):
    os.system('sh action/' + script + '.sh')
    return 'ok'

@app.route('/metadata')
def get_metadata(jsonify=True):
    url = 'http://www.thecurrent.org/playlist/metadata/current'
    response = json.load(urllib2.urlopen(url))

    return flask.jsonify(response) if jsonify else response

@app.route('/')
def index():
    return flask.render_template('index.html',
        metadata = get_metadata(False)
    )

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
