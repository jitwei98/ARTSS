# ARTSS
**Automated Realtime Traffic Surveillance System**

Team EMANMAET: *Chuah Jin Wei, Lim Jit Wei, Chong Khe Yang, Lim Shuen*

## a) Problem Statement
With over 9000km of roads in Singapore today (and counting), monitoring accidents and ensuring the safety of road users is an increasingly difficult task which neccesitates a large amount of manpower.

Our group aims to increase the efficiency of staff monitoring the camera feeds as well as flag out dangerous driving activity that might not be noticed by an operator. 

We do so by flagging and detection of the following:
1. Accidents/road incidents
2. Dangerous driving behaviour, including drink driving, falling asleep at the wheel, aggressive driving etc.

We hope that this system would lead to faster response to incidents and possible intervention to reduce the chances of accidents.

## b) Pitch Video
https://youtu.be/GCLLyg7mdAA

## c) Solution Architecture
![Architecture](https://github.com/jitwei98/Emanmaet-ARTSS_SCDFXIBM/blob/master/solution-architecture.png)

## d) Solution Description
Our solution tracks objects on the road, as well as its motion across frames. With this data, we are able to detect dangerous driver behavior by extracting details such as the speed of the lane change (aggressive or drunk driving) or if the car is drifting between lanes (falling asleep at the wheel). 

This could preempt possible incidents, allowing for proper action to be prepared - dispatching of personnel or alerting of the driver via led street signs etc.

Our solution consists of Python scripts running on servers, with the camera feeds as input. When dangerous driver behaviors are detected, a HTTP request with the camera location information is sent to an API endpoint built using Node RED, and the Node RED API will push the notifications to the preferred notification platform (such as SMS, a Web dashboard etc.), for the demo purpose of this hackathon, we use a Telegram bot with a simple subscribe/unsubscribe funtion to broadcast the notifications.

### High level overview of the Python script
1. Read a video/camera feed using OpenCV's [cv.VideoCapture()](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-videocapture) and decodes the video frame using [VideoCapture::read](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-read)
1. Detect the lanes using OpenCV's [findContours()](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga17ed9f5d79ae97bd4c7cf18403e1689a) function, the lanes are hardcoded in the demo because we could not find footage of the road without traffic.
1. Convert each frame to grayscale
1. Select the pixels to track using Shi-Tomasi Corner Detector [[ref]](https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack)
1. Estimate the motion of the tracked pixels using the Lucas-Kanade method [[ref]](https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk)
1. If a tracked pixel switched between different lanes (labelled as different contours in step 2) more than X times in the span of Y frames, where X and Y are parameters that can be configured manually, send a HTTP request with the camera location to the Node RED API endpoint to broadcast the information.
1. Visualize the motion path for each frame


### Node RED API
1. Listen to HTTP request from the Python script(s)
1. Broadcast notifications to preferred platform (we used a simple Telegram bot with a subscribe/unsubscribe function for this hackathon)

## f) Getting Started

### Creating a Telegram Bot ###
1. Refer to the instructions [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
1. Note down your Telegram bot token.


### Node RED API ###
1. Replace `package.json` in Node RED source with `package.json` in this repo.
1. In the Node RED editor, click on the menu icon on the top right corner and select import, upload `node-red-api.json` in this repo.
1. Once the flow has been imported successfully, double click on any of the Telegram nodes, click on the edit button beside the Bot property of the node, and replace the Telegram bot token with your Telegram bot token acquired in the steps above.
1. Click deploy.
1. Find your Telegram bot on Telegram and send `/start` to subscribe to the traffic notifications. Send `/help` to see the list of available commands.

(Optional) Securing your Node RED API endpoints: refer to the instructions [here](https://nodered.org/docs/user-guide/runtime/securing-node-red#http-node-security).

### Python Scripts ###
On a server/computer with the camera feed, run:
```
python3 -m venv venv
(venv) pip install -r requirements.txt
(venv) python3 vehicle-motion-path-detection.py
```

Note: 
The source of the camera feed can be changed on `line 47 : vehicle-motion-path-detection.py`
```
cap = cv.VideoCapture("test_video_4.mp4")
```

## i) Technologies Used
[IBM Cloud](https://www.ibm.com/sg-en/cloud)

[OpenCV](http://opencv.org/)

[Node-RED](https://nodered.org/)

[Telegram Bot API](https://core.telegram.org/bots/api)

[Watson Studio AutoAI](https://www.ibm.com/sg-en/cloud/watson-studio/autoai)
