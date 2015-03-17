#!/usr/bin/env python

import time
import pickle
import RPi.GPIO as GPIO

SETTINGS_P = 'settings.p'
LED1 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)

def onLED(pin):
    GPIO.output(pin, True)

def offLED(pin):
    GPIO.output(pin, False)

if __name__ == '__main__':
    try:
        while True:
            settings = {}

            try:
                settings = pickle.load(open(SETTINGS_P, 'rb'))
            except IOError:
                pass

            #print "Current state is {}".format(settings['state'])

            if (settings['state'] == 'on'):
                onLED(LED1)
            if (settings['state'] == 'off'):
                offLED(LED1)

            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
