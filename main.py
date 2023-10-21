from level import Level
from map import Map
from mappiece import MapPiece
from pieceposition import PiecePosition
from piecetype import *
from window import Window


WINDOW_X = 0
WINDOW_Y = 0
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


if __name__ == '__main__':
    # TODO: Encode this in some json format and write a parser to read from file
    # TODO: Make a level editor to save to json format
    level=Level(
        title="My Level",
        window=Window(
            x=WINDOW_X,
            y=WINDOW_Y,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        ),
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
    level.start_main_loop()
