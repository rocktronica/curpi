import argparse
import flask
import json
import os
import Player

app = flask.Flask(__name__, template_folder='')
player = Player.Player()

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default='0.0.0.0')
parser.add_argument("--port", type=int, default=80)
parser.add_argument("--debug", type=bool, default=True)

parser.add_argument("--public-host", type=str)
arguments = parser.parse_args()

@app.route('/action/<method>')
def run_player_method(method):
    if method == 'play':
        return player.play()
    elif method == 'stop':
        return player.stop()
    elif method == 'volume_up':
        return player.volume_up()
    elif method == 'volume_down':
        return player.volume_down()
    elif method == 'status':
        return player.status()

    elif method == 'restart':
        os.system('sudo reboot')
    elif method == 'shut_down':
        os.system('sudo halt')

@app.route('/status')
def get_status(jsonify=True):
    status = player.get_status()
    return flask.jsonify(status) if jsonify else status

def get_exposed_endpoints(public_host=None):
    if not public_host: return []

    actions = ['play', 'stop', 'volume_up', 'volume_down'];
    def to_set(action):
        return dict(
            key = action,
            url = 'http://' + public_host + '/action/' + action,
        )

    return map(to_set, actions)

@app.route('/')
def index():
    return flask.render_template('index.html',
        status = get_status(False),
        exposed_endpoints = get_exposed_endpoints(arguments.public_host),
    )

if __name__ == '__main__':
    app.debug = arguments.debug
    app.run(host=arguments.host, port=arguments.port)
