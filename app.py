import argparse
import flask
import json
import Player

app = flask.Flask(__name__, template_folder='')
player = Player.Player()

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

@app.route('/status')
def get_status(jsonify=True):
    status = player.get_status()
    return flask.jsonify(status) if jsonify else status

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
