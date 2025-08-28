from piece import Piece
from enums import Color, PieceType

class Bishop(Piece):
    def __init__(self, color: Color, row: int, col: int):
        super().__init__(PieceType.BISHOP, color, row, col)
    

