from OpenGL.GL import * # TODO: Delete
from OpenGL.GLU import * # TODO: Delete
from OpenGL.GLUT import * # TODO: Delete
from PIL import Image

import glhelper as GLHelper
from map import Map
from window import Window


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
        self._display_grid()
        self._display_map()
        self._gl_display_commit()


    def _display_grid(self):
        # TODO: Use map number of rows and columns correctly
        glPushMatrix()
        self._gl_display_line(color=COLOR_GRAY, x0=self.window.width/5, y0=3*self.window.height/5, x1=self.window.width, y1=3*self.window.height/5)
        self._gl_display_line(color=COLOR_GRAY, x0=self.window.width/5, y0=4*self.window.height/5, x1=self.window.width, y1=4*self.window.height/5)
        self._gl_display_line(color=COLOR_GRAY, x0=self.window.width/5, y0=2*self.window.height/5, x1=self.window.width, y1=2*self.window.height/5)
        self._gl_display_line(color=COLOR_GRAY, x0=3*self.window.width/5, y0=self.window.height/5, x1=3*self.window.width/5, y1=self.window.height)
        self._gl_display_line(color=COLOR_GRAY, x0=4*self.window.width/5, y0=self.window.height/5, x1=4*self.window.width/5, y1=self.window.height)
        self._gl_display_line(color=COLOR_GRAY, x0=2*self.window.width/5, y0=self.window.height/5, x1=2*self.window.width/5, y1=self.window.height)
        glPopMatrix()


    def _display_map(self):
        # TODO: Display map and pieces!
        # TODO: We need an asset for each piece and an asset-name to piece mapping!
        self._gl_display_point(color=COLOR_WHITE, size=300, x=self._temp_x, y=self._temp_y)


    def _gl_display_commit(self):
        glFlush()
        glutSwapBuffers()


    def _gl_display_point(self, color, size, x, y):
        # TODO: This is a mess and not a point anymore
        # TODO: Let's make a 'run in XXX matrix mode' with function block a thing
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glScalef(0.01, 0.01, 1) # This is probably going from window 1200 / 800 into our sizes
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
        glBindTexture(GL_TEXTURE_2D, self.texture_map["test.png"])

        glPushMatrix()
        glTranslatef(
            x*1000,
            y*1000,
            0,
        )

        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(0, self._cell_size)
        glVertex2f(self._cell_size, self._cell_size)
        glVertex2f(self._cell_size, 0)
        glEnd()

        glPopMatrix()

        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glDisable(GL_TEXTURE_2D)


    def _gl_display_line(self, color, x0, y0, x1, y1):
        glColor3f(*color)
        # TODO: Let's make a 'run in XXX begin/end' with function block a thing, with optional color that defaults to white
        glBegin(GL_LINES)
        glVertex2f(x0, y0)
        glVertex2f(x1, y1)
        glEnd()


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
            self._exit()


    def _exit(self):
        glutDestroyWindow(self.glut_window)
        # Forceful exit is unfortunately needed since there is no way to leave the GLUT main loop otherwise
        # ([sys.exit()] or [raise SystemExit] both result in segmentation faults)
        # https://www.gamedev.net/forums/topic/376112-terminating-a-glut-loop-inside-a-program/3482380/
        # https://stackoverflow.com/a/35430500
        os._exit(0)
