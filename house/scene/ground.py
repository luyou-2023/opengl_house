from OpenGL.GL import *


# todo: maybe replace this for a texture to remove loop overhead
def draw_ground():
    max_row_column = 25
    min_row_column = -25
    y = -4
    light_gray = (0.502, 0.502, 0.502)
    dark_gray = (0.863, 0.863, 0.863)

    glPushMatrix()
    glBegin(GL_TRIANGLES)
    colors = (light_gray, dark_gray)
    for row in range(min_row_column, max_row_column):
        for column in range(min_row_column, max_row_column):
            glColor3fv(colors[(column + row) % 2])
            a = (column, y, row + 1)  # (0, y, 1)
            b = (column + 1, y, row + 1)  # (1, y, 1)
            c = (column, y, row)  # (0, y, 0)
            d = (column + 1, y, row)  # (1, y, 0)

            glVertex3fv(a)
            glVertex3fv(b)
            glVertex3fv(c)

            glVertex3fv(c)
            glVertex3fv(b)
            glVertex3fv(d)

    glEnd()
    glPopMatrix()
