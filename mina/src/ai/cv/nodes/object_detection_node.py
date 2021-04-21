# In this module we get image data from sensor
import rospy
import os
from edgetpu.detection.engine import DetectionEngine
from imutils.video import VideoStream
from PIL import Image as pil_image
import argparse
import imutils
import time
import cv2
import streamlit as st
from loguru import logger
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

def callback(ros_image_data):
   rgb_image = CvBridge().imgmsg_to_cv2(ros_image_data, desired_encoding="rgb8")
   # rgb_undist = cv2.undistort(rgb_image, camera_info_K, camera_info_D)
   frame = imutils.resize(rgb_image, width=500)
   orig = frame.copy()
   frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   frame = pil_image.fromarray(frame)
   results = model.DetectWithImage(frame, threshold = confidence,keep_aspect_ratio=True, relative_coord=False)
   for r in results:
      box = r.bounding_box.flatten().astype("int")
      (startX, startY, endX, endY) = box
      label = labels[r.label_id]
      cv2.rectangle(orig, (startX, startY), (endX, endY),
               (0, 255, 0), 2)
      y = startY - 15 if startY - 15 > 15 else startY + 15
      text = "{}: {:.2f}%".format(label, r.score * 100)
      cv2.putText(orig, text, (startX, y),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
   cv2.imshow('Webcam', orig)
   cv2.waitKey(1)

if __name__ == '__main__': 
   args = {}
   labels_path = "/home/robotws1/Desktop/ROBOT/mina/src/ai/cv/nodes/object_detection/data/processed/coco_labels.txt"
   model = "/home/robotws1/Desktop/ROBOT/mina/src/ai/cv/nodes/object_detection/models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
   confidence = 0.3
   labels = {}
   # loop over the class labels file
   for row in open(labels_path):
      (classID, label) = row.strip().split(maxsplit=1)
      labels[int(classID)] = label.strip()
   model = DetectionEngine(model)
   try:
      rospy.init_node('object detection node', anonymous=True)
      image_sub = rospy.Subscriber('/camera/color/image_raw', Image,callback,queue_size=1)
      rospy.spin()
   except rospy.ROSException:
      pass
   