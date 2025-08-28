from piece import Piece
from enums import Color, PieceType

class Rook(Piece):
    def __init__(self, color: Color, col: int, row: int):
        super().__init__(PieceType.ROOK, color, col, row)
    

