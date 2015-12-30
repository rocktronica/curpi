import flask
import glob
import os
import subprocess

app = flask.Flask(__name__, template_folder='')

@app.route('/action/<script>')
def action(script):
    os.system('sh action/' + script + '.sh')
    return 'ok'

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
