import pygame
from OpenGL.raw.GLU import gluPerspective, gluLookAt
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# 地图纹理列表
textures = ['/Users/luyou/code_work/shopastro/rust_code/opengl_house/resources/textures/fogao-front.jpg', '/Users/luyou/code_work/shopastro/rust_code/opengl_house/resources/textures/tv.jpg', '/Users/luyou/code_work/shopastro/rust_code/opengl_house/resources/textures/fogao-left-right.jpg']
current_texture_index = 0

def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texture_id

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glBindTexture(GL_TEXTURE_2D, textures[current_texture_index])

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, 0)

    glTexCoord2f(1, 0)
    glVertex3f(1, -1, 0)

    glTexCoord2f(1, 1)
    glVertex3f(1, 1, 0)

    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, 0)
    glEnd()

    pygame.display.flip()

def main():
    global textures, current_texture_index

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # 加载所有纹理
    textures = [load_texture(filename) for filename in textures]

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 切换到下一个纹理
                    current_texture_index = (current_texture_index + 1) % len(textures)

        render()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()


'''
在OpenGL中，每次调用 gl... 开头的函数设置的值会影响当前OpenGL的状态，但并不会自动清除上一次的设置。这意味着如果你在多次调用 render() 函数之间更改了OpenGL的状态（如绑定不同的纹理、设置不同的顶点数据等），则当前的状态会保持，直到下一次显式地修改或重置。

具体来说：

OpenGL 状态持久性：

OpenGL 的状态，例如当前绑定的纹理、顶点数组的设置等，会保持不变，直到你显式地重新设置或修改它们。
如果你在每次渲染中绑定不同的纹理，那么上一个纹理会继续绑定，直到你显式地重新绑定一个新的纹理。
影响展示的可能性：

如果在渲染场景时，每次调用 render() 函数之间更改了OpenGL的状态，可能会导致不同状态的混合或者意外的渲染效果。
例如，如果你在绘制一个物体时更改了纹理的绑定，可能会导致不同纹理之间的过渡效果或错误的渲染。
为了确保正确的渲染效果，通常需要在每次渲染前设置好所有需要的OpenGL状态，包括：

绑定正确的纹理对象 (glBindTexture)
设置正确的顶点数据 (glVertex, glTexCoord 等)
配置正确的渲染模式和参数 (glTexParameter, glEnable, glDisable 等)
'''

'''
glLoadIdentity() 是OpenGL中的一个函数，用于将当前的矩阵重置为单位矩阵。在OpenGL中，矩阵被用来描述各种变换（如模型视图变换、投影变换等），而 glLoadIdentity() 则用来重置当前矩阵，使其成为一个单位矩阵。

具体来说：

单位矩阵是一个特殊的方形矩阵，主对角线上的元素均为1，其它元素均为0。单位矩阵在矩阵运算中类似于数字运算中的1，对任何矩阵进行乘法运算，都会得到原来的矩阵。

glLoadIdentity() 的作用是将当前的矩阵（通常是模型视图矩阵或投影矩阵）重置为单位矩阵。这样做的目的是清除之前可能对该矩阵进行的所有变换，从而确保接下来的绘制操作不受之前变换的影响，从一个清空状态开始新的绘制操作。

在OpenGL中，常见的用法是在每次绘制场景之前调用 glLoadIdentity() 来确保绘制操作不受之前的变换影响。例如，在绘制下一个物体之前，可以调用 glLoadIdentity() 来确保物体的绘制基于一个清空的坐标系。

示例说明
python
复制代码
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 重置模型视图矩阵
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 执行需要的变换
    glTranslate(0.0, 0.0, -5.0)  # 示例中的平移变换

    # 绘制物体
    glBegin(GL_TRIANGLES)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()

    pygame.display.flip()
在这个例子中，glLoadIdentity() 用来确保每次渲染前模型视图矩阵都是一个单位矩阵，然后通过 glTranslate() 函数进行平移变换，最后绘制一个三角形。
'''
