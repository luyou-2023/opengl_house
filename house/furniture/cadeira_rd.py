import pygame
from OpenGL.GL import *
import numpy as np

from house.furniture.base_furniture import BaseFurniture
from house.scene.textures import TextureLoader


def loadTexture(image_file):
    textureSurface = pygame.image.load(image_file)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1, image_file)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid


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

normals = (
    (0, 0, -1),
    (0, 0, 1),
    (0, -1, 0),
    (0, 1, 0),
    (-1, 0, 0),
    (1, 0, 0),
)

faces = (
    (0, 1, 2, 3),
    (4, 5, 7, 6),
    (0, 3, 6, 4),
    (1, 2, 7, 5),
    (2, 3, 6, 7),
    (0, 1, 5, 4)
)


# Função responável pela criação dos cubos
def Cubo(wireframe, texture=None):
    if not texture is None:
        glBindTexture(GL_TEXTURE_2D, texture)

    if wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glBegin(GL_QUADS)
    texIndexes = [(1, 0), (1, 1), (0, 1), (0, 0)]
    for face, normal in zip(faces, normals):
        glNormal3d(normal[0], normal[1], normal[2])
        for vertex, texIndex in zip(face, texIndexes):
            if not texture is None:
                glTexCoord2f(texIndex[0], texIndex[1])
            glVertex3fv(verticies[vertex])
    glEnd()


class CadeiraDr(BaseFurniture):
    scale = (0.2, 0.2, 0.2)
    translate = (10, -15, 0)
    # rotate = [270, 0, 1, 0]

    def draw_on_scene(self):
        self.desenhar_cadeira()

    def __init__(self, texture_loader: TextureLoader, init_x=0.0, init_y=0.0, init_z=0.0, init_rotate_x=0.0, init_rotate_y=0.0,
                 init_rotate_z=0.0, init_angle_rotate=0.0):
        super().__init__(texture_loader)
        self.tx = init_x
        self.ty = init_y
        self.tz = init_z

        self.rotate_x = init_rotate_x
        self.rotate_y = init_rotate_y
        self.rotate_z = init_rotate_z
        self.angle_rotate = init_angle_rotate

        self.diff_x = init_x
        self.diff_z = init_z
        self.wireframe = False
        self.texture = True
        self.m_cubeAngle = 0.0

        self.cadeira_textura = [None]
        self.cadeira_textura[0] = self.texture_loader.load_texture('textura_cadeira.jpeg')

        self.ctrlpoints = [
            [[-3.0, 3.0, -0.38], [0.4, 3.0, -0.8],  [3.0, 3.0, -0.38]],
            [[-3.0, 0.0, -0.38], [-0.5, 2.8, -2.0], [3.0, 0.0, -0.38]],
            [[-3.0, 0.0, -0.38], [-0.5, 1.5, -2.5], [3.0, 0.0, -0.38]],
            [[-3.0, 0.0, -0.38], [1.5, -1.0, -3.0], [3.0, 0.0, -0.38]],
            [[-3.0, -2.0, -0.38], [0.4, -2.0, -0.8], [3.0, -2.0, -0.38]],
        ]

        # self.ctrlpoints = 2 * np.array(self.ctrlpoints)

    def init_almofada(self):
        glMap2f(GL_MAP2_VERTEX_3, 0, 1, 0, 1, self.ctrlpoints)
        glEnable(GL_MAP2_VERTEX_3)
        glEnable(GL_AUTO_NORMAL)
        glMapGrid2f(20, 0.0, 1.0, 20, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def display_scene_almofada(self):
        glPushMatrix()

        glRotatef(self.m_cubeAngle, 1.0, 1.0, 0.0)
        glRotatef(self.m_cubeAngle, 0.0, 0.0, 1.0)

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
        glPopMatrix()

    def desenhar_cadeira(self):
        # Item A.1 e A.2: Criação do caractere
        self.texture = True

        glScalef(*self.scale)
        glTranslate(*self.translate)
        glRotatef(self.angle_rotate, self.rotate_x, self.rotate_y, self.rotate_z)

        glPushMatrix()

        glPushMatrix()  # matriz para a almofada

        glRotatef(90, 1, 0, 0)

        glTranslatef(self.tx, self.tz, self.ty * -1)
        self.init_almofada()
        # cube_color = [0.0, 0.8, 0.05]
        # cube_specular = [0.0, 0.8, 0.05]
        glBindTexture(GL_TEXTURE_2D, 0)
        # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, cube_color)
        # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, cube_specular)
        # glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 5.0)
        # glColor3fv([1, 1, 1])

        self.display_scene_almofada()

        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.tx, self.ty, self.tz)  # representa a posição da cadeira, de maneira geral.
        glScalef(3, 0.4, 3)
        Cubo(self.wireframe, texture=self.cadeira_textura[0])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.tx, self.ty, self.tz)
        glTranslatef(2.4, -3.2, 2.4)
        glScalef(0.4, 2.8, 0.4)
        Cubo(self.wireframe, texture=self.cadeira_textura[0])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.tx, self.ty, self.tz)
        glTranslatef(2.4, -3.2, -2.4)
        glScalef(0.4, 2.8, 0.4)
        Cubo(self.wireframe, texture=self.cadeira_textura[0])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.tx, self.ty, self.tz)
        glTranslatef(-2.4, -3.2, 2.4)
        glScalef(0.4, 2.8, 0.4)
        Cubo(self.wireframe, texture=self.cadeira_textura[0])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.tx, self.ty, self.tz)
        glTranslatef(-2.4, -3.2, -2.4)
        glScalef(0.4, 2.8, 0.4)
        Cubo(self.wireframe, texture=self.cadeira_textura[0])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.tx, self.ty, self.tz)
        glTranslatef(0, 3.9, -2.4)
        glScalef(2.8, 3.5, 0.4)
        Cubo(self.wireframe, texture=self.cadeira_textura[0])
        glPopMatrix()

        glPopMatrix()
