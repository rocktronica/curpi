import argparse
import RPi.GPIO as GPIO
import time
import threading
import Player

player = Player.Player()

PINS = dict(
    ON_OFF_BUTTON = 7,
    ON_OFF_LIGHT = 11,
    VOLUME_UP_BUTTON = 13,
    VOLUME_DOWN_BUTTON = 15,
)

IO_PINS = [
    PINS['ON_OFF_BUTTON'],
    PINS['VOLUME_UP_BUTTON'],
    PINS['VOLUME_DOWN_BUTTON'],
]

def first_pressed():
    for pin in IO_PINS:
        if get_pressed(pin):
            return pin
    return None

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

    pressed = first_pressed()
    clean = not pressed

    def main():
        global active, clean, pressed

        light_toggle(active)

        previously_clean = clean
        clean = not first_pressed()
        updated = not previously_clean == clean

        pressed = first_pressed()
        if updated and pressed:
            if pressed == PINS['ON_OFF_BUTTON']:
                if active:
                    player_ouput = player.stop()
                else:
                    player_ouput = player.play()

                active = player.get_active()

            if arguments.debug:
                print "\t".join([
                    'pressed: ' + str(pressed),
                    'active:  ' + ('Y' if active else 'N'),
                ])

    # TODO: let Flask app and hardware share same instance of player.....
    def fetch_active_status():
        global active
        active = player.get_active()

    set_interval(fetch_active_status, 2)

    while True:
        main()
        time.sleep(0.05)

    GPIO.cleanup()
