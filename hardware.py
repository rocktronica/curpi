import argparse
import RPi.GPIO as GPIO
import time
import threading
import Player

player = Player.Player()

# Raspberry Pi 2 Model B
PINS = dict(
    ON_OFF_BUTTON = 7, # GPIO4
    ON_OFF_LIGHT = 11, # GPIO17
    VOLUME_UP_BUTTON = 13, # GPIO27
    VOLUME_DOWN_BUTTON = 15, #GPIO22

    # BELOW FOR DOCUMENTATION ONLY AND NOT EXPOSED

    # Used by HiFiBerry DAC+ HW1.0
    # https://support.hifiberry.com/hc/en-us/community/posts/201491612-GPIO-pins-used-by-Digi-
    HIFIBERRY_3 = 3, # GPIO2
    HIFIBERRY_5 = 5, # GPIO3
    HIFIBERRY_31 = 31, # GPIO6
    HIFIBERRY_12 = 12, # GPIO18
    HIFIBERRY_35 = 35, # GPIO19
    HIFIBERRY_38 = 38, # GPIO20
    HIFIBERRY_40 = 40, # GPIO21

    # Short to ground to engage
    BOOT_TIME_READ_WRITE = 36, # GPIO16
    HALT_SHUTDOWN = 32, # GPIO12

    # Unused GPIO pins
    UNUSED_16 = 16, # GPIO23
    UNUSED_18 = 18, # GPIO24
    UNUSED_19 = 19, # GPIO10
    UNUSED_21 = 21, # GPIO09
    UNUSED_22 = 22, # GPIO25
    UNUSED_23 = 23, # GPIO11
    UNUSED_29 = 29, # GPIO05
    UNUSED_33 = 33, # GPIO13
    UNUSED_37 = 37, # GPIO26
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
            elif pressed == PINS['VOLUME_UP_BUTTON']:
                player.volume_up()
            elif pressed == PINS['VOLUME_DOWN_BUTTON']:
                player.volume_down()

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
