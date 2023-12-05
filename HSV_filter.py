import time
import cv2
import numpy as np

def add_HSV_filter(frame, camera):

    # blurr the image
    blur = cv2.GaussianBlur(frame, (5,5), 0)

    # convert rgb to hsv
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # lower limit for red cube
    l_b_r = np.array([60, 110, 50])
    # upper limit for red cube 
    u_b_r = np.array([255, 255, 255])
    # lower limit for red cube
    l_b_l = np.array([143, 110, 50])
    # upper limit for red cube
    u_b_l = np.array([255, 255, 255])

    if camera == 1:
        mask = cv2.inRange(hsv, l_b_r, u_b_r)
    else:
        mask = cv2.inRange(hsv, l_b_l, u_b_l)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask