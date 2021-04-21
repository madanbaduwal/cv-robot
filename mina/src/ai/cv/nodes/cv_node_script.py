# In this module we do object detection and render it in streamlit web app

# import the necessary packages
from edgetpu.detection.engine import DetectionEngine
from imutils.video import VideoStream
from PIL import Image
import argparse
import imutils
import time
import cv2
import streamlit as st
from loguru import logger

args = {}
args["labels"] = "/home/robotws1/Desktop/ROBOT/mina/src/ai/cv/nodes/object_detection/data/processed/coco_labels.txt"
args["model"] = "/home/robotws1/Desktop/ROBOT/mina/src/ai/cv/nodes/object_detection/models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
args["confidence"] = 0.3
FRAME_WINDOW  = st.image([])
st.title("HI")
# initialize the labels dictionary
logger.info("[INFO] parsing class labels...")
labels = {}
# loop over the class labels file
for row in open(args["labels"]):
	#logger.info("[INFO] unpack the row and update the labels dictionary")
	(classID, label) = row.strip().split(maxsplit=1)
	labels[int(classID)] = label.strip()
# load the Google Coral object detection model
logger.info("[INFO] loading Coral model...")
model = DetectionEngine(args["model"])
# initialize the video stream and allow the camera sensor to warmup


def app(image):

	# loop over the frames from the video stream
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 500 pixels
	#logger.info("[INFO] finished video stream")
	frame = image
	#cv2.imshow('image',frame)
	#print(frame)
	frame = imutils.resize(frame, width=500)
	orig = frame.copy()
	# prepare the frame for object detection by converting (1) it
	# from BGR to RGB channel ordering and then (2) from a NumPy
	# array to PIL image format
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = Image.fromarray(frame)
	#print(frame)
	# make predictions on the input frame
	start = time.time()
	results = model.DetectWithImage(frame, threshold=args["confidence"],
		keep_aspect_ratio=True, relative_coord=False)
	#logger.info(f"[INFO] prediction result:{results}")
	end = time.time()
	
	# loop over the results
	for r in results:
		# extract the bounding box and box and predicted class label
		box = r.bounding_box.flatten().astype("int")
		(startX, startY, endX, endY) = box
		#logger.info(f"[INFO] boundry box is:,{box}")
		label = labels[r.label_id]
		print(label)
		#logger.info(f"[INFO] predicted label:,{label}")
		# draw the bounding box and label on the image
		cv2.rectangle(orig, (startX, startY), (endX, endY),
					(0, 255, 0), 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		text = "{}: {:.2f}%".format(label, r.score * 100)
		cv2.putText(orig, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	# show the output frame and wait for a key press
	    #cv2.imshow("Frame", orig)
	#FRAME_WINDOW.image(orig)
	cv2.imshow('Webcam', orig)
	cv2.waitKey(1)