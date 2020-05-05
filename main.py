import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from house.furniture import X
from house.scene import Controls, Camera, Lighting, draw_ground


def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # base settings
    glClearColor(0.761, 0.773, 0.824, 1.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)

    # set perspective
    gluPerspective(45, (display[0] / display[1]), .1, 50.0)

    # camera vars
    eye = (0, 0, 10)
    target = (0, 0, 0)
    up = (0, 1, 0)

    # light vars
    luzAmbiente = (0.1, 0.1, 0.1, 1.0)
    luzDifusa = (0.7, 0.7, 0.7, 1.0)
    luzEspecular = (1.0, 1.0, 1.0, 1.0)
    posicaoLuz = (5.0, 0.0, 0.0, 1.)
    especularidade = (1.0, 1.0, 1.0, 1.0)
    especMaterial = 1

    # todo: maybe auto retrieve classes from furniture module
    # clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    furniture = [X()]
    camera = Camera(eye, target, up)
    controls = Controls(camera)
    lighting = Lighting(especularidade, especMaterial, luzAmbiente, luzDifusa, luzEspecular, posicaoLuz)
    lighting.set_lighting()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                controls.handle_key(event.key)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        camera.set_look_at()

        draw_ground()

        for f in furniture:
            f.draw_on_scene()
        # draw_chair()

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(33)


if __name__ == "__main__":
    main()
