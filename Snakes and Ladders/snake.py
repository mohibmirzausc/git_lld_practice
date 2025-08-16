from boardentity import BoardEntity

class Snake(BoardEntity):
    def __init__(self, start, end):
        super().__init__(start, end)
        if start <= end:
            raise ValueError("Snake head must be higher than it's tail!")