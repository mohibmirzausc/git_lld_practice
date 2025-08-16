from boardentity import BoardEntity
from typing import List

class Board:
    def __init__(self, size: int, entities: List[BoardEntity]):
        self.snakes_and_ladders = {}
        self.size = size

        for entity in entities:
            self.snakes_and_ladders[entity.getStart()] = entity.getEnd()

    def getSize(self):
        return self.size
    
    def get_final_position(self, pos):
        return self.snakes_and_ladders.get(pos, pos)
