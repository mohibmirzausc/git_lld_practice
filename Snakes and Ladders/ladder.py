from boardentity import BoardEntity

class Ladder(BoardEntity):
    def __init__(self, start, end):
        super().__init__(start, end)
        if start >= end:
            raise ValueError("Start of ladder must be less than it's end!")