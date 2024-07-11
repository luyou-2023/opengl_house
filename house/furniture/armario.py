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
    # 顶点坐标定义：vertices 定义了立方体的八个顶点坐标，每个顶点由三个坐标值 (x, y, z) 表示。
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

    glPushMatrix()  # 保存当前的模型视图矩阵

    if translate:
        glTranslatef(*translate)  # 平移变换

    if scale:
        glScalef(*scale)  # 缩放变换

    glColor3f(*color)  # 设置颜色

    glBegin(GL_TRIANGLES)  # 开始绘制三角形

    for (edge, normal) in zip(edges, normals):
        glNormal3d(*normal)  # 设置法线方向
        for vertex in edge:
            glVertex3fv(vertices[vertex])  # 设置顶点坐标

    glEnd()  # 结束绘制

    glPopMatrix()  # 恢复之前保存的模型视图矩阵

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
    #Armario 类包含了家具的位置 (translate)、缩放 (scale) 和旋转 (rotate) 属性。
    translate = [35, -8, -9]
    scale = (.5, .5, .5)
    rotate = (270, 0, 1, 0)

    def draw_on_scene(self):
        # 这个函数用于按照指定的比例缩放对象。在你的代码中，self.scale 是一个包含三个元素的元组，分别代表 x、y、z 轴的缩放比例。例如，如果 self.scale = (.5, .5, .5)，则对象在每个轴上缩小一半。
        glScalef(*self.scale)
        # 这个函数用于将对象平移到指定的位置。self.translate 是一个包含三个元素的元组，分别代表 x、y、z 轴上的平移量。例如，如果 self.translate = [35, -8, -9]，则对象将在 x 轴上平移 35 个单位，在 y 轴上向下平移 8 个单位，在 z 轴上向内平移 9 个单位。
        glTranslatef(*self.translate)
        # 这个函数用于按照指定的角度和轴旋转对象。self.rotate 是一个包含四个元素的元组，分别代表旋转角度和围绕的轴向量的 x、y、z 分量。例如，如果 self.rotate = (270, 0, 1, 0)，则对象将围绕 y 轴逆时针旋转 270 度。
        glRotatef(*self.rotate)
        draw_box()
        draw_divisions()
        draw_doors()
        draw_push()
        draw_footers()


'''
draw_cube(translate=(0, 1, 0), scale=(7, 10, 0.2))
让我们通过坐标图来解释这个调用。

解释和示意图
参数解析：

translate=(0, 1, 0)：平移参数，表示在三维空间中沿着 x、y、z 轴分别移动了 0、1、0 个单位。
scale=(7, 10, 0.2)：缩放参数，表示在 x、y、z 方向上分别缩放了 7、10、0.2 倍。
立方体的顶点坐标定义：
立方体的顶点坐标为 (x, y, z)，根据坐标的顺序分别为：

bash
复制代码
(0, 0, 0)  # 0
(1, 0, 0)  # 1
(0, 1, 0)  # 2
(1, 1, 0)  # 3
(0, 0, -1) # 4
(1, 0, -1) # 5
(0, 1, -1) # 6
(1, 1, -1) # 7
绘制流程：

glTranslatef(0, 1, 0)：在绘制之前将模型沿 y 轴正方向平移一个单位，使得立方体上升到 y 轴为 1 的位置。
glScalef(7, 10, 0.2)：在进行绘制时，在 x 方向上放大 7 倍，在 y 方向上放大 10 倍，在 z 方向上缩小为原来的 0.2 倍。
绘制的结果：

经过平移和缩放后，立方体的各个面会根据参数调整尺寸和位置。
具体效果图如下：
      (1,1,-1)  +-----------------------+ (1,1,0)
               |\                      \
               | \                      \
               |  \                      \
               |   \                      \
               |    \                      \
      (0,1,-1) +-----------------------+ (0,1,0)
               |      \                   |
               |       \                  |
               |        \                 |
               |         \                |
               |          \               |
      (0,0,-1) +-----------------------+ (0,0,0)
             (1,0,-1)                 (1,0,0)
这个图示展示了经过平移和缩放后的立方体在三维空间中的位置和尺寸。
'''
