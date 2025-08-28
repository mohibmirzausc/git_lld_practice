from enum import Enum

class PieceType(Enum):
    PAWN ="Pawn"
    ROOK = "Rook"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    QUEEN ="Queen"
    KING = "King"

class Color(Enum):
    BLACK = "Black"
    WHITE = "White"