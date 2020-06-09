# Feito por Gabriel e Hudson

import numpy as np
import pygame
from pygame.locals import *
from copy import copy

from OpenGL.GL import *
from OpenGL.GLU import *
from .base_furniture import BaseFurniture

import math

from ..scene import TextureLoader

verticies = (
    (1, -1, -1),  # 0
    (1, 1, -1),  # 1
    (-1, 1, -1),  # 2
    (-1, -1, -1),  # 3

    (1, -1, 1),  # 4
    (1, 1, 1),  # 5
    (-1, -1, 1),  # 6
    (-1, 1, 1)  # 7
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

normals = (
    (0, 0, -1),
    (0, 0, 1),
    (0, -1, 0),
    (0, 1, 0),
    (-1, 0, 0),
    (1, 0, 0),
)

face1 = (4, 5, 7, 6)  # Z Positivo
normal1 = (0, 0, 1)  # Z Positivo

face2 = (0, 1, 2, 3)  # Z Negativo
normal2 = (0, 0, -1)  # Z Negativo

face3 = (1, 2, 7, 5)  # Y Positivo
normal3 = (0, 1, 0)  # Y Positivo

face4 = (0, 3, 6, 4)  # Y Negativo
normal4 = (0, -1, 0)  # Y Negativo

face5 = (0, 1, 5, 4)  # X Positivo
normal5 = (1, 0, 0)  # X Positivo

face6 = (2, 3, 6, 7)  # X Negativo
normal6 = (-1, 0, 0)  # X Negativo


# segments = np.array((
#     ((0, 0.3, 0),(0, 0, 0)),
#     ((0, 0, 0),(0, 0, 0)),
#     ((0, 0, 0),(0, 0, 0)),
# ))


def retornaNovaFace(face, normal, texture=None):
    if not texture is None:
        glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    texIndexes = [(1, 0), (1, 1), (0, 1), (0, 0)]
    glNormal3d(normal[0], normal[1], normal[2])
    for vertex, texIndex in zip(face, texIndexes):
        if not texture is None:
            glTexCoord2f(texIndex[0], texIndex[1])
        glVertex3fv(verticies[vertex])
    glEnd()


def retornaOsPesDoFogao(texture=None):
    verticies = (
        (0.1, -0.1, -0.1),  # 0
        (0.2, 0.1, -0.1),  # 1
        (-0.1, 0.1, -0.1),  # 2
        (-0.1, -0.1, -0.1),  # 3

        (0.1, -0.1, 0.1),  # 4
        (0.2, 0.1, 0.1),  # 5
        (-0.1, -0.1, 0.1),  # 6
        (-0.1, 0.1, 0.1)  # 7
    )

    if not texture is None:
        glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    for face, normal in zip(faces, normals):
        glNormal3d(normal[0], normal[1], normal[2])
        for vertex in face:
            glVertex3fv(verticies[vertex])
    glEnd()


def retornaGradesDoFogao(texture=None):
    verticies = (
        (0.0625 / 2, 0.0625 / 2, -0.0125),  # 0
        (0.4375 / 2, 0.125 / 2, -0.0125),  # 0.5
        (-0.125 / 2, 0.125 / 2, -0.0125),  # 2
        (-0.125 / 2, -0.125 / 2, -0.0125),  # 3

        (0.0625, 0.0625, 0.0125),  # 4
        (0.4375 / 2, 0.125 / 2, 0.0125),  # 5
        (-0.125 / 2, -0.125 / 2, 0.0125),  # 6
        (-0.125 / 2, 0.125 / 2, 0.0125)  # 7
    )

    if not texture is None:
        glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    for face, normal in zip(faces, normals):
        glNormal3d(normal[0], normal[1], normal[2])
        for vertex in face:
            glVertex3fv(verticies[vertex])
    glEnd()


class Fogao(BaseFurniture):
    translate = [16, -2.6, -6]
    scale = (1, 1, 1)
    rotate = (270, 0, 1, 0)

    def __init__(self, texture_loader: TextureLoader):
        super().__init__(texture_loader)

        self.fogaoTextura = [None, None, None, None, None, None, None, None]
        self.fogaoTextura[0] = self.texture_loader.load_texture('fogao-front.jpg')
        self.fogaoTextura[1] = self.texture_loader.load_texture('fogao-left-right.jpg')
        self.fogaoTextura[2] = self.texture_loader.load_texture('fogao-up-new.jpeg')
        self.fogaoTextura[3] = self.texture_loader.load_texture('fogao-left-right.jpg')
        self.fogaoTextura[4] = self.texture_loader.load_texture('fogao-left-right.jpg')
        self.fogaoTextura[5] = self.texture_loader.load_texture('fogao-left-right.jpg')
        self.fogaoTextura[6] = self.texture_loader.load_texture('grades.jpeg')
        self.fogaoTextura[7] = self.texture_loader.load_texture('pe-fogao.jpeg')

    def draw_on_scene(self):
        glScalef(*self.scale)
        glTranslate(*self.translate)
        glRotatef(*self.rotate)
        glColor3f(1, 1, 1)

        glPushMatrix()
        glTranslatef(0, 0, 0.)  # Monta as Faces do Fogão
        retornaNovaFace(face1, normal1, self.fogaoTextura[0])  # Z Positivo
        retornaNovaFace(face2, normal2, self.fogaoTextura[1])  # Z Negativo
        retornaNovaFace(face3, normal3, self.fogaoTextura[2])  # Y Positivo
        retornaNovaFace(face4, normal4, self.fogaoTextura[3])  # Y Negativo
        retornaNovaFace(face5, normal5, self.fogaoTextura[4])  # X Positivo
        retornaNovaFace(face6, normal6, self.fogaoTextura[5])  # X Negativo
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 2, 0.)
        retornaNovaFace(face2, normal2, self.fogaoTextura[5])  # Tampa do Fogão
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.9, -1.1, 0.9)
        retornaOsPesDoFogao(self.fogaoTextura[7])  # Pés do fogão
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.9, -1.1, 0.9)
        glRotatef(180.0, 0.0, 1.0, 0.0)
        retornaOsPesDoFogao(self.fogaoTextura[7])  # Pés do fogão
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.9, -1.1, -0.9)
        retornaOsPesDoFogao(self.fogaoTextura[7])  # Pés do fogão
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.9, -1.1, -0.9)
        glRotatef(180.0, 0.0, 1.0, 0.0)
        retornaOsPesDoFogao(self.fogaoTextura[7])  # Pés do fogão
        glPopMatrix()

        glPushMatrix()
        # glBindTexture(GL_TEXTURE_2D, self.fogaoTextura[6])
        q = gluNewQuadric()  # Grades das bocas do fogão
        gluQuadricDrawStyle(q, GLU_FILL)
        gluQuadricNormals(q, GLU_SMOOTH)
        glTranslatef(0.5, 1.01, 0.55)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        gluDisk(q, 0.2, 0.3, 64, 6)
        glPopMatrix()

        glPushMatrix()
        # glBindTexture(GL_TEXTURE_2D, self.fogaoTextura[6])
        q = gluNewQuadric()  # Grades das bocas do fogão
        gluQuadricDrawStyle(q, GLU_FILL)
        gluQuadricNormals(q, GLU_SMOOTH)
        glTranslatef(-0.5, 1.01, 0.55)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        gluDisk(q, 0.2, 0.3, 64, 6)
        glPopMatrix()

        glPushMatrix()
        # glBindTexture(GL_TEXTURE_2D, self.fogaoTextura[6])
        q = gluNewQuadric()  # Grades das bocas do fogão
        gluQuadricDrawStyle(q, GLU_FILL)
        gluQuadricNormals(q, GLU_SMOOTH)
        glTranslatef(0.5, 1.01, -0.55)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        gluDisk(q, 0.2, 0.3, 64, 6)
        glPopMatrix()

        glPushMatrix()
        # glBindTexture(GL_TEXTURE_2D, self.fogaoTextura[6])
        q = gluNewQuadric()  # Grades das bocas do fogão
        gluQuadricDrawStyle(q, GLU_FILL)
        gluQuadricNormals(q, GLU_SMOOTH)
        glTranslatef(-0.5, 1.01, -0.55)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        gluDisk(q, 0.2, 0.3, 64, 6)
        glPopMatrix()

        # Grade 1 Inicio
        glPushMatrix()
        glTranslatef(0.35, 1, 0.7)
        glRotatef(45.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.65, 1, 0.7)
        glRotatef(135.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.65, 1, 0.4)
        glRotatef(225.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.35, 1, 0.4)
        glRotatef(315.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()
        # Grade 1 Fim

        # Grade 2 Inicio
        glPushMatrix()
        glTranslatef(-0.35, 1, 0.7)
        glRotatef(135.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.65, 1, 0.7)
        glRotatef(45.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.65, 1, 0.4)
        glRotatef(315.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.35, 1, 0.4)
        glRotatef(225.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()
        # Grade 2 Fim

        # Grade 3 Inicio
        glPushMatrix()
        glTranslatef(0.35, 1, -0.7)
        glRotatef(315.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.65, 1, -0.7)
        glRotatef(225.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.65, 1, -0.4)
        glRotatef(135.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.35, 1, -0.4)
        glRotatef(45.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()
        # Grade 3 Fim

        # Grade 4 Inicio
        glPushMatrix()
        glTranslatef(-0.35, 1, -0.7)
        glRotatef(225.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.65, 1, -0.7)
        glRotatef(315.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.65, 1, -0.4)
        glRotatef(45.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.35, 1, -0.4)
        glRotatef(135.0, 0.0, 1.0, 0.0)
        retornaGradesDoFogao(self.fogaoTextura[6])
        glPopMatrix()
        # Grade 4 Fim
