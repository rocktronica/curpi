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
    line = ''

    def main():
        global active, pressed, line

        previously_pressed = pressed
        pressed = get_pressed()

        light_toggle(active)

        updated = False
        if pressed and not previously_pressed:
            updated = True

            if active:
                player_ouput = player.stop()
            else:
                player_ouput = player.play()

            # Sure hope this'll immediately be accurate!
            active = player.get_active()

            if arguments.debug:
                print player_ouput

        previous_line = line
        if arguments.debug:
            line = "\t".join([
                'pressed: ' + ('Y' if pressed else 'N'),
                'previously_pressed: ' + ('Y' if previously_pressed else 'N'),
                'updated: ' + ('Y' if updated else 'N'),
                'active: ' + ('Y' if active else 'N'),
            ])

            if not previous_line == line:
                print line

    # TODO: let Flask app and hardware share same instance of player.....
    def fetch_active_status():
        global active
        active = player.get_active()

    set_interval(fetch_active_status, 2)

    while True:
        main()
        time.sleep(0.05)

    GPIO.cleanup()
