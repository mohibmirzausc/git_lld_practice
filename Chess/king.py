from piece import Piece
from enums import Color, PieceType

class King(Piece):
    def __init__(self, color: Color, row: int, col: int):
        super().__init__(PieceType.KING, color, row, col)
        self.has_moved = False
    
    
