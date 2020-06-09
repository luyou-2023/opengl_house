from OpenGL.GL import *
from .base_furniture import BaseFurniture
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

default_color = (1, 1, 1)


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


def draw_circle(translate=None, radius=None, slices=None, stacks=None, color=None):
    if color is None:
        color = default_color

    sphere = gluNewQuadric()
    glPushMatrix()
    glTranslatef(*translate)
    glColor3f(*color)  # Put color
    gluSphere(sphere, radius, slices, stacks)  # Draw sphere

    glPopMatrix()


def draw_box():
    draw_cube(translate=(0, 1, 0), scale=(7, 10, 0.2))  # Costas
    draw_cube(translate=(7, 1, 3.3), scale=(0.2, 10, 3.5))  # LD
    draw_cube(translate=(0, 1, 3.3), scale=(0.2, 10, 3.5))  # LE
    draw_cube(translate=(0, 1, 3.3), scale=(7, 0.2, 3.5))  # Piso
    draw_cube(translate=(0, 10.8, 3.3), scale=(7, 0.2, 3.5))  # Topo


def draw_divisions():
    draw_cube(translate=(0, 4.5, 3.3), scale=(7, 0.2, 3.5))  # Meio
    draw_cube(translate=(0, 8, 3.3), scale=(7, 0.2, 3.5))  # Meio
    draw_cube(translate=(3.5, 1.2, 3.3), scale=(0.5, 3.3, 0.2))  # divisoria


def draw_doors():
    draw_cube(translate=(0.06, 8.2, 3.5), scale=(7, 2.7, 0.2), color=(0.100, 0.500, 0.100))  # PortaCima
    draw_cube(translate=(0.06, 1.2, 3.5), scale=(3.5, 3.3, 0.2), color=(0.100, 0.500, 0.100))  # PortaBL
    draw_cube(translate=(3.6, 1.2, 3.5), scale=(3.5, 3.3, 0.2), color=(0.100, 0.500, 0.100))  # PortaBR


def draw_push():
    draw_circle(translate=(3, 2.8, 3.6), radius=0.2, slices=100, stacks=5)  # ME
    draw_circle(translate=(4.1, 2.8, 3.6), radius=0.2, slices=100, stacks=5)  # MD
    draw_cube(translate=(2.5, 8.3, 3.8), scale=(0.1, 0.1, 0.2))
    draw_cube(translate=(4.4, 8.3, 3.8), scale=(0.1, 0.1, 0.2))
    draw_cube(translate=(2.3, 8.3, 3.9), scale=(2.37, 0.2, 0.1))


def draw_footers():
    draw_cube(translate=(0, 0, 3.3), scale=(0.8, 1, 1))  # FE
    draw_cube(translate=(0, 0, 0.8), scale=(0.8, 1, 1))  # CE
    draw_cube(translate=(6.3, 0, 0.8), scale=(0.8, 1, 1))  # CD
    draw_cube(translate=(6.3, 0, 3.3), scale=(0.8, 1, 1))  # CD


class Armario(BaseFurniture):
    translate = [35, -8, -9]
    scale = (.5, .5, .5)
    rotate = (270, 0, 1, 0)

    def draw_on_scene(self):
        glScalef(*self.scale)
        glTranslatef(*self.translate)
        glRotatef(*self.rotate)
        draw_box()
        draw_divisions()
        draw_doors()
        draw_push()
        draw_footers()
