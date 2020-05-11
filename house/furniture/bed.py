from OpenGL.GLU import *
from .base_furniture import BaseFurniture


class Bed(BaseFurniture):
    def draw_on_scene(self):
        q = gluNewQuadric()
        gluQuadricDrawStyle(q, GLU_FILL)
        gluQuadricNormals(q, GLU_SMOOTH)
        gluSphere(q, 1.5, 50, 50)
