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
import smtplib #for text messages

from email.message import EmailMessage

#from slack_sdk import WebClient
#from slack_sdk.errors import SlackApiError

#client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
#doorbell = os.getenv('KKWT_NAME')
#channel_id = "C01GRC04C2E"

# in seconds
settle_time = 0.1
bounce_time = 1

active = False

'''def notify():
    result = client.chat_postMessage(
        channel=channel_id, 
        text='Someone is at ' + doorbell + '\'s door'
    )
#    logger.info(result)'''
def door_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = Doorbell alert

    user = "jerry.naylor77@gmail.com"
    password = "MarchApril20072014!"

def play():
    x = datetime.datetime.now()
    y = (x.month)
    z = (x.day)

    if ((y == 11 and 30 >= z >= 27)
        or (y == 12 and 25 >= z >= 1)):
            print('DING DONG')
            os.system('aplay jinglebell.wav >/dev/null 2>&1')

    elif (y == 10 and 30 >= z >= 1):
        print('DING DONG')
        os.system('aplay vampire howl.wav >/dev/null 2>&1')  

    else:
        os.system('aplay din-dong.wav >/dev/null 2>&1')
    
def wait():
    global active

    while True:
        input_state = GPIO.input(18)
        if input_state:
            print('Bell has rung.')
            active = False
            break
        time.sleep(0.2)

def trigger():
    now = datetime.datetime.now()
    print("Doorbell pushed at: ")
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
   

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
    print('Doorbell ready. Waiting to be activated.') 
    return not input_state

def falling_edge(channel):
    input_state = GPIO.input(18)
    print('Doorbell entering ready state')
    if settle():
        trigger()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=falling_edge, bouncetime=(bounce_time * 1000))

print('started')

signal.pause()