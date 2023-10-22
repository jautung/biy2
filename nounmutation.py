from piecetype import *


class NounMutation:
    def __init__(
        self,
        from_object_piece_type: ObjectPieceType,
        to_object_piece_type: ObjectPieceType,
    ):
        self.from_object_piece_type = from_object_piece_type
        self.to_object_piece_type = to_object_piece_type
