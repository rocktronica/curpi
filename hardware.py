import argparse
import json
import RPi.GPIO as GPIO
import subprocess
import time
import urllib2
import sys

def hit_action_endpoint(action, arguments):
    host = arguments.host
    port = arguments.port

    url = 'http://' + host + ':' + str(port) + '/action/' + action

    try:
        if arguments.debug: print url
        output = subprocess.check_output('curl ' + url,
            stderr=subprocess.STDOUT,
            shell=True)
        if arguments.debug: print output
        return output
    except subprocess.CalledProcessError, e:
        if arguments.debug: print e.output

def get_active_status(arguments):
    host = arguments.host
    port = arguments.port

    url = 'http://' + host + ':' + str(port) + '/status'
    result = json.load(urllib2.urlopen(url))

    return result['active']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='0.0.0.0')
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(7, GPIO.IN)

    on = get_active_status(arguments)
    pressed = False

    while True:
        previously_pressed = pressed
        pressed = GPIO.input(7)

        GPIO.output(11, GPIO.HIGH if on else GPIO.LOW)

        if pressed and not previously_pressed:
            on = not on
            hit_action_endpoint('play' if on else 'stop', arguments)

        if arguments.debug:
            print ("pressed" if GPIO.input(7) else "unpressed") + "\t" + \
                ('on' if on else 'off')

        time.sleep(0.05)

    GPIO.cleanup()
