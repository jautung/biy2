from piecetype import *
from pieceposition import PiecePosition


class MapPiece:
    def __init__(self, position: PiecePosition, piece_type: PieceType):
        self.position = position
        self.piece_type = piece_type

    def __repr__(self) -> str:
        return f"{self.piece_type}@{self.position}"
