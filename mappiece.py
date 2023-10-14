from piecetype import PieceType
from movedirection import MoveDirection


class MapPiece:
    def __init__(self, x, y, piece_type: PieceType):
        self.x = x
        self.y = y
        self.piece_type = piece_type
