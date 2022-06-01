import cv2
import mediapipe as mp
import numpy as np


class Chopstick:

    def __init__(self):
        self.weight = cv2.dnn.readNet('mysite/game/game_class/object_detect/chopstick/yolov3-tiny_training_05-22.weights',
                                      'mysite/game/game_class/object_detect/chopstick/yolov3-tiny_testing.cfg')
        self.classes = []
        with open("mysite/game/game_class/object_detect/chopstick/classes.txt", "r") as f:
            self.classes = f.read().splitlines()

        self.boxes = []

    def check_chopstick(self, img, landmark_MIDDLE_FINGER_TIP):
        image_width, image_height = img.shape[1], img.shape[0]
        self.boxes.clear()

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        self.weight.setInput(blob)
        output_layers_names = self.weight.getUnconnectedOutLayersNames()
        layerOutputs = self.weight.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.1:
                    center_x = int(detection[0] * image_width)
                    center_y = int(detection[1] * image_height)

                    w = int(detection[2] * image_width)
                    h = int(detection[3] * image_height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.boxes.append([x, y, 50, h])
                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(self.boxes, confidences, 0.2, 0.4)
        # indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)


        if len(indexes) > 0:
            for i in indexes.flatten():
                # x, y, w, h = self.boxes[i]
                x, y, w, h = boxes[i]

                label = str(self.classes[class_ids[i]])

                confidence = str(round(confidences[i], 2))
                print("정리", x, y)
                img = cv2.rectangle(img, (x, y), (x +50, y+h), (255, 0, 0), 1)
                # img = cv2.putText(img, label + " " + confidence, (x, y + 20), Const.FONT, 2, (255, 255, 255), 2)

        return img
