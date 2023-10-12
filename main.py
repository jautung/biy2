from level import Level
from map import Map
from window import Window


WINDOW_POSITION_X = 0
WINDOW_POSITION_Y = 0
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


if __name__ == '__main__':
    level=Level(
        title="My Level",
        window=Window(
            position_x=WINDOW_POSITION_X,
            position_y=WINDOW_POSITION_Y,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        ),
        map=Map(
            number_rows=3,
            number_columns=3,
            pieces=[]
        )
    )
    level.start_main_loop()
