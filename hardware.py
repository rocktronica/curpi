import app
import argparse
import RPi.GPIO as GPIO
import subprocess
import time

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
    except subprocess.CalledProcessError, e:
        if arguments.debug: print e.output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='0.0.0.0')
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(7, GPIO.IN)

    on = False # TODO: use status
    pressed = False

    while True:
        previously_pressed = pressed
        pressed = GPIO.input(7)

        if pressed and not previously_pressed:
            on = not on

            GPIO.output(11, GPIO.HIGH if on else GPIO.LOW)

            hit_action_endpoint('play' if on else 'stop', arguments)

        if arguments.debug:
            print ("pressed" if GPIO.input(7) else "unpressed") + "\t" + \
                ('on' if on else 'off')

        time.sleep(0.05)

    GPIO.cleanup()
