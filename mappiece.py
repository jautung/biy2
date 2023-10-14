from piecetype import PieceType
from movedirection import MoveDirection


class MapPiece:
    def __init__(self, x, y, piece_type: PieceType):
        self.x = x
        self.y = y
        self.piece_type = piece_type


    def execute_move(self, direction: MoveDirection):
        if direction == MoveDirection.UP:
            self.y += 1
        elif direction == MoveDirection.DOWN:
            self.y -= 1
        elif direction == MoveDirection.LEFT:
            self.x -= 1
        elif direction == MoveDirection.RIGHT:
            self.x += 1
        elif direction == MoveDirection.WAIT:
            pass