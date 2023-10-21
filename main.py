import levelparser as LevelParser
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
    # TODO: Make a level editor to save to json format
    window = Window(
        x=WINDOW_X,
        y=WINDOW_Y,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
    )
    # TODO: Make a level selector
    level = LevelParser.get_level_by_name(level_name="test", window=window)
    level.start_main_loop()
