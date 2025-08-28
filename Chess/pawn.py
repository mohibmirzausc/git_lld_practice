from piece import Piece
from enums import Color, PieceType

class Pawn(Piece):
    def __init__(self, color: Color, row: int, col: int):
        super().__init__(PieceType.PAWN, color, row, col)
        self.has_moved = False
    
    
