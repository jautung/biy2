from enum import Enum, auto
from mappiece import MapPiece


class MoveDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    WAIT = auto()


class Map:
    def __init__(self, number_rows, number_columns, pieces: list[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.pieces = pieces


    def execute_move(self, direction: MoveDirection):
        print(direction)
