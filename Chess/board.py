from pawn import Pawn
from queen import Queen
from king import King
from bishop import Bishop
from knight import Knight
from rook import Rook
from enums import Color
from piece import Piece
from typing import Optional


class Board:
    def __init__(self):
        cols = 8
        rows = 8
        self.board: Optional[Piece] = [[None for _ in range(cols)] for _ in range(rows)]
        self._initialize_board()

    def _initialize_board(self):
        pawn_rows = [1, 6]
        for i in pawn_rows:
            for j in range(8):
                if i < 4:
                    self.board[i][j] = Pawn(Color.WHITE, i, j)
                else:
                    self.board[i][j] = Pawn(Color.BLACK, i, j)

        # Queens
        self.board[0][3] = Queen(Color.WHITE, 0, 3)
        self.board[7][3] = Queen(Color.BLACK, 7, 3)

        # Kings
        self.board[0][4] = King(Color.WHITE, 0, 4)
        self.board[7][4] = King(Color.BLACK, 7, 4)

        # Rooks
        self.board[0][0] = Rook(Color.WHITE, 0, 0)
        self.board[0][7] = Rook(Color.WHITE, 0, 7)
        self.board[7][0] = Rook(Color.BLACK, 7, 0)
        self.board[7][7] = Rook(Color.BLACK, 7, 7)

        # Knights
        self.board[0][1] = Knight(Color.WHITE, 0, 1)
        self.board[0][6] = Knight(Color.WHITE, 0, 6)
        self.board[7][1] = Knight(Color.BLACK, 7, 1)
        self.board[7][6] = Knight(Color.BLACK, 7, 6)

        # Bishops
        self.board[0][2] = Bishop(Color.WHITE, 0, 2)
        self.board[0][5] = Bishop(Color.WHITE, 0, 5)
        self.board[7][2] = Bishop(Color.BLACK, 7, 2)
        self.board[7][5] = Bishop(Color.BLACK, 7, 5)

    def can_move(self, piece: Piece, dest_x: int, dest_y: int):
        pass
    
    def __str__(self):
        if not self.board:
            return ""
        
        s = ""

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                s += "None" if not self.board[i][j] else self.board[i][j].get_type().value
                s += ","
            s += "\n"

        return s 