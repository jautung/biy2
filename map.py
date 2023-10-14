from enum import Enum, auto
from piece import Piece


class MoveDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    WAIT = auto()


class Map:
    def __init__(self, number_rows, number_columns, pieces: list[Piece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.pieces = pieces


    def execute_move(self, direction: MoveDirection):
        print(direction)
