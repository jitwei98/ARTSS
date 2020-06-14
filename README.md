# ARTSS
**Automated Realtime Traffic Surveillance System**

Team EMANMAET: *Chuah Jin Wei, Lim Jit Wei, Chong Khe Yang, Lim Shuen*

## a) Problem Statement
With over 9000km of roads in Singapore today (and counting), monitoring accidents and ensuring the safety of road users is an increasingly difficult task which neccesitates a large amount of manpower.

Our group aims to increase the efficiency of staff monitoring the camera feeds as well as flag out dangerous driving activity that might not be noticed by an operator. We do so by flagging and detection of 2 things - (1) accidents/road incidents and (2) dangerous driving behaviour, including drink driving, falling asleep at the wheel, aggressive driving etc. We hope that this system would lead to faster response to incidents and possible prediction of accidents.

## b) Pitch Video
youtube link here

## c) Solution Architecture

## d) Solution Description

## e) Project Roadmap

## f) Getting Started

### Creating a Telegram Bot ###
1. Refer to instructions here (https://core.telegram.org/bots#3-how-do-i-create-a-bot)
1. Note down your Telegram bot token


### Node RED API ###
1. Replace `package.json` in Node RED source with `package.json` in this repo.
1. In the Node RED editor, click on the menu icon on the top right corner and select import, upload `node-red-api.json` in this repo.
1. Once the flow has been imported successfully, double click on any of the Telegram nodes, click on the edit button beside the Bot property of the node, and replace the Telegram bot token with your Telegram bot token acquired in the steps above.
1. Click deploy.
1. Find your Telegram bot on Telegram and send `/start` to subscribe to the traffic notifications. Send `/help` to see the list of available commands.


### Python Scripts ###
On a server/computer with the camera feed, run:
```
python3 -m venv venv
(venv) pip install -r requirements.txt
(venv) python3 vehicle-motion-path-detection.py
```

Note: 
The source of the camera feed can be changed in line 47 : vehicle-motion-path-detection.py
cap = cv.VideoCapture("test_video_4.mp4")

## h) Live Demo

## i) Technologies Used
[IBM Cloud](https://www.ibm.com/sg-en/cloud)

[OpenCV](http://opencv.org/)

[Node-RED](https://nodered.org/)

[Telegram Bot API](https://core.telegram.org/bots/api)

[Watson Studio AutoAI](https://www.ibm.com/sg-en/cloud/watson-studio/autoai)
