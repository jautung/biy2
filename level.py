from PIL import Image

import glhelper as GLHelper
import levelhelper as LevelHelper
from map import Map
from window import Window


# Colors in RGB
COLOR_WHITE = (1.0, 1.0, 1.0)
COLOR_GRAY = (0.4, 0.4, 0.4)


class Level:
    def __init__(self, title: str, window: Window, map: Map):
        self.window = window
        self.map = map
        self.cell_size = LevelHelper.calculate_cell_size(window=window, map=map)
        self.window_paddings = LevelHelper.calculate_window_paddings(window=window, map=map, cell_size=self.cell_size)
        self.glut_window = GLHelper.init_glut_window(window=window, title=title)
        self._init_assets_as_textures()

        self._temp_x = 0.0
        self._temp_y = 0.0


    def _init_assets_as_textures(self):
        self.texture_map = {}
        # TODO: Handle opening all assets one by one
        for name in ["test.png"]:
            image = Image.open(f"assets/{name}").convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
            self.texture_map[name] = GLHelper.store_asset_as_texture(image=image)


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
                x0=self.window_paddings[0],
                y0=self.window_paddings[1] + row_index * self.cell_size,
                x1=self.window.width - self.window_paddings[0],
                y1=self.window_paddings[1] + row_index * self.cell_size,
            )
        for column_index in range(self.map.number_columns + 1):
            GLHelper.draw_line(
                color=COLOR_WHITE if column_index == 0 or column_index == self.map.number_columns else COLOR_GRAY,
                x0=self.window_paddings[0] + column_index * self.cell_size,
                y0=self.window_paddings[1],
                x1=self.window_paddings[0] + column_index * self.cell_size,
                y1=self.window.height - self.window_paddings[1],
            )


    def _draw_map(self):
        # TODO: Display map and pieces!
        # TODO: We need an asset for each piece and an asset-name to piece mapping!
        GLHelper.draw_square_asset(
            texture_id=self.texture_map["test.png"],
            x0=self._temp_x*1000,
            y0=self._temp_y*1000,
            size=100
        )


    def _keyboard_func(self, key, x, y):
        # TODO: Actually implement logic
        if key == b'w':
            self._temp_y += 0.1
        elif key == b'a':
            self._temp_x -= 0.1
        elif key == b's':
            self._temp_y -= 0.1
        elif key == b'd':
            self._temp_x += 0.1
        elif key == b'q':
            GLHelper.destroy_glut_window(self.glut_window)

