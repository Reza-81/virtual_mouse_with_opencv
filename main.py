import time
import cv2
import numpy as np
import pyautogui
from HandTrackingModule import handDetector
pyautogui.FAILSAFE = False

p_time = 0
c_time = 0
tracking_mouse_pointer = False
capture = cv2.VideoCapture(0)
w_cam, h_cam = 920, 700
w_rectangle_1, h_rectangle_1 = 250, 300
w_rectangle_2, h_rectangle_2 = 250, 150
accuracy_movement = 10
accuracy_click = 25
capture.set(3, w_cam)
capture.set(4, h_cam)
detector = handDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)

while (True):
    # make image
    success, image = capture.read()
    image = cv2.flip(image, 1)
    detector.findHands(image, draw=True)

    #showing the specific hand land mrks
    list_land_marks = detector.findPosition(image)

    if list_land_marks:
        #mouse pointer
        x = (np.interp(list_land_marks[0][1], [w_rectangle_1, w_cam - w_rectangle_2], [0, pyautogui.size()[0]])) // accuracy_movement * accuracy_movement
        y = (np.interp(list_land_marks[0][2], [h_rectangle_1, h_cam - h_rectangle_2], [0, pyautogui.size()[1]])) // accuracy_movement * accuracy_movement
        up_fingers_list = detector.find_up_fingers(list_land_marks)
        # turn of and trun on tracking
        if up_fingers_list[1:] == [0, 0, 0, 0]:
            tracking_mouse_pointer = not tracking_mouse_pointer
            time.sleep(0.5)
        if tracking_mouse_pointer:
            #scroll
            if up_fingers_list[1:] == [1, 0, 0, 0]:
                pyautogui.scroll(50)
            elif up_fingers_list[1:] == [1, 0, 0, 1]:
                pyautogui.scroll(-50)
            # left click
            if up_fingers_list[1] and up_fingers_list[2] and abs(list_land_marks[8][1] - list_land_marks[12][1]) < accuracy_click:
                pyautogui.click(x, y)
            # right click
            elif up_fingers_list[2] and up_fingers_list[3] and abs(list_land_marks[12][1] - list_land_marks[16][1]) < accuracy_click:
                pyautogui.rightClick(x, y)
            # move
            else:
                cv2.circle(image, (list_land_marks[0][1], list_land_marks[0][2]), 10, (255, 0, 255), cv2.FILLED)
                pyautogui.moveTo(x ,y)

    # find fps
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time