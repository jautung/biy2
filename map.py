from piece import Piece

class Map:
    def __init__(self, number_rows, number_columns, pieces: list[Piece]):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.pieces = pieces
