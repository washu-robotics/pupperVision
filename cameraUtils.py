# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


# color thresholds
yellowLower = (19, 12, 199)
yellowUpper = (68, 255, 255)

pts = deque()

vs = None

lastVal = 0
lastTime = 0

def onCam():
	global vs
	vs = VideoStream(src=0).start()


def getBallX():
	global vs, lastTime, lastVal
	# grab the current frame
	if vs is None: return 0

	curTime = time.time();
	if (curTime-lastTime < .5):
		return lastVal
	else:
		lastTime = curTime
		
	frame = vs.read()

	if frame is None: 
		print("broke") 
		return

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	#process
	mask = cv2.inRange(hsv, yellowLower, yellowUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)


	cnts = imutils.grab_contours(cnts)
	center = None

	contour_list = []
	for contour in cnts:
		approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
		area = cv2.contourArea(contour)
		if ((len(approx) > 8) & (area > 30) ):
			contour_list.append(contour)
	# cv2.drawContours(frame, contour_list, -1, (0,255,0), 3)

	x = 0
	
	# only proceed if at least one contour was found
	if len(contour_list) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(contour_list, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		# M = cv2.moments(c)
		# center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	else:
		return 0

	# x is right most 0 and leftmost 600
	x = ((x-300)/300)*(0.6)
	lastVal = x
	return x


def stopCam():
	global vs
	vs.stop()

onCam()
start = time.time()
getBallX()
end = time.time()
print(end - start)