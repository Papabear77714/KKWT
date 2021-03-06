#!/usr/bin/python3 -u

#
# Not going to win any awards this one, is it?
#
# The Pi is wired up such that pin 18 goes through the switch to ground.
# The on-pin pull-up resistor is enabled (so .input() is normally True).
# When the circuit completes, it goes to ground and hence we get a
# falling edge and .input() becomes False.
#
# I get the occasional phantom still so we wait for settle_time before
# thinking it's real.
#

from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from datetime import datetime

import RPi.GPIO as GPIO
import subprocess
import alsaaudio
import threading
import signal
import wave
import time
import sys
import os

samplefile = sys.argv[1]
device='plughw:1,0'

# in seconds
settle_time = 0.1
bounce_time = 1

active = False

def notify():
    subprocess.run(['/home/pi/notify-sent'])

    msg = MIMEText('At %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    msg['From'] = 'doorbell <levon@movementarian.org>'
    msg['To'] = 'John Levon <john.levon@gmail.com>'
    msg['Subject'] = 'Someone is ringing the doorbell'

    p = Popen(['/usr/sbin/sendmail', '-f', 'levon@movementarian.org', '-t', '-oi'], stdin=PIPE)
    p.stdin.write(msg.as_string().encode())
    p.stdin.close()

def play():
    global samplefile
    global active

    active = True
    count = 0

    with wave.open(samplefile) as f:

        format = None

        # 8bit is unsigned in wav files
        if f.getsampwidth() == 1:
            format = alsaaudio.PCM_FORMAT_U8
        # Otherwise we assume signed data, little endian
        elif f.getsampwidth() == 2:
            format = alsaaudio.PCM_FORMAT_S16_LE
        elif f.getsampwidth() == 3:
            format = alsaaudio.PCM_FORMAT_S24_3LE
        elif f.getsampwidth() == 4:
            format = alsaaudio.PCM_FORMAT_S32_LE
        else:
            raise ValueError('Unsupported format')

        rate = f.getframerate()

        periodsize = rate // 8

        out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, device=device)
        out.setchannels(f.getnchannels())
        out.setrate(rate)
        out.setformat(format)
        out.setperiodsize(periodsize)

        # We always play at least one time round...
        while active or count < 1:
            data = f.readframes(periodsize)

            if data:
                out.write(data)
            else:
                print('looping after %d plays, active %s' % (count, active))
                count += 1
                f.rewind()

        print('pausing audio')
        out.pause()

    print('stopped after %d plays' % count)

def wait():
    global active

    while True:
        input_state = GPIO.input(18)
        if input_state:
            print('got input_state %s, active -> False' % input_state)
            active = False
            break
        time.sleep(0.2)

def trigger():
    print('triggering at %s' % time.time())

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
    print('input state now %s' % input_state)
    return not input_state

def falling_edge(channel):
    input_state = GPIO.input(18)
    print('got falling edge, input_state %s' % input_state)
    if settle():
        trigger()

with wave.open(samplefile) as f:
    # things go horrible if the rate isn't 48000 for some reason
    if f.getframerate() != 48000:
        raise ValueError('file must be 48000 rate')
    if f.getsampwidth() not in [ 1, 2, 3, 4]:
            raise ValueError('Unsupported format')

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=falling_edge, bouncetime=(bounce_time * 1000))

print('started')

signal.pause()