import argparse
import flask
import glob
import json
import os
import subprocess
import urllib2

app = flask.Flask(__name__, template_folder='')

@app.route('/action/<script>')
def get_action_script_result(script):
    return subprocess.check_output(
        'sh action/' + script + '.sh',
        stderr=subprocess.STDOUT,
        shell=True)

def get_metadata():
    url = 'http://www.thecurrent.org/playlist/metadata/current'
    return json.load(urllib2.urlopen(url))

@app.route('/status')
def get_status(jsonify=True):
    active = bool(get_action_script_result('status'))

    response = dict(
        active = active
    )

    if active:
        response['metadata'] = get_metadata()

    return flask.jsonify(response) if jsonify else response

@app.route('/')
def index():
    return flask.render_template('index.html',
        status = get_status(False),
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='0.0.0.0')
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--debug", type=bool, default=True)
    arguments = parser.parse_args()

    app.debug = arguments.debug
    app.run(host=arguments.host, port=arguments.port)
