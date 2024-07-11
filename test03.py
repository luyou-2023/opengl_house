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
            self.draw_cube_with_thickness(0.1)

            pygame.display.flip()
            pygame.time.wait(10)

    def draw_cube_with_thickness(self, thickness):
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

        # 定义内层立方体的顶点
        inner_vertices = [
            (1 - thickness, -1 + thickness, -1 + thickness),
            (1 - thickness, 1 - thickness, -1 + thickness),
            (-1 + thickness, 1 - thickness, -1 + thickness),
            (-1 + thickness, -1 + thickness, -1 + thickness),
            (1 - thickness, -1 + thickness, 1 - thickness),
            (1 - thickness, 1 - thickness, 1 - thickness),
            (-1 + thickness, -1 + thickness, 1 - thickness),
            (-1 + thickness, 1 - thickness, 1 - thickness)
        ]

        # 定义立方体的面，每个面由四个顶点组成
        faces = [
            (0, 1, 2, 3),  # 后面
            #(4, 5, 6, 7),  # 前面
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

        # 绘制外层立方体
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glColor3fv(colors[i])       # 设置当前面的颜色
            glNormal3fv(normals[i])     # 设置当前面的法线
            for vertex in face:
                glVertex3fv(vertices[vertex])  # 绘制顶点
        glEnd()

        # 绘制内层立方体
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glColor3fv(colors[i])       # 设置当前面的颜色
            glNormal3fv(normals[i])     # 设置当前面的法线
            for vertex in face:
                glVertex3fv(inner_vertices[vertex])  # 绘制顶点
        glEnd()

        # 绘制连接内外层立方体的边
        glBegin(GL_QUADS)
        for i in range(4):
            glColor3fv((0.5, 0.5, 0.5))  # 设置边的颜色为灰色
            # 绘制后面到前面的边
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[(i + 1) % 4])
            glVertex3fv(inner_vertices[(i + 1) % 4])
            glVertex3fv(inner_vertices[i])

            # 绘制底面到顶面的边
            glVertex3fv(vertices[i + 4])
            glVertex3fv(vertices[(i + 1) % 4 + 4])
            glVertex3fv(inner_vertices[(i + 1) % 4 + 4])
            glVertex3fv(inner_vertices[i + 4])

            # 绘制底面到前面的边
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[i + 4])
            glVertex3fv(inner_vertices[i + 4])
            glVertex3fv(inner_vertices[i])
        glEnd()

if __name__ == "__main__":
    core = Core()
    core.main_loop()


'''
在计算机图形学中，法线（normal）是指与曲面或多边形某一点的垂直方向的一个向量。法线向量通常用于描述表面的朝向和光照计算。

作用：
表面光照计算： 光线照射到表面时，法线决定了光线的入射角度和表面反射光的方向。在光照模型中，根据入射光线的方向和法线的方向可以计算出反射光的强度和颜色，从而实现表面的阴影和高光效果。

渲染和着色： 法线信息有助于渲染引擎正确计算和描绘表面的几何特征。例如，法线可以影响光照模型中的漫反射和镜面反射效果，使得物体在不同光照条件下呈现出真实的阴影和高光。

碰撞检测： 法线向量在物理仿真和碰撞检测中也有重要作用。例如，碰撞检测算法可以利用法线判断物体之间的接触和碰撞情况，从而模拟真实世界中的物体互动。

如何使用：
在OpenGL中，通过设置每个面的法线向量，可以使得光照模型正确计算出每个面的光照效果。在绘制三维模型时，通常需要指定每个顶点的法线向量，以确保整个模型的光照效果正确和连贯。

法线向量的方向非常重要，因为它决定了光线的反射和入射角度。在处理复杂表面或者曲面时，可能需要计算或者估算法线向量，以确保光照效果的真实性和精确性。

总之，法线向量在计算机图形学中是一个非常重要的概念，它影响了表面的视觉表现、光照效果以及物理模拟的准确性和真实感。
'''
