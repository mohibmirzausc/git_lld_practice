from typing import List
from boardentity import BoardEntity
from board import Board
from player import Player
from dice import Dice

class Game:
    class Builder:
        def __init__(self) -> None:
            self.board = None
            self.players = None
            self.dice = None

        def set_board(self, board_size: int, board_entities: List[BoardEntity]):
            self.board = Board(board_size, board_entities)

        def set_players(self, players: List[Player]):
            self.players = players

        def set_dice(self, dice: Dice):
            self.dice = dice

        def build(self):
            if self.board is None or self.players is None or self.dice is None:
                raise ValueError("Board, Players, and Dice must all be set!")
            
            return Game(self)
        
    def __init__(self, builder: 'Game.Builder'):
        self.board = builder.board
        self.players = builder.players
        self.dice = builder.dice
