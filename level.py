from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
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


    def _init_gl(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGB)
        glutInitWindowPosition(self.window.position_x, self.window.position_y)
        glutInitWindowSize(self.window.width, self.window.height)
        self.glut_window = glutCreateWindow(self.title)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)


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
        glClear(GL_COLOR_BUFFER_BIT)


    def _display_grid(self):
        # TODO: Use map number of rows and columns correctly
        self._gl_display_line(color=COLOR_GRAY, x0=-1, y0=0, x1=1, y1=0)
        self._gl_display_line(color=COLOR_GRAY, x0=-1, y0=0.5, x1=1, y1=0.5)
        self._gl_display_line(color=COLOR_GRAY, x0=-1, y0=-0.5, x1=1, y1=-0.5)
        self._gl_display_line(color=COLOR_GRAY, x0=0, y0=-1, x1=0, y1=1)
        self._gl_display_line(color=COLOR_GRAY, x0=0.5, y0=-1, x1=0.5, y1=1)
        self._gl_display_line(color=COLOR_GRAY, x0=-0.5, y0=-1, x1=-0.5, y1=1)


    def _display_map(self):
        # TODO: Display map and pieces!
        self._gl_display_point(color=COLOR_WHITE, size=30, x=self._temp_x, y=self._temp_y)


    def _gl_display_commit(self):
        glFlush()
        glutSwapBuffers()


    def _gl_display_point(self, color, size, x, y):
        glColor3f(*color)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()


    def _gl_display_line(self, color, x0, y0, x1, y1):
        glColor3f(*color)
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
