import random


class RandomCoordinate:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x = random.randrange(300, int(width)- 1-300)
        self.y = random.randrange(200, int(height) - 200)

    def get_coord(self):
        return self.x, self.y
