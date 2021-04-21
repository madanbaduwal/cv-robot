# In this module we get image data from sensor
import rospy
import os
import sys
import streamlit as st
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import message_filters
import cv2
import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo, Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from cv_node_script import app

def callback(rgb_msg, camera_info):
   #print("Start call back function")
   global prev_img
   rgb_image = CvBridge().imgmsg_to_cv2(rgb_msg, desired_encoding="rgb8")
   camera_info_K = np.array(camera_info.K).reshape([3, 3])
   camera_info_D = np.array(camera_info.D)
   rgb_undist = cv2.undistort(rgb_image, camera_info_K, camera_info_D)
   #print(rgb_image)
   app(rgb_image)
   # myfunction(data/rgb_image)

if __name__ == '__main__': 
   #print("start my_node")
   rospy.init_node('my_node', anonymous=True)
   # image_sub = message_filters.Subscriber('/ardrone/front/image_raw', Image)
   # info_sub = message_filters.Subscriber('/ardrone/front/camera_info', CameraInfo)
   image_sub = message_filters.Subscriber('/camera/color/image_raw', Image)
   info_sub = message_filters.Subscriber('/camera/color/camera_info', CameraInfo)
   #print(image_sub)
   #print("Take all data from sensor")
   ts = message_filters.ApproximateTimeSynchronizer([image_sub, info_sub], 10, 0.2)
   #print(ts)
   ts.registerCallback(callback)
   #print("Called callback function")
   #print("Start sapin")
   rospy.spin()
   