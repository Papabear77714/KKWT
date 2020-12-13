# Knock, Knock, Who's There (KKWT) Project
A Raspberry Pi project for the Code Devils Hackathon 2020

1. Original PiBell code from https://movementarian.org/blog and Slackbot code from Dr. Mehlhase
    1. we take no credit for originality of code.
    1. changes made to reduce clutter and clean coding up to make it simple.
    1. Some cleanup included removing messaging at the beginning
    1. Code posted on this GitHub for judges to review
1. Configured on Pi with doorbell and USB speaker. Doorbell wired to go to Pi GPIO 18 and ground. 
    1. Best speaker to use is one that requires no power or has no timeout on it
1. Idea used for CodeDevils Hackathon Fall 2020.

## Pre-installation Steps
There are two modes that you can run your Raspberry Pi in:
- Desktop Version
- No Desktop
I recommend that you run it with no desktop as this will run best in a *headless* state. However, you can also run this in desktop version.

Once you have the OS loaded onto the Pi, enable SSH. SSH will facilite remote connectivity as well as file transfer from your computer. Run the following commands to run the project:
````
        sudo apt-get update
        sudo apt-get install python3-rpi.gpio
        sudo apt-get install python3-alsaaudio
        sudo apt-get install dos2unix
        python3 -m venv .venv
        source .venv/bin/activate
````

## Installation
Copy the files using WinSCP or Cyberduck (Or any software you prefere) to the Pi. You can create a KKWT folder, or leave it on the Pi.
