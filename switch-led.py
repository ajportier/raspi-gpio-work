#!/usr/bin/env python
# Author: Adam Portier <ajportier@gmail.com>

import RPi.GPIO as GPIO
import time

# Configuration
LED1 = 18
SWITCH1 = 25
mode = 0
last_flicker = 0 # stores timestamp of the last LED flicker

'''
These values change how often the loop looks for a change and if the state
is allowed to change. Keeping the button pressed will not permit a state change
if at least one polling cycle has not gone by where the button is not pressed,
setting the change_ok to True. This provides software debouncing.
'''
polling = .05
change_ok = False

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SWITCH1, GPIO.IN, initial=GPIO.LOW)

# Turns LED on
def onLED(pin):
    GPIO.output(pin, True)

# Turns LED off
def offLED(pin):
    GPIO.output(pin, False)

# Toggles LED state
def toggleLED(pin):
    state = GPIO.input(pin)
    state = not state
    GPIO.output(pin, state)

while True:
    try:
        # Read the current switch state into a variable
        switch = GPIO.input(SWITCH1)

        '''
        If the switch is pressed at the time of polling change mode.
        This is done by incrementing mode and taking the modulus of
        the number of modes (4).
        Note: I would have expected the switch to be False when not
        pressed and True when it is, but it is the other way around.
        Maybe the value indicates if the circuit is closed or not?
        '''
        if (switch == False and change_ok):
            mode = (mode + 1) % 4
            change_ok = False

        if (switch == True):
            change_ok = True

        # If mode is 0, turn the LED off
        if (mode == 0):
            offLED(LED1)

        # If mode is 1, turn the LED on
        if (mode == 1):
            onLED(LED1)

        # If mode is 2, flicker slowly (once every second)
        if (mode == 2):
            ts = time.time()
            if ts >= (last_flicker + 1):
                toggleLED(LED1)
                last_flicker = ts

        # If mode is 3, flicker quickly (4 times a second)
        if (mode == 3):
            ts = time.time()
            if ts >= (last_flicker + .25):
                toggleLED(LED1)
                last_flicker = ts

        time.sleep(polling)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
