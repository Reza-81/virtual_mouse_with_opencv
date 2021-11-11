import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence = 0.5
                 , min_tracking_confidence = 0.5):
        #initialize the Required paramiters for creat hand
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        #creat object to detect hand
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode, max_num_hands, min_detection_confidence
                                         , min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def findHands(self, image, draw=False):
        #creat image
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # find hand land marks
        self.results = self.hands.process(image_rgb)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, hand_number=0, draw=False):
        land_mark_list = []

        if self.results.multi_hand_landmarks:
            my_hand_land_mark = self.results.multi_hand_landmarks[hand_number]
            for id, land_mark_coordinate in enumerate(my_hand_land_mark.landmark):
                height, width, chanel = image.shape
                coordinate_x, coordinate_y = int(width * land_mark_coordinate.x), int(
                    height * land_mark_coordinate.y)
                land_mark_list.append([id, coordinate_x, coordinate_y])
                if draw:
                    cv2.circle(image, (coordinate_x, coordinate_y), 10, (255, 0, 255), cv2.FILLED)
        return land_mark_list

    def find_up_fingers(self, land_mark_list):
        up_fingers_list = 5 * [0]

        # checking the position of top pointer on each fingers with under pointer
        for i in range(4, 21, 4):
            if land_mark_list[i][2] < land_mark_list[i-1][2]:
                up_fingers_list[i//4-1] = 1

        return up_fingers_list