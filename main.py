from level import Level
from map import Map
from piece import Piece
from piecetype import WordIsPieceType, BabaObjectPieceType, FlagObjectPieceType, BabaWordPieceType, FlagWordPieceType, WinWordPieceType, YouWordPieceType
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
            pieces=[
                Piece(
                    x=0,
                    y=0,
                    piece_type=BabaWordPieceType()
                ),
                Piece(
                    x=1,
                    y=0,
                    piece_type=WordIsPieceType()
                ),
                Piece(
                    x=2,
                    y=0,
                    piece_type=YouWordPieceType()
                ),
                Piece(
                    x=3,
                    y=0,
                    piece_type=BabaObjectPieceType()
                ),
                Piece(
                    x=4,
                    y=0,
                    piece_type=FlagObjectPieceType()
                ),
            ]
        )
    )
    level.start_main_loop()
