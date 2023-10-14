import os
from PIL import Image

import glhelper as GLHelper
import levelhelper as LevelHelper
from asset import Asset
from map import Map
from piece import Piece
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

        self._temp_x = 0
        self._temp_y = 0


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
            keyboard_func=self._keyboard_func
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
        for piece in self.map.pieces:
            self._draw_piece(piece=piece)


    def _draw_piece(self, piece: Piece):
        x, y = LevelHelper.calculate_asset_position(
            row_index=piece.x,
            column_index=piece.y,
            cell_size=self.cell_size,
            asset_size=self.asset_size,
            window_padding_horizontal=self.window_padding_horizontal,
            window_padding_vertical=self.window_padding_vertical,
        )
        GLHelper.draw_square_asset(
            asset=self.asset_map[piece.piece_type.asset_name],
            x0=x,
            y0=y,
            size=self.asset_size
        )


    def _keyboard_func(self, key, x, y):
        # TODO: Actually implement logic
        if key == b'w':
            self._temp_y += 1
        elif key == b'a':
            self._temp_x -= 1
        elif key == b's':
            self._temp_y -= 1
        elif key == b'd':
            self._temp_x += 1
        elif key == b'q':
            GLHelper.destroy_glut_window(self.glut_window)

