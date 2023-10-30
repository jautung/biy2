from movedirection import MoveDirection
from piecetype import *
from pieceposition import PiecePosition


class MapPiece:
    def __init__(
        self,
        position: PiecePosition,
        piece_type: PieceType,
        direction: MoveDirection,
    ):
        self.position = position
        self.piece_type = piece_type
        self.direction = direction

    def __repr__(self) -> str:
        return f"{self.piece_type}@{self.position}"

    def get_asset_name(self) -> str:
        return self.piece_type.asset_set.get_asset_name(direction=self.direction)
