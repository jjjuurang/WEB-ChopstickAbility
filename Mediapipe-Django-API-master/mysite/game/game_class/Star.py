import time

from mysite.game.game_class.RandomCoordinate import RandomCoordinate


class Star:
    def __init__(self, vanishing_time, width, height):
        self.__x, self.__y = RandomCoordinate(width, height).get_coord()
        self.create_time = time.time()
        self.vanishing_time = vanishing_time

    def elapsed_time(self, now):
        return now - self.create_time

    def check_timeover(self):
        if time.time() - self.create_time >= self.vanishing_time:
            return True
        else:
            return False

    def get_coord(self):
        return (self.__x, self.__y)

    def check_inChopstick(self, boxes):
        """
        TODO
        chopstick의 좌표를 가져와 (chopstick class 내에 구현)
        해당 좌표 끝(젓가락) 근처 내에 별이 있는지 체크
        """

        for box in boxes:
            if self.__x in range(box[0], box[0]+box[2]) and self.__y in range(box[1], box[1]+box[3]) :
                return True
            else:
                return False






