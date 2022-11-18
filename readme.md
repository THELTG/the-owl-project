# Python Programming for IoT
# Project Owl

## Koh Kai En (P2104175)
---

## Table of Contents

- [Libraries and setup](#Setup)
- [Functions](#functions)
- [User Guide](#user-guide)


---

## Setup

These are the dependencies used for project owl:

1) flask
2) cv2
3) numpy
4) telegram

Install these dependencies by running this command:

`pip3 install -r requirements.txt`

---

In order to start these services:

1) Motion detection
2) Telegram bot
3) Alarm System
4) Web Server

Simply run this command within the root directory of project owl in the raspberry pi:

`python3 server.py`

---

Apart from software, here is the hardware infrastructure:

![Infrastructure](./physical%20infra.png)

And here is how it looks like after setting everythin up:

![3D printed things](./how%20it%20looks.png)

--- 

## Functions

This section will guide you through the functions of this IoT device.

1) Motion Detection

- Detects motion through image processing using computer vision 2 (cv2) in python.
- Main source of information for other services
- Automatically captures images when a motion is detected

2) Telegram bot

- Allows users to communicate with the IoT device
- Ability to sound alarm at will
- A variety of commands for the user to use 


3) Alarm System

- Acts as a deterrant for any possible intrusions
- Alerts the owner if he/she is nearby
- Mainly uses motion detection as a trigger

4) Web Server

- Allows the user to have a live view of the area

---

## User Guide

1) Telegram

The invite link to the group chat with the bot is: https://t.me/+nwSxVbzIgu4xODM1

Here are the commands that the bot is listening out for when communicating with it.
- /start - Display this message
- /latest - Show the last picture taken
- /extractall - Send all images in an archive
- /beep - Beep the alarm
- /uptime - Shows the amount of time project owl has been running

2) Webserver
- navigate to the raspberrypi's ip address at port 8081
  (e.g. http://raspIPaddr:8081)

- default page shows the live stream of the camera 

3) desktop server.py
- This is the desktop version of server.py in which doesnt contain the RPi library
- The desktop version can be used the same way as the raspberry pi version with: `python "./desktop server.py"`


---

## Change(s) from original idea:

1) Email alerting has been changed to telegram reporting 
   - Reasons:
   - Allows users to easily communicate with the bot
   - Easier for the user to see telegram than to open an email app
   - Telegram offers a free API for bots while emails are restricted to a sandbox environment

---

## Parts used

|Physical Part Used|Specifications|
|:-------------|:-----------|
|Circuit board PCB|3cm x 7cm ZY2486A PCB|
|Raspberry pi|Model 4B 8gb RAM|
|Piezo buzzer|3.3~24V buzzer|
|White LED|3.3V LED light|
|Voltage booster|5V to 12V booster|
|Top casing|3D printed casing|
|Bottom casing|3D printed casing|
|Customised camera casing|3D printed casing|
|Miscellaneous parts|e.g. screws|

---

## Contributions

|Part of the project|Contribution|
|:-------------|:-----------|
|3D printing + modelling of the case|Kai En|
|Planning and designing of the project|Kai En|
|Purchasing of all the necessary parts|Kai En|
|Programming of the telegram bot|Kai En|
|Programming of the motion detection|Kai En|
|Programming of the webserver|Kai En|
|Programming of the raspberry pi's GPIO pins|Kai En|
|Web page design|Kai En|
|File system infrastructure|Kai En|
|Circuit board creation|Kai En|
|Integration of all the parts|Kai En|
|Testing of the project|Kai En|
|Documentation|Kai En|

---

## Credits for open-sourced projects

3D model of top casing: https://www.thingiverse.com/thing:922740


**NOTE: Other items not listed here were originally created/designed**

