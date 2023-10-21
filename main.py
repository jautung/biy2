import os
import pick

import levelparser as LevelParser
from window import Window


ASSETS_DIRECTORY = "assets"
LEVELS_DIRECTORY = "levels"

PICK_INDICATOR = '=>'

WINDOW_X = 0
WINDOW_Y = 0
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


if __name__ == '__main__':
    # TODO: Add a linter
    # TODO: Make a level editor to save to json format
    window = Window(
        x=WINDOW_X,
        y=WINDOW_Y,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
    )
    level_names = [level_filename[:-len(".json")] for level_filename in os.listdir(LEVELS_DIRECTORY) if level_filename.endswith(".json")]
    _, level_selected_index = pick.pick(options=level_names, title="Choose level!", indicator=PICK_INDICATOR)
    level = LevelParser.get_level_by_name(
        level_name=level_names[level_selected_index],
        window=window,
        levels_directory=LEVELS_DIRECTORY,
        assets_directory=ASSETS_DIRECTORY
    )
    level.start_main_loop()
