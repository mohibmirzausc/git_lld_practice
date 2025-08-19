import math

class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_distance_to(self, other_loc: 'Location') -> float:
        x_diff = other_loc._x - self.x
        y_diff = other_loc._y - self.y

        return math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2))

