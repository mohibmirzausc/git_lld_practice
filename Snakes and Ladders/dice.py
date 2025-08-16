import random

class Dice:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def roll(self) -> int:
        return int(random.random() * (self.max_val - self.min_val + 1) + self.min_val)