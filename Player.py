import json
import subprocess
import urllib2

def get_action_script_result(script, argument_string=None):
    command = 'sh action/' + script + '.sh'

    if argument_string:
        command += ' ' + str(argument_string)

    try:
        return subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, e:
         return e.output

def get_metadata():
    url = 'http://www.thecurrent.org/playlist/metadata/current'
    return json.load(urllib2.urlopen(url))

class Player():
    def play(self):
        if self.get_active(): return
        return get_action_script_result('play')

    def stop(self):
        if not self.get_active(): return
        return get_action_script_result('stop')

    def volume_up(self):
        return get_action_script_result('volume_up')

    def volume_down(self):
        return get_action_script_result('volume_down')

    def get_status(self, fetch_metadata=True):
        # Ahem...
        active = bool(get_action_script_result('status'))

        response = dict(
            active = active
        )

        if active and fetch_metadata:
            response['metadata'] = get_metadata()

        return response

    def get_active(self):
        return self.get_status(fetch_metadata=False)['active']
