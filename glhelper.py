from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy

from window import Window


def init_glut_window(window: Window, title):
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowPosition(window.position_x, window.position_y)
    glutInitWindowSize(window.width, window.height)
    glut_window = glutCreateWindow(title)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    return glut_window


def destroy_glut_window(glut_window):
    glutDestroyWindow(glut_window)
    # Forceful exit is unfortunately needed since there is no way to leave the GLUT main loop otherwise
    # ([sys.exit()] or [raise SystemExit] both result in segmentation faults)
    # https://www.gamedev.net/forums/topic/376112-terminating-a-glut-loop-inside-a-program/3482380/
    # https://stackoverflow.com/a/35430500
    os._exit(0)


def store_asset_as_texture(image: Image.Image):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # TODO: Probably store the actual width and height for use to calculate the scaling later
    glTexImage2D(
        GL_TEXTURE_2D, # target
        0, # level
        GL_RGB, # internal_format
        image.size[0], # width
        image.size[1], # height
        0, # border
        GL_RGB, # format
        GL_UNSIGNED_BYTE, # type
        numpy.array(list(image.getdata()), numpy.int8), # *pixels
    )
    return texture_id


def start_main_loop(display_func, keyboard_func):
    glutDisplayFunc(display_func)
    glutIdleFunc(display_func)
    glutKeyboardFunc(keyboard_func)
    glutMainLoop()


def commit_display():
    glFlush()
    glutSwapBuffers()


def _run_block_in_matrix_mode(mode, block_func):
    glMatrixMode(mode)
    block_func()


def _draw_shape(shape, block_func):
    glBegin(shape)
    block_func()
    glEnd()


def reset_display(window: Window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    _run_block_in_matrix_mode(
        mode=GL_MODELVIEW,
        block_func=lambda: _reset_display_in_modelview_mode(window=window),
    )
    _run_block_in_matrix_mode(
        mode=GL_PROJECTION,
        block_func=lambda: _reset_display_in_projection_mode(window=window),
    )


def _reset_display_in_modelview_mode(window: Window):
    glLoadIdentity()
    glViewport(
        window.position_x, # x
        window.position_y, # y
        window.width, # width
        window.height, # height
    )


def _reset_display_in_projection_mode(window: Window):
    glLoadIdentity()
    glOrtho(
        window.position_x, # left
        window.position_x + window.width, # right
        window.position_y, # bottom
        window.position_y + window.height, # top
        0.0, # zNear
        1.0, # zFar
    )


def draw_line(color, x0, y0, x1, y1):
    glColor3f(*color)
    _run_block_in_matrix_mode(
        mode=GL_MODELVIEW,
        block_func=lambda: _draw_shape(
            shape=GL_LINES,
            block_func=lambda: _draw_line_inner(
                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1,
            )
        ),
    )


def _draw_line_inner(x0, y0, x1, y1):
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)


def draw_square_asset(texture_id, x, y, size):
    _run_block_in_matrix_mode(
        mode=GL_TEXTURE,
        # This is probably going from window 1200 / 800 into our sizes
        block_func=lambda: _scale_texture(scale=0.01),
    )
    _run_block_in_matrix_mode(
        mode=GL_MODELVIEW,
        block_func=lambda: _draw_texture(
            texture_id=texture_id,
            x=x,
            y=y,
            size=size,
        ),
    )
    _run_block_in_matrix_mode(
        mode=GL_TEXTURE,
        block_func=lambda: _unscale_texture(),
    )


def _scale_texture(scale):
    glPushMatrix()
    glScalef(
        scale, # x
        scale, # y
        1, # z
    )


def _unscale_texture():
    glPopMatrix()


def _draw_texture(texture_id, x, y, size):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glPushMatrix()
    glTranslatef(
        x, # x
        y, # y
        0, # z
    )
    _draw_shape(
        shape=GL_QUADS,
        block_func=lambda: _draw_texture_inner(
            size=size, # TODO
        )
    )
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def _draw_texture_inner(size):
    glVertex2f(0, 0)
    glVertex2f(0, size)
    glVertex2f(size, size)
    glVertex2f(size, 0)
