from abc import ABC, abstractmethod
from enums import PieceType, Color

class Piece(ABC):
    def __init__(self, piece_type: PieceType, color: Color, row: int, col: int) -> None:
        self.piece_type = piece_type
        self.color = color
        self.row = row
        self.col = col

    @abstractmethod
    def can_move(self, dest_x: int, dest_y: int) -> int:
        pass

    
    def get_type(self) -> PieceType:
        return self.piece_type
    
    def get_color(self):
        return self.color
    
    def get_x(self):
        return self.row
    
    def get_y(self):
        return self.col
    

    

    
    