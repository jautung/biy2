import copy
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


RGB_COLOR_WHITE = (1.0, 1.0, 1.0)
RGB_COLOR_GRAY = (0.4, 0.4, 0.4)
ALPHA_ASSET = 0.6


class Level:
    def __init__(self, title: str, window: Window, map: Map, assets_directory: str):
        self.window = window
        self.map = map
        self.cell_size = LevelHelper.calculate_cell_size(window=window, map=map)
        self.asset_size = LevelHelper.calculate_asset_size(cell_size=self.cell_size)
        (
            self.window_padding_horizontal,
            self.window_padding_vertical,
        ) = LevelHelper.calculate_window_paddings(
            window=window, map=map, cell_size=self.cell_size
        )
        self.glut_window = GLHelper.init_glut_window(window=window, title=title)
        self._init_assets_as_textures(assets_directory=assets_directory)
        self.original_map = copy.deepcopy(map)
        self.undo_map_stack: list[Map] = []

    def _init_assets_as_textures(self, assets_directory: str):
        self.asset_map: dict[str, Asset] = dict()
        for asset_filename in os.listdir(assets_directory):
            if not asset_filename.endswith(".png"):
                continue
            image = (
                Image.open(os.path.join(assets_directory, asset_filename))
                .convert("RGBA")
                .transpose(Image.FLIP_TOP_BOTTOM)
            )
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
                color=RGB_COLOR_WHITE
                if row_index == 0 or row_index == self.map.number_rows
                else RGB_COLOR_GRAY,
                x0=self.window_padding_horizontal,
                y0=self.window_padding_vertical + row_index * self.cell_size,
                x1=self.window.width - self.window_padding_horizontal,
                y1=self.window_padding_vertical + row_index * self.cell_size,
            )
        for column_index in range(self.map.number_columns + 1):
            GLHelper.draw_line(
                color=RGB_COLOR_WHITE
                if column_index == 0 or column_index == self.map.number_columns
                else RGB_COLOR_GRAY,
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
            asset=self.asset_map[map_piece.get_asset_name()],
            x0=x,
            y0=y,
            size=self.asset_size,
            alpha=ALPHA_ASSET,
        )

    def _keyboard_func(self, key, x, y):
        if key == b"w":
            self._execute_move(direction=MoveDirection.UP)
        elif key == b"a":
            self._execute_move(direction=MoveDirection.LEFT)
        elif key == b"s":
            self._execute_move(direction=MoveDirection.DOWN)
        elif key == b"d":
            self._execute_move(direction=MoveDirection.RIGHT)
        elif key == b" ":
            self._execute_move(direction=MoveDirection.WAIT)
        elif key == b"z" or key == b"u":
            self._undo()
        elif key == b"r":
            self._reset_level()
        elif key == b"q":
            GLHelper.destroy_glut_window(glut_window=self.glut_window)
        elif key == b"/":
            self.map.print_rules()
        elif key == b".":
            self.map.print_simplified_rules()

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
        self.undo_map_stack.append(copy.deepcopy(self.map))
        self.map.execute_move(direction=direction)
        if self.map.is_in_win_state():
            print("WIN!")
            GLHelper.destroy_glut_window(glut_window=self.glut_window)

    def _undo(self):
        if len(self.undo_map_stack) == 0:  # Nothing to undo
            return
        self.map = self.undo_map_stack.pop()

    def _reset_level(self):
        self.map = copy.deepcopy(self.original_map)
        self.undo_map_stack = []
