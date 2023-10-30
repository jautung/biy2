from movedirection import MoveDirection
from piecetype import *
from pieceposition import PiecePosition


class MapPiece:
    def __init__(
        self,
        position: PiecePosition,
        piece_type: PieceType,
        move_direction: MoveDirection,
    ):
        self.position = position
        self.piece_type = piece_type
        self.move_direction = move_direction

    def __repr__(self) -> str:
        return f"{self.piece_type}@{self.position}"

    def get_asset_name(self) -> str:
        # TODO: move_direction as input
        return self.piece_type.asset_set.get_asset_name(
            move_direction=MoveDirection.RIGHT
        )
