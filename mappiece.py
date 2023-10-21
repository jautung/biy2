from piecetype import *


class MapPiece:
    def __init__(self, x, y, piece_type: PieceType):
        self.x = x
        self.y = y
        self.piece_type = piece_type


    def __repr__(self):
        return f"{self.piece_type}@({self.x}, {self.y})"
