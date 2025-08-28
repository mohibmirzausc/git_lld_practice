from piece import Piece
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from enums import Color, PieceType
from game import Game
import unittest

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("Setting up tests")

    def test_piece(self):
        print("Testing base Piece")
        piece = Piece(PieceType.PAWN, Color.BLACK, 1, 1)

        self.assertEqual(piece.get_color(), Color.BLACK)
        self.assertEqual(piece.get_type(), PieceType.PAWN)

    def test_king(self):
        king = King(Color.BLACK, 3, 3)
        self.assertEqual(king.get_color(), Color.BLACK)
        self.assertEqual(king.get_type(), PieceType.KING)

    def test_queen(self):
        queen = Queen(Color.WHITE, 5, 3)
        self.assertEqual(queen.get_color(), Color.WHITE)
        self.assertEqual(queen.get_type(), PieceType.QUEEN)

    def test_rook(self):
        rook = Rook(Color.BLACK, 7, 4)
        self.assertEqual(rook.get_color(), Color.BLACK)
        self.assertEqual(rook.get_type(), PieceType.ROOK)

    def test_bishop(self):
        bishop = Bishop(Color.WHITE, 4, 2)
        self.assertEqual(bishop.get_color(), Color.WHITE)
        self.assertEqual(bishop.get_type(), PieceType.BISHOP)

    def test_knight(self):
        knight = Knight(Color.BLACK, 1, 1)
        self.assertEqual(knight.get_color(), Color.BLACK)
        self.assertEqual(knight.get_type(), PieceType.KNIGHT)

    def test_pawn(self):
        pawn = Pawn(Color.WHITE, 1, 5)
        self.assertEqual(pawn.get_color(), Color.WHITE)
        self.assertEqual(pawn.get_type(), PieceType.PAWN)

    def test_game(self):
        game = Game()
        print(game)

    

    def tearDown(self):
        print("Tearing down tests")

if __name__ == "__main__":
    unittest.main(verbosity=2)
