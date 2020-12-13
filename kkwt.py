#!/usr/bin/python3 -u

#code used was copied from https://movementarian.org/blog/
#changes are being made to what we know works

import datetime
import RPi.GPIO as GPIO
import threading
import signal
import wave
import time
import sys
import os

# in seconds
settle_time = 0.1
bounce_time = 1

active = False

def notify():
    Nothing = 0

def play():
    print('DING DONG')
    os.system('aplay ding-dong.wav >/dev/null 2>&1')
   
def wait():
    global active

    while True:
        input_state = GPIO.input(18)
        if input_state:
            print('Bell has rung.')#('got input_state %s, active -> False' % input_state)
            active = False
            break
        time.sleep(0.2)

def trigger():
    now = datetime.datetime.now()
    print("Doorbell pushed at: ")
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    #print('Doorbell pushed at %s' %t)#('triggering at %s' % time.time())

    tn = threading.Thread(target=notify)
    tn.start()

    tp = threading.Thread(target=play)
    tp.start()

    tw = threading.Thread(target=wait)
    tw.start()

    tw.join()
    tp.join()
    tn.join()

def settle():
    global settle_time
    time.sleep(settle_time)
    input_state = GPIO.input(18)
    print('Doorbell ready. Waiting for doorbell to be activated.') #('input state now %s' % input_state)
    return not input_state

def falling_edge(channel):
    input_state = GPIO.input(18)
    print('Doorbell entering ready state')#('got falling edge, input_state %s' % input_state)
    if settle():
        trigger()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=falling_edge, bouncetime=(bounce_time * 1000))

print('started')

signal.pause()