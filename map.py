from mappiece import MapPiece
from movedirection import MoveDirection


class Map:
    def __init__(self, number_rows, number_columns, pieces: list[MapPiece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.pieces = pieces


    def generate_rules(self):
        return []


    def execute_move(self, direction: MoveDirection):
        for piece in self.pieces:
            piece.execute_move(direction=direction)
