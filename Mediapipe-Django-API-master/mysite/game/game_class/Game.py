import copy

import cv2
import time

import cvzone as cvzone
import numpy as np
from PIL import Image

from mysite.core.models import Ranking, UserGameRecord
from mysite.game.game_class.Camera import Camera
from mysite.game.game_class.Chopstick import Chopstick
from mysite.game.game_class.Hand import Hand
from mysite.game.game_class.Star import Star


class Game:
    def __init__(self, mode="easy", user=None):
        self.user = user

        self.mode = mode
        self.speed = 0

        self.game_mode()  # speed = vanishing time

        self.chopstick = Chopstick()
        self.camera = Camera()
        self.hand = Hand()

        self.regen_time = float(self.speed) / float(2)
        self.stars = []

        tempstarImage = cv2.imread("mysite/game/game_class/image/star.png", cv2.IMREAD_UNCHANGED)
        self.starSize = 80
        self.starImage = cv2.resize(tempstarImage, (self.starSize, self.starSize))

        self.score = 0


    def game_mode(self):
        if self.mode == "easy":  # easy
            self.speed = 10
        elif self.mode == "normal":
            self.speed = 7
        elif self.mode == "hard":
            self.speed = 5

    def get_frame(self, now):
        success, image = self.camera.video.read()
        if success:
            image = self.game(now)

        return image

    def game(self, now):

        # get Image
        ret, image = self.camera.video.read()

        image = cv2.flip(image, 1)
        image_width, image_height = image.shape[1], image.shape[0]

        # 손인식
        hand_is_true, image = self.hand.hand_detect(image)

        # 손인식 되었으면 chopstick 확인, 중지와 가까이있는 이미지두개만 출력
        if hand_is_true:
            image = self.chopstick.check_chopstick(image, self.hand.landmark_MIDDLE_FINGER_TIP)

        # 우선은 hand와 같이두지않음
        # image = self.chopstick.check_chopstick(image, self.hand.landmark_MIDDLE_FINGER_TIP)

        if not self.stars:
            self.stars.append(Star(self.speed, image_width, image_height))
        else:
            image = self.set_star_image(image)
            if self.stars[-1].elapsed_time(now) >= self.regen_time:
                self.stars.append(Star(self.speed, image_width, image_height))
            for i in range(len(self.stars)):
                if self.hand.hand_sign_id is not None and self.chopstick.boxes is not None:
                    if self.stars[i].check_inChopstick(self.chopstick.boxes) and (self.hand.hand_sign_id == 2):
                        self.score += 1
                        del self.stars[i]
                        print(self.score)
                        break

                # if self.stars[i].check_inChopstick(self.chopstick.boxes):
                #     self.score += 1
                #     del self.stars[i]
                #     print(self.score)
                #     break

                if self.stars[i].check_timeover():
                    del self.stars[i]
                    break

        image = self.draw_score(image)
        return image
        # cv2.imshow('Image', image)

    def __del__(self):
        self.camera.video.release()

    def set_star_image(self, image):
        for star in self.stars:
            # image = cv2.circle(image, star.get_coord(), radius=10, color=(255, 255, 255), thickness=10)
            image = cvzone.overlayPNG(image, self.starImage, [star.get_X() - (int)(self.starSize / 2),
                                                              star.get_Y() - (int)(self.starSize / 2)])
        return image

    def draw_score(self, image):

        cv2.putText(image, "YOUR SCORE: " + str(self.score), (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                    cv2.LINE_AA)
        return image

    def get_score(self):
        return self.score

    def get_mode(self):
        return self.mode

    def get_user(self):
        return self.user


def gen(game):
    playtime = 60

    start = time.time()
    now = start
    overtime = (int)(now - start)

    game_mode = game.get_mode()
    game_mode_image = cv2.imread("mysite/game/game_class/image/" + game_mode + ".png")

    while overtime <= playtime:
        game_mode_image_copy = copy.deepcopy(game_mode_image)
        game_mode_image_copy = cv2.putText(img=game_mode_image_copy, text=(str)(game.get_score()), org=(125, 650),
                                           fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 255, 255),
                                           thickness=2)

        game_mode_image_copy = cv2.putText(img=game_mode_image_copy, text=(str)(60 - overtime), org=(115, 550),
                                           fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=2)

        image_hconcat = cv2.hconcat([game.get_frame(now), game_mode_image_copy])
        ret, jpeg = cv2.imencode('.jpg', image_hconcat)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        now = time.time()
        overtime = (int)(now - start)

    # gameOver
    ret, image = cv2.imencode('.jpg', cv2.imread("mysite/game/game_class/image/gameover_ingame.png"))
    frame = image.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # ranking 등록
    Ranking.objects.create(NAME=game.get_user(), SCORE=game.get_score(), MODE =game.get_mode())
    print("ranking 등록 완료")

    user_game_count = UserGameRecord.objects.get(NAME=game.user)
    user_game_count.COUNT += 1
    user_game_count.save()
    print("count 업데이트 완료")

