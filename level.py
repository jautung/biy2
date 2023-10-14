from PIL import Image

import glhelper as GLHelper
from map import Map
from window import Window


# Colors in RGB
COLOR_WHITE = (1.0, 1.0, 1.0)
COLOR_GRAY = (0.4, 0.4, 0.4)


class Level:
    def __init__(self, title: str, window: Window, map: Map):
        self.window = window
        self.map = map
        self._temp_x = 0.0
        self._temp_y = 0.0
        self.glut_window = GLHelper.init_glut_window(window=window, title=title)
        # TODO: Compute size of cells based on grid in map
        self._cell_size = 110
        self._init_assets_as_textures()


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
        # TODO: Use map number of rows and columns correctly
        GLHelper.draw_line(color=COLOR_GRAY, x0=self.window.width/5, y0=3*self.window.height/5, x1=self.window.width, y1=3*self.window.height/5)
        GLHelper.draw_line(color=COLOR_GRAY, x0=self.window.width/5, y0=4*self.window.height/5, x1=self.window.width, y1=4*self.window.height/5)
        GLHelper.draw_line(color=COLOR_GRAY, x0=self.window.width/5, y0=2*self.window.height/5, x1=self.window.width, y1=2*self.window.height/5)
        GLHelper.draw_line(color=COLOR_GRAY, x0=3*self.window.width/5, y0=self.window.height/5, x1=3*self.window.width/5, y1=self.window.height)
        GLHelper.draw_line(color=COLOR_GRAY, x0=4*self.window.width/5, y0=self.window.height/5, x1=4*self.window.width/5, y1=self.window.height)
        GLHelper.draw_line(color=COLOR_GRAY, x0=2*self.window.width/5, y0=self.window.height/5, x1=2*self.window.width/5, y1=self.window.height)


    def _draw_map(self):
        # TODO: Display map and pieces!
        # TODO: We need an asset for each piece and an asset-name to piece mapping!
        GLHelper.draw_square_asset(
            texture_id=self.texture_map["test.png"],
            x0=self._temp_x*1000,
            y0=self._temp_y*1000,
            size=self._cell_size
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

