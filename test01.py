'''
相机和光在计算机图形学和3D渲染中起着至关重要的作用。以下是相机和光在这个程序中的作用详细解释：

相机（Camera）
相机定义了场景的视角，即从哪个位置、朝向哪个方向看场景。它类似于现实世界中的相机，决定了我们看到的场景部分和角度。

eye: 定义相机的位置。在这个程序中，eye 的初始值是 (0, 0, 10)，表示相机位于 z 轴的 10 个单位处。

target: 定义相机的目标位置或焦点。在这个程序中，target 的初始值是 (0, 0, 0)，表示相机看向原点。

up: 定义相机的上方向，用于确定相机的旋转。在这个程序中，up 的初始值是 (0, 1, 0)，表示相机的上方向是 y 轴正方向。

在代码中，相机的作用是通过调用 gluLookAt 函数来设置相机的位置、目标和上方向，从而确定我们看到的场景视图。

光（Lighting）
光源在 3D 渲染中用于模拟真实世界的光照效果。光照影响了物体的颜色和阴影，从而使场景更加真实。

luz_ambiente: 环境光的颜色和强度。环境光是场景中每个点都均匀受到的光照，主要用于模拟散射光线。在这个程序中，环境光的初始值是 (0.4, 0.4, 0.4, 1.0)。

luz_difusa: 漫反射光的颜色和强度。漫反射光用于模拟光线照射在物体表面并均匀散射的效果。在这个程序中，漫反射光的初始值是 (0.7, 0.7, 0.7, 1.0)。

luz_especular: 镜面反射光的颜色和强度。镜面反射光用于模拟光线照射在物体表面并定向反射的效果，使物体表面看起来有光泽。在这个程序中，镜面反射光的初始值是 (1.0, 1.0, 1.0, 1.0)。

posicao_luz: 光源的位置。在这个程序中，光源的位置是 (0, 10, 0, 1.0)，表示光源位于 y 轴的 10 个单位处。

especularidade: 材质的高光反射强度。在这个程序中，especularidade 的初始值是 (1.0, 1.0, 1.0, 1.0)。

espec_material: 材质的高光反射指数。在这个程序中，espec_material 的值是 50，表示高光反射的强度。

在代码中，光源的作用是通过调用 OpenGL 的光照设置函数来定义光源的属性，从而影响场景中物体的光照效果，使得物体看起来更加真实。
'''

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

# 定义相机类，用于控制视角
class Camera:
    def __init__(self, eye, target, up):
        self.eye = eye
        self.target = target
        self.up = up

    def set_look_at(self):
        # 设置相机位置和方向
        gluLookAt(*self.eye, *self.target, *self.up)

# 定义光源类，用于设置光照参数
class Lighting:
    def __init__(self, ambient, diffuse, specular, position):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.position = position

    def set_lighting(self):
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)      # 设置环境光
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)      # 设置漫反射光
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)    # 设置镜面反射光
        glLightfv(GL_LIGHT0, GL_POSITION, self.position)    # 设置光源位置
        glEnable(GL_LIGHT0)                                 # 启用光源0
        glEnable(GL_LIGHTING)                               # 启用光照

# 定义主类，用于初始化和运行程序
class Core:
    def __init__(self):
        # 设置基础资源路径
        self.base_resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

        # 初始化Pygame
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        # 初始化相机
        self.camera = Camera((0, 0, 10), (0, 0, 0), (0, 1, 0))

        # 初始化光源
        self.lighting = Lighting(
            (0.2, 0.2, 0.2, 1.0),  # 环境光
            (0.8, 0.8, 0.8, 1.0),  # 漫反射光
            (1.0, 1.0, 1.0, 1.0),  # 镜面反射光
            (0, 10, 0, 1.0)        # 光源位置
        )

        # 设置OpenGL基础参数
        glClearColor(0.761, 0.773, 0.824, 1.0)  # 设置背景颜色
        glEnable(GL_DEPTH_TEST)                 # 启用深度测试
        glEnable(GL_LIGHTING)                   # 启用光照
        glEnable(GL_COLOR_MATERIAL)             # 启用颜色材质

        # 设置透视投影
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            # 设置相机视角
            self.camera.set_look_at()

            # 设置光照
            self.lighting.set_lighting()

            # 绘制一个立方体
            self.draw_cube()

            pygame.display.flip()
            pygame.time.wait(10)

    def draw_cube(self):
        # 定义立方体的顶点
        vertices = [
            (1, -1, -1),  # 顶点0
            (1, 1, -1),   # 顶点1
            (-1, 1, -1),  # 顶点2
            (-1, -1, -1), # 顶点3
            (1, -1, 1),   # 顶点4
            (1, 1, 1),    # 顶点5
            (-1, -1, 1),  # 顶点6
            (-1, 1, 1)    # 顶点7
        ]

        # 定义立方体的面，每个面由四个顶点组成
        faces = [
            (0, 1, 2, 3),  # 后面
           # (4, 5, 6, 7),  # 前面
            (0, 1, 5, 4),  # 右面
            (2, 3, 7, 6),  # 左面
            (1, 2, 7, 5),  # 顶面
            (0, 3, 6, 4)   # 底面
        ]

        # 每个面的颜色
        colors = [
            (1, 0, 0),  # 红色
            (0, 1, 0),  # 绿色
            (0, 0, 1),  # 蓝色
            (1, 1, 0),  # 黄色
            (1, 0, 1),  # 洋红
            (0, 1, 1)   # 青色
        ]

        # 每个面的法线
        normals = [
            (0, 0, -1),  # 后面
            (0, 0, 1),   # 前面
            (1, 0, 0),   # 右面
            (-1, 0, 0),  # 左面
            (0, 1, 0),   # 顶面
            (0, -1, 0)   # 底面
        ]

        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glColor3fv(colors[i])       # 设置当前面的颜色
            glNormal3fv(normals[i])     # 设置当前面的法线
            for vertex in face:
                glVertex3fv(vertices[vertex])  # 绘制顶点
        glEnd()

if __name__ == "__main__":
    core = Core()
    core.main_loop()
