import sys
import cv2
import numpy as np
import time
import imutils
import matplotlib.pyplot as plt
import HSV_filter as hsv
import find_cubes as cubes
import triangulation as tri

# open both cameras
cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap_left = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# set camera frame rate 
frame_rate = 120

# set distance between cameras
B = 14
# set camera's lense focal length
f = 4.1
# camera field of view in the horizontal plane in degrees
alpha = 90

# break counter 
b_counter = 0
counter = 0

while(True):
    counter += 1
    # if object detected, wait 5 and break
    # if b_counter >= 5:
    #     break

    ret_right, frame_right = cap_right.read()
    ret_left, frame_left = cap_left.read()

    # if cannot catch any frame, break
    if not ret_right or not ret_left:
        print("here")
        break
    else:    
        # apply hsv filter
        mask_right = hsv.add_HSV_filter(frame_right, 1)
        mask_left = hsv.add_HSV_filter(frame_left, 0)

        # result frames after applying hsv_filter mask
        res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
        res_left = cv2.bitwise_and(frame_left, frame_left, mask=mask_left)

        # apply shape recognition
        circles_right = cubes.find_cubes(frame_right, mask_right)
        circles_left = cubes.find_cubes(frame_left, mask_left)

        # calculate depth
        if not np.all(circles_right) or not np.all(circles_left):
            cv2.putText(frame_right, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame_left, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            
            # start counter 
            b_counter += 1

            # get coords
            depth = tri.find_depth(circles_right, circles_left, frame_right, frame_left, B, f, alpha)
            cv2.putText(frame_right, "TRACKING", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            cv2.putText(frame_left, "TRACKING", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            cv2.putText(frame_right, f"DISTANCE: {str(round(depth, 3))}", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            cv2.putText(frame_left, f"DISTANCE: {str(round(depth, 3))}", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)

            #print("Depth: ", depth)

            # show frames
            cv2.imshow("frame right", frame_right)
            cv2.imshow("frame left", frame_left)
            #cv2.imshow("mask right", mask_right)
            #cv2.imshow("mask left", mask_left)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()


        