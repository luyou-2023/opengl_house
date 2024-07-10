from OpenGL.GL import *
from .base_furniture import BaseFurniture

default_color = (0.318, 0.271, 0.224)


def draw_cube(translate=None, scale=None, color=None):
    if color is None:
        color = default_color

    vertices = (
        (0, 0, 0),  # 0
        (1, 0, 0),  # 1
        (0, 1, 0),  # 2
        (1, 1, 0),  # 3

        (0, 0, -1),  # 4
        (1, 0, -1),  # 5
        (0, 1, -1),  # 6
        (1, 1, -1),  # 7
    )

    edges = (
        # front face
        (0, 1, 2),
        (1, 3, 2),
        # back face
        (4, 5, 6),
        (5, 7, 6),
        # left
        (4, 0, 6),
        (0, 2, 6),
        # right
        (1, 5, 7),
        (1, 7, 3),
        # up
        (2, 3, 6),
        (3, 7, 6),
        # down
        (0, 1, 4),
        (1, 5, 4)
    )

    normals = [
        (0, 0, 1),  # front face
        (0, 0, 1),  # front face
        (0, 0, -1),  # back face
        (0, 0, -1),  # back face
        (-1, 0, 0),  # left face
        (-1, 0, 0),  # left face
        (1, 0, 0),  # right face
        (1, 0, 0),  # right face
        (0, 1, 0),  # up face
        (0, 1, 0),  # up face
        (0, -1, 0),  # down face
        (0, -1, 0),  # down face
    ]

    glPushMatrix()

    if translate:
        glTranslatef(*translate)

    if scale:
        glScalef(*scale)

    glColor3f(*color)

    glBegin(GL_TRIANGLES)
    for (edge, normal) in zip(edges, normals):
        glNormal3d(*normal)
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()

    glPopMatrix()


def draw_front_down():
    # left foot
    draw_cube(translate=(-4, 0, 0), scale=(1.5, 3, .5))
    # middle
    draw_cube(translate=(-2.5, 1.5, -.2), scale=(6.5, 1.5, .3))
    # right foot
    draw_cube(translate=(4, 0, 0), scale=(1.5, 3, .5))


def draw_connection():
    # left
    draw_cube(translate=(-3.7, 1.8, -.5), scale=(.4, 1.2, 12))
    # right
    draw_cube(translate=(4.7, 1.8, -.5), scale=(.4, 1.2, 12))


def draw_back_down():
    dark_color = (0.145, 0.129, 0.125)
    # left foot
    draw_cube(translate=(-4, 0, -12.5), scale=(1.5, 8.5, .5))
    # # middle
    draw_cube(translate=(-2.5, 1.5, -12.7), scale=(2, 7, .3), color=dark_color)
    draw_cube(translate=(-.5, 1.5, -12.7), scale=(2.5, 6.6, .3), color=dark_color)
    draw_cube(translate=(2, 1.5, -12.7), scale=(2, 7, .3), color=dark_color)
    # right foot
    draw_cube(translate=(4, 0, -12.5), scale=(1.5, 8.5, .5))
    # full up
    draw_cube(translate=(-4, 8.5, -12.5), scale=(2, 1, .5))
    draw_cube(translate=(-2, 8.5, -12.5), scale=(.3, 1, .5), color=dark_color)  # dark space
    draw_cube(translate=(-1.7, 8.5, -12.5), scale=(.3, 1, .5))  # lighter space
    draw_cube(translate=(-1.4, 8.5, -12.5), scale=(.3, 1, .5), color=dark_color)  # dark space
    draw_cube(translate=(-1.1, 8.5, -12.5), scale=(3.7, 1, .5))  # middle lighter space
    draw_cube(translate=(2.6, 8.5, -12.5), scale=(.3, 1, .5), color=dark_color)  # dark space
    draw_cube(translate=(2.9, 8.5, -12.5), scale=(.3, 1, .5))  # lighter space
    draw_cube(translate=(3.2, 8.5, -12.5), scale=(.3, 1, .5), color=dark_color)  # dark space
    draw_cube(translate=(3.5, 8.5, -12.5), scale=(2, 1, .5))


def draw_mattress_base():
    draw_cube(translate=(-4, 3, 0), scale=(9.5, .35, 12.5))


class Bed(BaseFurniture):
    translate = [7, -4, -15]
    scale = (.7, .5, .7)
    rotate = (270, 0, 1, 0)

    def draw_on_scene(self):
        glTranslate(*self.translate)
        glScalef(*self.scale)
        glRotatef(*self.rotate)
        draw_front_down()
        draw_connection()
        draw_back_down()
        draw_mattress_base()
