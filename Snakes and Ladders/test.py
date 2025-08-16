import unittest
from dice import Dice

from snake import Snake
from ladder import Ladder
from board import Board
from game import Game

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("Setting up tests")

    def test_dice(self):
        dice = Dice(1,6)

        for i in range(100):
            x = dice.roll()
            self.assertTrue(1 <= x <= 6)

    def test_board(self):
        self.assertRaises(ValueError, Snake, 1, 3)
        self.assertRaises(ValueError, Ladder, 5, 2)

        snake = Snake(3, 1)
        ladder = Ladder(1, 5)

        board = Board(5, [snake, ladder])

        self.assertEqual(board.getSize(), 5)
        self.assertEqual(board.snakes_and_ladders[3], 1)
        self.assertEqual(board.snakes_and_ladders[1], 5)

        dice = Dice(1,6)

        builder = Game.Builder()

        builder.set_board(board)
        builder.set_dice(dice)

        

        

    





unittest.main(verbosity=2)