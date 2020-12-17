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
#import smtplib for text messages
import random

#from email.message import EmailMessage
from array import *

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
doorbell = os.getenv('KKWT_NAME')
channel_id = os.getenv('SLACK_CHANNEL_ID')

# in seconds
settle_time = 0.1
bounce_time = 1

active = False

def notify():
    result = client.chat_postMessage(
        channel=channel_id, 
        text='Someone is at the *' + doorbell + ' Door*'
    )
    #logger.info(result)

tone = 0

def doortone():
    holiday = ["NewYear", "Halloween", "Christmas"]
    wav = [["ding-dong.wav"]]
    wav[holiday["Halloween"]][0] = "vampirehowl.wav"
    wav.insert(holiday.index("Christmas"), ["jnglebell.wav", "hohoho.wav", "carolbells.wav"])
    wav.insert(holiday.index("Halloween"), ["vampirehowl.wav", "spooky.wav", "jacko.wav"])
    wav.insert(holiday.index("New Year"), ["happyny.wav"])

    today = datetime.datetime.now()
    month = (today.month)
    day = (today.day)

    if (month == 1 and 10 >-= day >= 1):
        currentholiday = holiday["NewYear"]

    elif (month == 10 and 30 >= day >= 1):
        print('DING DONG')
        currentholiday = holiday["Halloween"]

    elif ((month == 11 and 30 >= day >= 23)
        or (month == 12 and 31 >= day >= 1)):
            print('DING DONG')
            currentholiday = holday["Christmas"]
    else:
        return "ding-dong.wav"

    tone += 1
    if (tone >= len(wav[currentholiday])):
        tone =0

    return wav[currentholiday][tone]
    

#This defines the music for the bells
'''def newyears(): #NEED TO GET TONES!
    wav = {
        0: "vampirehowl.wav",
        1: "hohoho.wav",
        2: "carolbells.wav"
    }
    wavfile = wav.get(random.randint(0,2),'ding-dong.wav')
    print(wavfile)
    return wavfile

def halloweentone(): #NEED TO GET TONES!
    wav = {
        0: "vampirehowl.wav",
        1: "hohoho.wav",
        2: "carolbells.wav"
    }
    wavfile = wav.get(random.randint(0,2),'ding-dong.wav')
    print(wavfile)
    return wavfile

def christmastone():
    wav = {
        0: "jnglbell.wav",
        1: "hohoho.wav",
        2: "carolbells.wav"
    }
    wavfile = wav.get(random.randint(0,2),'ding-dong.wav')
    print(wavfile)
    return wavfile

#This will define the times it is played
def play():
    x = datetime.datetime.now()
    month = (x.month)
    day = (x.day)

    if (month == 1 and 10 >= day >= 1):
        print('DING DONG')
        wav = random.randint(0,22)
        playcmd = 'aplay ' + newyears() + '  >/dev/null 2>&1'
        os.system(playcmd)

    elif (month == 10 and 30 >= day >= 1):
        print('DING DONG')
        wav = random.randint(0,22)
        playcmd = 'aplay ' + halloweentone() + '  >/dev/null 2>&1'
        os.system(playcmd)

    elif ((month == 11 and 30 >= day >= 23)
        or (month == 12 and 31 >= day >= 1)):
            print('DING DONG')
            playcmd = 'aplay ' + christmastone() + '  >/dev/null 2>&1'
            os.system(playcmd)
    else:
        os.system('aplay ding-dong.wav >/dev/null 2>&1')'''
    
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

    tp = threading.Thread(target=doortone) #return to play
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