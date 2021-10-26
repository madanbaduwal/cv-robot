Ai base robot
==============================


Ai base robot is an autonomous robot.  Integration of ros framework with artificial intelligence package is crucial work. The basic theme of this project is to try to mimic the human. How humans sense from their five senses and decide to do something, similarly ai robots sense from sensors and ai algorithms decide to do something.
In technical terms, ros publisher publishes data sensor data and I subscribe that data and fit this data to a machine learning model for prediction.
After the prediction machine learning model did some decisions that decision are published by the publisher and subscriber subscribe this decision and to act.

  ![Gazebo Simulation](https://github.com/MadanBaduwal/ros_robot/blob/main/mina%20object%20detection.gif)
  
   Gif : Gazebo Simulation
   
  ![Real life implementation](https://github.com/MadanBaduwal/robot/blob/main/AI%20autonomous%20robot.gif)
  
   Gif : Real life implementation

# Table of Contents
=================

 * [Computer Vision](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv)
   * [Object Detection](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv/nodes/object_detection)
   * [Face recognition](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv/nodes/face-recognition)
   * [Face recognition azurefaceapi](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/cv/nodes/face_recognition)

 * [NLP](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/nlp)
   * [Chatbot](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/nlp/chatbot)
 * [RL](https://github.com/MadanBaduwal/robot/tree/main/mina/src/ai/rl) 


# Installation and configuration fire
```shell
pip3 install -r requirements.txt

cd mina

catkin_make

roslaunch base_rover base_rover.launch   # most important when we lunch this , all sensor throw data throw node, so we just need to collect this data and do process
```

**Note : In ros everythin is publisher and subscriber, they are the python module with collect data from sensor and publish data for sensor.There are lots of library in ros which collect data from sensor(in .yaml file)**

# Resources
* [Robot Operating System (ROS)](http://wiki.ros.org/Documentation)

* I follow [ros wiki](http://wiki.ros.org/ROS/Tutorials) for my ros study.
Here is the notebook for ros study.
