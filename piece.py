from piecetype import PieceType

class Piece:
    def __init__(self, x, y, piece_type: PieceType):
        self.x = x
        self.y = y
        self.piece_type = piece_type
