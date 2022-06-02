import random


class RandomCoordinate:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x = random.randrange(100, int(width - 1)-500)
        self.y = random.randrange(100, int(height - 1)-100)

    def get_coord(self):
        return self.x, self.y
