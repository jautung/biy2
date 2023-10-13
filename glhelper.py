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


def run_block_in_matrix_mode(mode, block_func):
    glMatrixMode(mode)
    block_func()


def reset_display(window: Window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    run_block_in_matrix_mode(
        mode=GL_MODELVIEW,
        block_func=lambda: _clear_display_in_modelview_mode(window=window),
    )
    run_block_in_matrix_mode(
        mode=GL_PROJECTION,
        block_func=lambda: _clear_display_in_projection_mode(window=window),
    )
    run_block_in_matrix_mode(
        mode=GL_MODELVIEW,
        block_func=_reset_display_in_modelview_mode,
    )


def _clear_display_in_modelview_mode(window: Window):
    glLoadIdentity()
    glViewport(
        window.position_x, # x
        window.position_y, # y
        window.width, # width
        window.height, # height
    )


def _clear_display_in_projection_mode(window: Window):
    glLoadIdentity()
    glOrtho(
        window.position_x, # left
        window.position_x + window.width, # right
        window.position_y, # bottom
        window.position_y + window.height, # top
        0.0, # zNear
        1.0, # zFar
    )


def _reset_display_in_modelview_mode():
    glLoadIdentity()
