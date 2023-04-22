import sys
import cv2 as cv
import numpy as np
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
def main(argv):
    
    # default_file = 'smarties.png'
    # filename = argv[0] if len(argv) > 0 else default_file
    # # Loads an image
    # src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
    # # Check if image is loaded fine
    # if src is None:
    #     print ('Error opening image!')
    #     print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
    #     return -1
    vs = VideoStream(src=0).start()


    while(True):
        
        img = vs.read()

# Convert BGR to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define yellow color range in HSV color space
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Threshold the HSV image to get only yellow pixels
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply Morphological Transformations to remove noise
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Display the result
        cv2.imshow('Yellow Pixels Only', mask)
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
    
    return 0
if __name__ == "__main__":
    main(sys.argv[1:])