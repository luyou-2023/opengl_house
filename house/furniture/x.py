from OpenGL.GL import *
from .base_furniture import BaseFurniture


def draw_cube():
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
        (1, 2, 3),
        # back face
        (4, 5, 6),
        (5, 6, 7),
        # left
        (4, 0, 6),
        (6, 0, 2),
        # right
        (5, 1, 7),
        (7, 1, 3),
        # up
        (2, 3, 6),
        (6, 3, 7),
        # down
        (0, 1, 4),
        (4, 1, 5)
    )

    glBegin(GL_TRIANGLES)
    colors = [
        (0.369, 0.592, 0.196),
        (0.369, 0.592, 0.196),
        (0.722, 0.886, 0.592),
        (0.722, 0.886, 0.592),
        (0.824, 0.549, 0.686),
        (0.824, 0.549, 0.686),
        (0.953, 0.867, 0.91),
        (0.953, 0.867, 0.91),
        (1, 0.827, 0.667),
        (1, 0.827, 0.667),
        (1, 0.953, 0.91),
        (1, 0.953, 0.91),
    ]

    i = 0
    mod = len(colors) - 1
    for edge in edges:
        glColor3fv(colors[i % mod])
        i = i + 1
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()


def draw_rectangular_prism(rotate, translate=(0, -.5, 0)):
    # push whatever it exists
    glPushMatrix()

    glRotate(rotate, 0, 0, 1)
    glScalef(1, 4, 1)
    glTranslatef(*translate)
    draw_cube()
    glPushMatrix()

    glPopMatrix()
    glPopMatrix()


def draw_x():
    draw_rectangular_prism(45)
    draw_rectangular_prism(315, (-.5, -.38, 0))


class X(BaseFurniture):
    def draw_on_scene(self):
        glTranslatef(0, .4100000000000002, 0)
        draw_x()
