import argparse
import RPi.GPIO as GPIO
import time
import threading
import Player

player = Player.Player()

PINS = dict(
    ON_OFF_BUTTON = 7,
    ON_OFF_LIGHT = 11,
)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    timer = threading.Timer(sec, func_wrapper)
    timer.start()
    return timer

def light_toggle(on):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS['ON_OFF_LIGHT'], GPIO.OUT)
    GPIO.output(PINS['ON_OFF_LIGHT'], GPIO.HIGH if on else GPIO.LOW)

def get_pressed(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()

    active = player.get_active()

    pressed = dict(
        on_off = get_pressed(PINS['ON_OFF_BUTTON']),
    )

    previously_pressed = dict()

    line = ''

    def main():
        global active, pressed, line

        previously_pressed['on_off'] = pressed['on_off']
        pressed['on_off'] = get_pressed(PINS['ON_OFF_BUTTON'])

        light_toggle(active)

        updated = False
        if pressed['on_off'] and not previously_pressed['on_off']:
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
                'pressed[\'on_off\']: ' + ('Y' if pressed['on_off'] else 'N'),
                'previously_pressed[\'on_off\']: ' +
                    ('Y' if previously_pressed['on_off'] else 'N'),
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
