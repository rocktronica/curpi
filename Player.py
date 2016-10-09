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

    try:
        return json.load(urllib2.urlopen(url))
    except urllib2.HTTPError, e:
        # TODO: log 404s, etc
        print None

class Player():
    # TODO: make this less magic...
    HARDWARE_MAX_VOLUME_PERCENT = 85 # effectively full loudness w/o distortion

    VOLUME_STEPS = 12
    DEFAULT_VOLUME_PERCENT = 90

    def __init__(self):
        self.set_volume(self.DEFAULT_VOLUME_PERCENT)

    def play(self):
        if self.get_active(): return
        return get_action_script_result('play')

    def stop(self):
        if not self.get_active(): return
        return get_action_script_result('stop')

    def toggle(self):
        if self.get_active():
            return self.stop()
        else:
            return self.play()

    def _update_volume_step(self, step):
        self._volume_step = step

        volume_percent = ((float(self._volume_step) / float(self.VOLUME_STEPS))
            * self.HARDWARE_MAX_VOLUME_PERCENT)

        return get_action_script_result('volume_set', str(volume_percent) + '%')

    def set_volume(self, volume_percent):
        step = int((float(volume_percent) / 100) * self.VOLUME_STEPS)
        return self._update_volume_step(step)

    def volume_up(self):
        step = min(self._volume_step + 1, self.VOLUME_STEPS)
        return self._update_volume_step(step)

    def volume_down(self):
        step = max(0, self._volume_step - 1)
        return self._update_volume_step(step)

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
