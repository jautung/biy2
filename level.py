import os
from OpenGL.GLUT import GLUT_KEY_UP, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from PIL import Image

import glhelper as GLHelper
import levelhelper as LevelHelper
from asset import Asset
from map import Map
from movedirection import MoveDirection
from mappiece import MapPiece
from window import Window


# Colors in RGB
COLOR_WHITE = (1.0, 1.0, 1.0)
COLOR_GRAY = (0.4, 0.4, 0.4)


ASSET_DIRECTORY = "assets"


class Level:
    def __init__(self, title: str, window: Window, map: Map):
        self.window = window
        self.map = map
        self.cell_size = LevelHelper.calculate_cell_size(window=window, map=map)
        self.asset_size = LevelHelper.calculate_asset_size(cell_size=self.cell_size)
        self.window_padding_horizontal, self.window_padding_vertical = LevelHelper.calculate_window_paddings(window=window, map=map, cell_size=self.cell_size)
        self.glut_window = GLHelper.init_glut_window(window=window, title=title)
        self._init_assets_as_textures()


    def _init_assets_as_textures(self):
        self.asset_map = {}
        for asset_filename in os.listdir(ASSET_DIRECTORY):
            image = Image.open(os.path.join(ASSET_DIRECTORY, asset_filename)).convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
            self.asset_map[asset_filename] = Asset(
                texture_id=GLHelper.store_asset_as_texture(image=image),
                width=image.size[0],
                height=image.size[1],
            )


    def start_main_loop(self):
        GLHelper.start_main_loop(
            display_func=self._display_func,
            keyboard_func=self._keyboard_func,
            special_func=self._special_func,
        )


    def _display_func(self):
        GLHelper.reset_display(window=self.window)
        self._draw_grid()
        self._draw_map()
        GLHelper.commit_display()


    def _draw_grid(self):
        for row_index in range(self.map.number_rows + 1):
            GLHelper.draw_line(
                color=COLOR_WHITE if row_index == 0 or row_index == self.map.number_rows else COLOR_GRAY,
                x0=self.window_padding_horizontal,
                y0=self.window_padding_vertical + row_index * self.cell_size,
                x1=self.window.width - self.window_padding_horizontal,
                y1=self.window_padding_vertical + row_index * self.cell_size,
            )
        for column_index in range(self.map.number_columns + 1):
            GLHelper.draw_line(
                color=COLOR_WHITE if column_index == 0 or column_index == self.map.number_columns else COLOR_GRAY,
                x0=self.window_padding_horizontal + column_index * self.cell_size,
                y0=self.window_padding_vertical,
                x1=self.window_padding_horizontal + column_index * self.cell_size,
                y1=self.window.height - self.window_padding_vertical,
            )


    def _draw_map(self):
        for map_piece in self.map.map_pieces:
            self._draw_piece(map_piece=map_piece)


    def _draw_piece(self, map_piece: MapPiece):
        x, y = LevelHelper.calculate_asset_position(
            row_index=map_piece.position.y,
            column_index=map_piece.position.x,
            cell_size=self.cell_size,
            asset_size=self.asset_size,
            window_padding_horizontal=self.window_padding_horizontal,
            window_padding_vertical=self.window_padding_vertical,
        )
        GLHelper.draw_square_asset(
            asset=self.asset_map[map_piece.piece_type.asset_name],
            x0=x,
            y0=y,
            size=self.asset_size
        )


    def _keyboard_func(self, key, x, y):
        if key == b'w':
            self._execute_move(direction=MoveDirection.UP)
        elif key == b'a':
            self._execute_move(direction=MoveDirection.LEFT)
        elif key == b's':
            self._execute_move(direction=MoveDirection.DOWN)
        elif key == b'd':
            self._execute_move(direction=MoveDirection.RIGHT)
        elif key == b' ':
            self._execute_move(direction=MoveDirection.WAIT)
        elif key == b'q':
            GLHelper.destroy_glut_window(self.glut_window)
        elif key == b'/':
            # Printing rules for debugging
            rules = self.map._generate_rules()
            print("Rules:")
            for rule in rules:
                print(" ".join([text_piece_type._debug_repr() for text_piece_type in rule]))
            print()


    def _special_func(self, key, x, y):
        if key == GLUT_KEY_UP:
            self._execute_move(direction=MoveDirection.UP)
        elif key == GLUT_KEY_DOWN:
            self._execute_move(direction=MoveDirection.DOWN)
        elif key == GLUT_KEY_LEFT:
            self._execute_move(direction=MoveDirection.LEFT)
        elif key == GLUT_KEY_RIGHT:
            self._execute_move(direction=MoveDirection.RIGHT)


    def _execute_move(self, direction: MoveDirection):
        self.map.execute_move(direction=direction)
        if self.map.check_for_win():
            print("WIN!")
            GLHelper.destroy_glut_window(self.glut_window)
