from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from window import Window
from map import Map


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
        self._display_reset()
        self._display_grid()
        self._display_map()
        self._display_flush()
        glutSwapBuffers()


    def _display_reset(self):
        glClear(GL_COLOR_BUFFER_BIT)


    def _display_grid(self):
        # TODO
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(0.0, 0.0)
        glVertex2f(1.0, 1.0)
        glEnd()


    def _display_map(self):
        # TODO
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_POINTS)
        glVertex2f(self._temp_x, self._temp_y)
        glEnd()


    def _display_flush(self):
        glFlush()


    def _keyboard_func(self, key, x, y):
        # TODO
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
