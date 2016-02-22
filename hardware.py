import argparse
import RPi.GPIO as GPIO
import time
import threading
import Player

player = Player.Player()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    timer = threading.Timer(sec, func_wrapper)
    timer.start()
    return timer

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
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()

    active = player.get_active()
    pressed = get_pressed()

    def main():
        global active, pressed

        previously_pressed = pressed
        pressed = get_pressed()

        light_toggle(active)

        if pressed and not previously_pressed:
            active = not active

            if active:
                player_ouput = player.play()
            else:
                player_ouput = player.stop()

            if arguments.debug:
                print player_ouput

        if arguments.debug:
            print "main \t" + \
                ('pressed' if GPIO.input(7) else 'unpressed') + "\t" + \
                ('active' if active else 'off')

    set_interval(main, 0.05)

    def fetch_active_status():
        global active

        # Need to prevent fetching if any actions haven't finished
        active = player.get_active()

        if arguments.debug:
            value = ('active' if active else 'off')
            print "fetch_active_status \t" + value


    set_interval(fetch_active_status, 5)

    GPIO.cleanup()
