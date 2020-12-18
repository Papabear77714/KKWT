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
import random

from array import *
from datetime import date,datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

tone = 0
today = (date.today())
y = (today.year)
holidays = [('New Year', (date(y, 1, 1), date(y, 1, 10))),
            ('Valentines', (date(y, 2, 13), date(y, 2, 15))),
            ('Fourth of July', (date(y, 7, 1), date(y, 7, 7))),
            ('Halloween', (date(y, 10, 1), date(y, 10, 31))),
            ('Thanksgiving', (date(y, 11, 18), date(y, 11, 24))),
            ('Christmas', (date(y, 11, 25), date(y, 12, 15)))]

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
doorbell = os.getenv('KKWT_NAME')
channel_id = os.getenv('SLACK_CHANNEL_ID')

# in seconds
settle_time = 0.1
bounce_time = 1

active = False

# Sends notification to Slack
def notify():
    result = client.chat_postMessage(
        channel=channel_id, 
        text='Someone is at the *' + doorbell + ' Door*'
    )
    #logger.info(result)

# Defines which holiday we are in
def get_holiday(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year = y)
    return next(holiday for holiday, (start, end) in holidays
                if start <= now <= end)

# Defines which tone to play for specific holiday
def doortone():
    global tone
    holiday = ["New Year", "Valentines", "Fourth of July", "Halloween", "Thanksgiving", "Christmas"]
    wav = [["ding-dong.wav"]]
    wav.insert(holiday.index("New Year"), ["celebrate", "hppyyr.wav"])
    wav.insert(holiday.index("Valentines"), ["heart.wav", "love.wav"])
    wav.insert(holiday.index("Fourth of July"), ["firework.wav", "cannon.wav"])
    wav.insert(holiday.index("Halloween"), ["vampirehowl.wav", "spooky.wav", "jacko.wav"])
    wav.insert(holiday.index("Thanksgiving"), ["gobblegobble.wav", "pilgrim.wav"])
    wav.insert(holiday.index("Christmas"), ["jnglbell.wav", "hohoho.wav", "carolbells.wav"])
   

    currentholiday = holiday.index(get_holiday(date.today()))

    tone += 1
    if (tone >= len(wav[currentholiday])):
        tone =0

    return wav[currentholiday][tone]

# Tells script to play tone
def play():
        print('DING DONG')
        currentdoortone = doortone()
        print (currentdoortone)
        playcmd = 'aplay ' + currentdoortone + '  >/dev/null 2>&1'
        os.system(playcmd)
    
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
    now = datetime.now()
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