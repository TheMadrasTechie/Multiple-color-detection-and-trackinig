from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
 	
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
# 	help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
# 	help="max buffer size")
# args = vars(ap.parse_args())
fourcc = cv2.VideoWriter_fourcc(*'XVID')
cap = cv2.VideoCapture(0)
vs = cv2.VideoWriter('virus.avi',fourcc,20.0,(640,480))
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (44, 100, 100)
greenUpper = (64, 255, 255)
blueLower = (110, 100, 100)
blueUpper = (130, 255, 255)
redLower = (-10, 100, 100)
redUpper = (10, 130, 130)
pinkLower = (155, 100, 100)
pinkUpper = (175, 255, 255)
yellowLower = (20, 100, 100)
yellowUpper = (40, 255, 255)

font = cv2.FONT_HERSHEY_SIMPLEX
#pts = deque(maxlen=args["buffer"])
pts_green = deque(maxlen=64)
pts_blue = deque(maxlen=64)
pts_red = deque(maxlen=64)
pts_pink = deque(maxlen=64)
pts_yellow = deque(maxlen=64)
o=0
# if a video path was not supplied, grab the reference
# to the webcam
# if not args.get("video", False):
# 	vs = VideoStream(src=0).start()
 
# # otherwise, grab a reference to the video file
# else:
# 	vs = cv2.VideoCapture(args["video"])
 
# allow the camera or video file to warm up
time.sleep(2.0)

while True:
	# grab the current frame
	#fun = cap.read()
	frame = cap.read()#cv2.flip(fun,1)
 
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] #if args.get("video", False) else frame
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	# if frame is None:
	# 	break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	# construct a mask_green for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask_green
	mask_green = cv2.inRange(hsv, greenLower, greenUpper)
	mask_green = cv2.erode(mask_green, None, iterations=2)
	mask_green = cv2.dilate(mask_green, None, iterations=2)

	cnts_green = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts_green = cnts_green[0] if imutils.is_cv2() else cnts_green[1]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts_green) > 0:
		# find the largest contour in the mask_green, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts_green, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.putText(frame, "Green", (int(x-2), int(y-2)), font, 0.8, (0,255,0), 2, cv2.LINE_AA)
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(100, 255, 101), 2)
			cv2.circle(frame, center, 5, (0, 255, 0), -1)
 
	# update the points queue
	pts_green.appendleft(center)
		# loop over the set of tracked points
	for i in range(1, len(pts_green)):
		# if either of the tracked points are None, ignore
		# them
		if pts_green[i - 1] is None or pts_green[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		o=o+1
		#print("Virus Attack in Your Computer \t Virus Number"+str(o))
		#print("You will get a video called Virus")
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts_green[i - 1], pts_green[i], (0, 255,0 ), thickness)
    #blue
	mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
	mask_blue = cv2.erode(mask_blue, None, iterations=2)
	mask_blue = cv2.dilate(mask_blue, None, iterations=2)
	# find contours in the mask_green and initialize the current
	# (x, y) center of the ball
	cnts_blue = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts_blue = cnts_blue[0] if imutils.is_cv2() else cnts_blue[1]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts_blue) > 0:
		# find the largest contour in the mask_green, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts_blue, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.putText(frame, "Blue", (int(x-2), int(y-2)), font, 0.8, (255,0,0), 2, cv2.LINE_AA)
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(255, 0, 0), 2)
			cv2.circle(frame, center, 5, (255, 0, 0), -1)
 
	# update the points queue
	pts_blue.appendleft(center)
		# loop over the set of tracked points
	for i in range(1, len(pts_blue)):
		# if either of the tracked points are None, ignore
		# them
		if pts_blue[i - 1] is None or pts_blue[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		o=o+1
		#print("Virus Attack in Your Computer \t Virus Number"+str(o))
		#print("You will get a video called Virus")
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts_blue[i - 1], pts_blue[i], (255, 0,0 ), thickness)


	mask_red = cv2.inRange(hsv, redLower, redUpper)
	fun = cv2.erode(mask_red, None, iterations=2)
	mask_red = cv2.dilate(mask_red, None, iterations=2)
	# find contours in the mask_green and initialize the current
	# (x, y) center of the ball
	cnts_red = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts_red = cnts_red[0] if imutils.is_cv2() else cnts_red[1]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts_red) > 0:
		# find the largest contour in the mask_green, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts_red, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.putText(frame, "Red", (int(x-2), int(y-2)), font, 0.8, (0,0,255), 2, cv2.LINE_AA)
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 0, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts_red.appendleft(center)
		# loop over the set of tracked points
	for i in range(1, len(pts_red)):
		# if either of the tracked points are None, ignore
		# them
		if pts_red[i - 1] is None or pts_red[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		o=o+1
		#print("Virus Attack in Your Computer \t Virus Number"+str(o))
		#print("You will get a video called Virus")
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts_red[i - 1], pts_red[i], (0, 0,255 ), thickness)	

	
	mask_pink = cv2.inRange(hsv, pinkLower, pinkUpper)
	mask_pink = cv2.erode(mask_pink, None, iterations=2)
	mask_pink = cv2.dilate(mask_pink, None, iterations=2)
	# find contours in the mask_green and initialize the current
	# (x, y) center of the ball
	cnts_pink = cv2.findContours(mask_pink.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts_pink = cnts_pink[0] if imutils.is_cv2() else cnts_pink[1]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts_pink) > 0:
		# find the largest contour in the mask_green, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts_pink, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.putText(frame, "pink", (int(x-2), int(y-2)), font, 0.8, (128,0,255), 2, cv2.LINE_AA)
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(128, 0, 255), 2)
			cv2.circle(frame, center, 5, (128, 0, 255), -1)
 
	# update the points queue
	pts_pink.appendleft(center)
		# loop over the set of tracked points
	for i in range(1, len(pts_pink)):
		# if either of the tracked points are None, ignore
		# them
		if pts_pink[i - 1] is None or pts_pink[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		o=o+1
		#print("Virus Attack in Your Computer \t Virus Number"+str(o))
		#print("You will get a video called Virus")
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts_pink[i - 1], pts_pink[i], (128, 0,255 ), thickness)		

	mask_yellow = cv2.inRange(hsv, yellowLower, yellowUpper)
	mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
	mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)
	cnts_yellow = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts_yellow = cnts_yellow[0] if imutils.is_cv2() else cnts_yellow[1]
	center = None
	if len(cnts_yellow) > 0:
		c = max(cnts_yellow, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.putText(frame, "yellow", (int(x-2), int(y-2)), font, 0.8, (0,255,255), 2, cv2.LINE_AA)
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 255, 255), -1)
	pts_yellow.appendleft(center)
	for i in range(1, len(pts_yellow)):
		if pts_yellow[i - 1] is None or pts_yellow[i] is None:
			continue
		o=o+1
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts_yellow[i - 1], pts_yellow[i], (	 ), thickness)		
	dd = cv2.flip(frame, 1)
	cv2.imshow("Ball", dd)
	cv2.imshow("fun", fun)
	vs.write(dd)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
vs.release()
cv2.destroyAllWindows()