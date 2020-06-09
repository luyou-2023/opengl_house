from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from .base_furniture import BaseFurniture

from ..scene import TextureLoader

default_color = (0.318, 0.271, 0.224)

ctrlpoints = [
    [
        [-1.5, .9, 0.], [0., 1., 0.], [1.5, .9, 0.]
    ],
    [
        [-1.5, .9, 0.], [0., 0.9, -.7], [1.5, .9, 0.]
    ],
    [
        [-1.5, .9, 0.], [0., 0.75, -.7], [1.5, .9, 0.]
    ],
    [
        [-1.5, -.9, 0.], [0., -0.75, -.7], [1.5, -.9, 0.]
    ],
    [
        [-1.5, -.9, 0.], [0., -0.9, -.7], [1.5, -.9, 0.]
    ],
    [
        [-1.5, -.9, 0.], [0., -1., 0.], [1.5, -.9, 0.]
    ]
]
ctrlpoints = 2 * np.array(ctrlpoints)

verticies = (
    (-3, -2., 0),
    (3, -2., 0),
    (3, 2., 0),
    (-3, 2., 0)
)

verticies_frame = (
    (3, 1.8, -0.1),  # 0
    (3.2, 2, -0.1),  # 1
    (-3.2, 2, -0.1),  # 2
    (-3, 1.8, -0.1),  # 3

    (3, 1.8, 0.1),  # 4
    (3.2, 2, 0.1),  # 5
    (-3, 1.8, 0.1),  # 6
    (-3.2, 2, 0.1)  # 7
)

verticies_base = (
    (2, -2.2, -0.8),  # 0
    (2, -2, -0.8),  # 1
    (-2, -2, -0.8),  # 2
    (-2, -2.2, -0.8),  # 3

    (2, -2.2, 0.8),  # 4
    (2, -2, 0.8),  # 5
    (-2, -2.2, 0.8),  # 6
    (-2, -2, 0.8)  # 7
)

verticies_base_h = (
    (0.5, -2, -0.1),  # 0
    (0.5, -1, -0.1),  # 1
    (-0.5, -1, -0.1),  # 2
    (-0.5, -2, -0.1),  # 3

    (0.5, -2, 0.1),  # 4
    (0.5, -1, 0.1),  # 5
    (-0.5, -2, 0.1),  # 6
    (-0.5, -1, 0.1)  # 7
)

faces = (
    # Z negativo = (0, 1, 2, 3)
    (0, 1, 2, 3),
    # Z positivo = (4, 5, 6, 7)
    (4, 5, 7, 6),
    # Y negativo = (0, 3, 4, 6)
    (0, 3, 6, 4),
    # Y positivo = (1, 2, 5, 7)
    (1, 2, 7, 5),
    # X negativo = (2, 3, 6, 7)
    (2, 3, 6, 7),
    # X positivo = (0, 1, 4, 5)
    (0, 1, 5, 4)
)


def draw_base():
    glPushMatrix()
    glTranslatef(0., 0.5, 0.)
    draw_frame(verticies_base)
    draw_frame(verticies_base_h)
    glPopMatrix()


def draw_frames():
    glPushMatrix()
    draw_frame(verticies_frame)
    glPopMatrix()
    glPushMatrix()
    glRotatef(90, 0., 0., 1.)
    glTranslatef(0., 1.2, 0.)
    glScalef(0.625, 1., 1.)
    draw_frame(verticies_frame)
    glPopMatrix()
    glPushMatrix()
    glRotatef(-90, 0., 0., 1.)
    glTranslatef(0., 1.2, 0.)
    glScalef(0.625, 1., 1.)
    draw_frame(verticies_frame)
    glPopMatrix()
    glPushMatrix()
    glRotatef(180, 0., 0., 1.)
    draw_frame(verticies_frame)
    glPopMatrix()


def draw_screen(screen_texture):
    glBindTexture(GL_TEXTURE_2D, screen_texture)

    glBegin(GL_QUADS)
    texIndexes = [(1, 0), (1, 1), (0, 1), (0, 0)]
    for vertex, tex in zip(verticies, texIndexes):
        glVertex3fv(vertex)
        glTexCoord2fv(tex)
    glEnd()


def draw_frame(v):
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(v[vertex])
    glEnd()


def draw_back():
    glClearColor(1.0, 7.0, 7.0, 0.0)
    glMap2f(GL_MAP2_VERTEX_3, 0, 1, 0, 1, ctrlpoints)
    glEnable(GL_MAP2_VERTEX_3)
    glMapGrid2f(20, 0.0, 1.0, 20, 0.0, 1.0)

    glEvalMesh2(GL_FILL, 0, 20, 0, 20)
    for j in range(8):
        glBegin(GL_LINE_STRIP)
        for i in range(30):
            glEvalCoord2f(i / 30.0, j / 8.0)
        glEnd()
        glBegin(GL_LINE_STRIP)
        for i in range(30):
            glEvalCoord2f(j / 8.0, i / 30.0)
        glEnd()


class Tv(BaseFurniture):
    translate = [14, -0.5, -8]
    # translate = [0, -0.5, -8]
    scale = (0.7, 0.7, 0.7)

    def __init__(self, texture_loader: TextureLoader):
        super().__init__(texture_loader)

        self.texture = texture_loader.load_texture('tv.jpg')

    def draw_on_scene(self):
        glScalef(*self.scale)
        glRotatef(90, 0., 1., 0.)
        glTranslate(*self.translate)
        glColor4f(0.1, 0.1, 0.1, 0.5)

        draw_back()
        draw_frames()

        glPushMatrix()
        glRotatef(180, 0., .0, 1.)
        glRotatef(90, 1., .0, .0)
        draw_base()
        glPopMatrix()

        draw_screen(self.texture)
