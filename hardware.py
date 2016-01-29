import argparse
import json
import RPi.GPIO as GPIO
import subprocess
import time
import urllib2
import sys
import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    timer = threading.Timer(sec, func_wrapper)
    timer.start()
    return timer

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

def light_toggle(on):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, GPIO.HIGH if on else GPIO.LOW)

def light_on():
    light_toggle(True)

def light_off():
    light_toggle(False)

def get_pressed():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)
    return GPIO.input(7)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='0.0.0.0')
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()

    active = get_active_status(arguments)
    pressed = get_pressed()

    def main():
        global active, pressed

        previously_pressed = pressed
        pressed = get_pressed()

        light_toggle(active)

        if pressed and not previously_pressed:
            active = not active
            hit_action_endpoint('play' if active else 'stop', arguments)

        if arguments.debug:
            print "main \t" + \
                ('pressed' if GPIO.input(7) else 'unpressed') + "\t" + \
                ('active' if active else 'off')

    set_interval(main, 0.05)

    def fetch_active_status():
        global active

        # Need to prevent fetching if any actions haven't finished
        active = get_active_status(arguments)

        if arguments.debug:
            print "fetch_active_status \t" + \
                ('active' if active else 'off')

    set_interval(fetch_active_status, 5)

    GPIO.cleanup()
