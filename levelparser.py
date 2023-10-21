import os

from level import Level
from map import Map
from mappiece import MapPiece
from pieceposition import PiecePosition
from piecetype import *
from window import Window


LEVELS_DIRECTORY = "levels"


def get_level_by_name(level_name: str, window: Window) -> Level:
    filename = os.path.join(LEVELS_DIRECTORY, f"{level_name}.json")
    return Level(
        title="My Level",
        window=window,
        map=Map(
            number_rows=8,
            number_columns=10,
            map_pieces=[
                MapPiece(
                    position=PiecePosition(
                        x=0,
                        y=0,
                    ),
                    piece_type=BabaTextPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=1,
                        y=0,
                    ),
                    piece_type=IsTextPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=2,
                        y=0,
                    ),
                    piece_type=YouTextPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=0,
                        y=3,
                    ),
                    piece_type=FlagTextPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=0,
                        y=2,
                    ),
                    piece_type=IsTextPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=1,
                        y=1,
                    ),
                    piece_type=WinTextPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=0,
                        y=5,
                    ),
                    piece_type=BabaObjectPieceType(),
                ),
                MapPiece(
                    position=PiecePosition(
                        x=8,
                        y=5,
                    ),
                    piece_type=FlagObjectPieceType(),
                ),
            ]
        )
    )
