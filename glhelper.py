from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import os
import numpy

from asset import Asset
from window import Window


def init_glut_window(window: Window, title, enable_transparency=True):
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowPosition(window.x, window.y)
    glutInitWindowSize(window.width, window.height)
    glut_window = glutCreateWindow(title)
    if enable_transparency:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    return glut_window


def destroy_glut_window(glut_window):
    glutDestroyWindow(glut_window)
    # Forceful exit is unfortunately needed since there is no way to leave the GLUT main loop otherwise
    # ([sys.exit()] or [raise SystemExit] both result in segmentation faults)
    # https://www.gamedev.net/forums/topic/376112-terminating-a-glut-loop-inside-a-program/3482380/
    # https://stackoverflow.com/a/35430500
    os._exit(0)


def store_asset_as_texture(image: Image.Image):
    texture_id = glGenTextures(1)  # number of textures to alloc
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # TODO: Figure out why transparency isn't working to overlap pieces
    glTexImage2D(
        GL_TEXTURE_2D,  # target
        0,  # level
        GL_RGB,  # internalformat
        image.size[0],  # width
        image.size[1],  # height
        0,  # border
        GL_RGBA,  # format
        GL_UNSIGNED_BYTE,  # type
        numpy.array(image),  # pixels
    )
    return texture_id


def start_main_loop(display_func, keyboard_func, special_func):
    glutDisplayFunc(display_func)
    glutIdleFunc(display_func)
    glutKeyboardFunc(keyboard_func)
    glutSpecialFunc(special_func)
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
    glClear(GL_COLOR_BUFFER_BIT)
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
        window.x,  # x
        window.y,  # y
        window.width,  # width
        window.height,  # height
    )


def _reset_display_in_projection_mode(window: Window):
    glLoadIdentity()
    glOrtho(
        window.x,  # left
        window.x + window.width,  # right
        window.y,  # bottom
        window.y + window.height,  # top
        0.0,  # zNear
        1.0,  # zFar
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
            ),
        ),
    )


def _draw_line_inner(x0, y0, x1, y1):
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)


def draw_square_asset(asset: Asset, x0, y0, size):
    _run_block_in_matrix_mode(
        mode=GL_TEXTURE,
        block_func=lambda: _scale_texture(
            scale_x=1.0 / size,
            scale_y=1.0 / size,
        ),
    )
    _run_block_in_matrix_mode(
        mode=GL_MODELVIEW,
        block_func=lambda: _draw_texture(
            texture_id=asset.texture_id,
            x0=x0,
            y0=y0,
            size=size,
        ),
    )
    _run_block_in_matrix_mode(
        mode=GL_TEXTURE,
        block_func=lambda: _unscale_texture(),
    )


def _scale_texture(scale_x, scale_y):
    glPushMatrix()
    glScalef(
        scale_x,  # x
        scale_y,  # y
        1,  # z
    )


def _unscale_texture():
    glPopMatrix()


def _draw_texture(texture_id, x0, y0, size):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPushMatrix()
    glTranslatef(
        x0,  # x
        y0,  # y
        0,  # z
    )
    _draw_shape(
        shape=GL_QUADS,
        block_func=lambda: _draw_square_inner(size=size),
    )
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def _draw_square_inner(size):
    glVertex2f(0, 0)
    glVertex2f(0, size)
    glVertex2f(size, size)
    glVertex2f(size, 0)
