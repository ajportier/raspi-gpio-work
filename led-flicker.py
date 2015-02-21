#!/usr/bin/env python
# Author: Adam Portier <aportier@haverford.edu>

import RPi.GPIO as GPIO
from time import sleep

# Configuration
led_pin = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, False)

# Toggles LED state
def toggleLED(pin):
    state = GPIO.input(pin)
    state = not state
    GPIO.output(pin, state)

while True:
    try:
        toggleLED(led_pin)
        sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
