import sys
import cv2
import numpy as np
import time
import imutils
import matplotlib.pyplot as plt
import HSV_filter as hsv
import find_cubes as cubes
import triangulation as tri

# open camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# set camera's lense focal length
f = 4.1
# camera field of view in the horizontal plane in degrees
alpha = 90

while(True):

    ret, frame = camera.read()
    
    frame = cv2.flip(frame, 1)
    frame = frame[40:260, 180:400] # TODO
    (h, w) = frame.shape[:2]
    #print(h, w)
    # break if camera not responding
    if not ret:
        raise Exception("Camera malfunction")

    else:    
        # apply hsv filter
        mask = hsv.add_HSV_filter(frame, 1)

        # result frames after applying hsv_filter mask
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # apply shape recognition
        circles, coords = cubes.find_circles(frame, mask)

        # transform coords to cm
        new_x = coords[0] * 15 / 110
        new_y = coords[1] * 12.5 / 110

        # show message
        cv2.putText(frame, f"X: {str(round(new_x, 3))}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
        cv2.putText(frame, f"Y: {str(round(new_y, 3))}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)


        # show frames
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)

        # breaking process
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()