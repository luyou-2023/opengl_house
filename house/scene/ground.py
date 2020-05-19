from OpenGL.GL import *


def draw_ground(ground_texture):
    y = -4

    glPushMatrix()
    glColor3fv((1, 1, 1))
    glBindTexture(GL_TEXTURE_2D, ground_texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3fv((25, y, 25))

    glTexCoord2f(25, 0)
    glVertex3fv((-25, y, 25))

    glTexCoord2f(25, 25)
    glVertex3fv((-25, y, -25))

    glTexCoord2f(0, 25)
    glVertex3fv((25, y, -25))

    glEnd()
    glPopMatrix()
    # unbind texture to avoid printing it on others elements
    glBindTexture(GL_TEXTURE_2D, 0)
