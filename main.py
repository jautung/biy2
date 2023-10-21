from level import Level
from map import Map
from mappiece import MapPiece
from piecetype import *
from window import Window


WINDOW_X = 0
WINDOW_Y = 0
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


if __name__ == '__main__':
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
                    x=0,
                    y=0,
                    piece_type=BabaTextPieceType()
                ),
                MapPiece(
                    x=1,
                    y=0,
                    piece_type=IsTextPieceType()
                ),
                MapPiece(
                    x=2,
                    y=0,
                    piece_type=YouTextPieceType()
                ),
                MapPiece(
                    x=0,
                    y=1,
                    piece_type=FlagTextPieceType()
                ),
                MapPiece(
                    x=1,
                    y=1,
                    piece_type=IsTextPieceType()
                ),
                MapPiece(
                    x=2,
                    y=1,
                    piece_type=WinTextPieceType()
                ),
                MapPiece(
                    x=0,
                    y=5,
                    piece_type=BabaObjectPieceType()
                ),
                MapPiece(
                    x=8,
                    y=5,
                    piece_type=FlagObjectPieceType()
                ),
            ]
        )
    )
    level.start_main_loop()
