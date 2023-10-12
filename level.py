from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy

from window import Window
from map import Map


COLOR_WHITE = (1.0, 1.0, 1.0)
COLOR_GRAY = (0.4, 0.4, 0.4)


class Level:
    def __init__(self, title: str, window: Window, map: Map):
        self.title = title
        self.window = window
        self.map = map
        self._temp_x = 0.0
        self._temp_y = 0.0
        self._init_gl()
        self._init_assets_as_textures()
        # TODO: Compute size of cells based on grid in map
        self._cell_size = 110


    def _init_gl(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGB)
        glutInitWindowPosition(self.window.position_x, self.window.position_y)
        glutInitWindowSize(self.window.width, self.window.height)
        self.glut_window = glutCreateWindow(self.title)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)


    def _init_assets_as_textures(self):
        self.texture_map = {}
        # TODO: Handle opening all assets one by one
        for name in ["test.png"]:
            image = Image.open(f"assets/{name}").convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
            texture_id = glGenTextures(1)
            self.texture_map[name] = texture_id
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            # TODO: Probably store the actual width and height for use to calculate the scaling later
            print(image.size)
            glTexImage2D(
                GL_TEXTURE_2D, # target
                0, # level
                GL_RGB, # internal_format
                image.size[0], # width
                image.size[1], # height
                0, # border
                GL_RGB, # format
                GL_UNSIGNED_BYTE, # type
                numpy.array(list(image.getdata()), numpy.int8) # *pixels
            )


    def start_main_loop(self):
        glutDisplayFunc(self._display_func)
        glutIdleFunc(self._display_func)
        glutKeyboardFunc(self._keyboard_func)
        glutMainLoop()


    def _display_func(self):
        self._gl_display_reset()
        self._display_grid()
        self._display_map()
        self._gl_display_commit()


    def _gl_display_reset(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # TODO: Let's make a 'run in XXX matrix mode' with function block a thing
        glLoadIdentity()
        glViewport(
            self.window.position_x, # x
            self.window.position_y, # y
            self.window.width, # width
            self.window.height, # height
        )
        # TODO: Let's make a 'run in XXX matrix mode' with function block a thing
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            self.window.position_x, # left
            self.window.position_x + self.window.width, # right
            self.window.position_y, # bottom
            self.window.position_y + self.window.height, # top
            0.0, # zNear
            1.0, # zFar
        )
        # TODO: Let's make a 'run in XXX matrix mode' with function block a thing
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


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
