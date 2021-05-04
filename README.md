Mina
==============================

# About 

Mina is an autonomous robot.  Integration of ros framework with artificial intelligence package is crucial work. In mina, I am trying to integrate ros with the python package.
In technical terms, ros publisher publishes data sensor data and I subscribe that data and fit this data to a machine learning model for prediction.
After the prediction machine learning model did some decisions that decision are published by the publisher and subscriber subscribe this decision and to act.

## [Robot Operating System (ROS)](http://wiki.ros.org/Documentation)

I follow [ros wiki](http://wiki.ros.org/ROS/Tutorials) for my ros study.
Here is the notebook for ros study.


# Project setup
``` 
pip3 install -r requirements.txt

cd mina

catkin_make

roslaunch base_rover base_rover.launch   # most important when we lunch this , all sensor throw data throw node, so we just need to collect this data and do process


```

# Table of Contents
=================

  * [Computer Vision](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv)
    * [Object Detection](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv/nodes/object_detection)
    * [Face recognition](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv/nodes/face-recognition)
    * [Face recognition azurefaceapi](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv/nodes/face_recognition)
    * ![object detection](https://github.com/MadanBaduwal/ros_robot/blob/main/mina%20object%20detection.gif)

  * [NLP](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/nlp)
    * [Chatbot](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/nlp/chatbot)
  * [RL](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/rl) 

**Note : In ros everythin is publisher and subscriber, they are the python module with collect data from sensor and publish data for sensor.**
