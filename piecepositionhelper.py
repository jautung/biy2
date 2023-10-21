from movedirection import MoveDirection
from pieceposition import PiecePosition


def get_position_after_move(position: PiecePosition, direction: MoveDirection) -> PiecePosition:
    if direction == MoveDirection.UP:
        return PiecePosition(
            x=position.x,
            y=position.y + 1,
        )
    elif direction == MoveDirection.DOWN:
        return PiecePosition(
            x=position.x,
            y=position.y - 1,
        )
    elif direction == MoveDirection.LEFT:
        return PiecePosition(
            x=position.x - 1,
            y=position.y,
        )
    elif direction == MoveDirection.RIGHT:
        return PiecePosition(
            x=position.x + 1,
            y=position.y,
        )
    elif direction == MoveDirection.WAIT:
        return PiecePosition(
            x=position.x,
            y=position.y,
        )
