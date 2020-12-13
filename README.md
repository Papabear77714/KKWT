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
        sudo apt-get install python3-venv
        sudo apt-get install dos2unix
        python3 -m venv .venv
        pip install slack_sdk
        pip install RPi.GPIO
        source .venv/bin/activate
        export SLACK_BOT_TOKEN=xoxb-your-token
        export KKWT_NAME=Your_name
````

## Installation
Copy the files using WinSCP or Cyberduck (Or any software you prefere) to the Pi. You can create a KKWT folder, or leave it on the Pi home folder. There are two files that you need to copy:
* kkwt.py
* ding-dong.wav
Once you have the two files loaded, connect to your Pi's shell. You can use your Mac's SSH command, or use Putty if you are using Windows. If you are using Windows, you may have to run dos2unix. Here is the code to do so:
````
        dos2unix kkwt.py
````
Make sure that both files are in the same directory. This completes the installation steps.

## Running
From a shell prompt change directories into the folder where you installed the two files. Run the following command:
````
        python3 kkwt.py
````
Leave the script running. Whenever the doorbell is pressed, you will get an audible tone locally, as well as a posting to the Slack channel with a message that your doorbell has rang. To stop the program from running, simply press Ctrl+C.

## Recomendations
Once you have the script running, you can exit the shell, however, if you want to be able to connect back to the same session and end the running script, you can install screen on your Pi. To do so, issue the following command:
````
        sudo apt-get install screen
````
Once the program is installed, start the program by typing screen. Press the enter key. Enter the following commands:
````
        source .venv/bin/activate
        export SLACK_BOT_TOKEN=xoxb-your-token
        export KKWT_NAME=Your_name
````
You are now ready to start the program like before. Type:
````
        python3 kkwt.py
````
Next, press Ctrl+A and then D. That will detach you from the *screen*. You can now exit Putty or close the session. The program will continue to run in the background. Once you are ready to reconnect, log back onto the Pi, and issue the **screen -ls** command. This will list the running screens. Look for the screen number, and type **screen -r 1234** with 1234 being the screen number you found. This will reattach you to the screen. You can exit the program by pressing Ctrl+C. And, you can terminate the screen by issuing the **exit** command.