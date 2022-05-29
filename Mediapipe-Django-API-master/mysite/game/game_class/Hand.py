import copy
import itertools
import csv

import mediapipe as mp
import cv2

from mysite.game.game_class.Const import Const
from script.model import KeyPointClassifier


class Hand:
    def __init__(self):
        self.hand_sign_id = None
        self.landmark_MIDDLE_FINGER_TIP = []

        self.keypoint_classifier = KeyPointClassifier()
        # Read labels ###########################################################
        with open('mysite/game/game_class/object_detect/hand/model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5
        )

    def hand_detect(self, frame):
        hand_is_true = False
        debug_image = copy.deepcopy(frame)

        debug_image.flags.writeable = False
        results = self.hands.process(debug_image)  # 손인식 결과의 객체를 얻어오는 함수
        debug_image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            hand_is_true = True
            # draw result landmarks
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)
                self.landmark_MIDDLE_FINGER_TIP = landmark_list[12]
                # print(self.landmark_MIDDLE_FINGER_TIP)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = self.pre_process_landmark(
                    landmark_list)

                # Hand sign classification
                self.hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)

                debug_image = self.draw_hand_classification(debug_image, self.keypoint_classifier_labels[self.hand_sign_id])
        else:
            self.landmark_MIDDLE_FINGER_TIP = None
            self.hand_sign_id = None

        return hand_is_true, debug_image

    def get_hand_result(self):
        return self.hand_result

    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def draw_hand_classification(self, image, hand_sign_id):
        cv2.putText(image, "YOUR STEP: " + hand_sign_id, (10, 120),
                    Const.FONT, 0.6, (255, 255, 255), 1,
                    cv2.LINE_AA)

        return image
