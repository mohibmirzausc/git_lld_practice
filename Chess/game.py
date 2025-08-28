from board import Board


class Game:

    def __init__(self):
        self.board = Board()
    
    def __str__(self):
        return str(self.board)