import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


def setup_perspective_projection(width, height):
    # 设置视口
    glViewport(0, 0, width, height)

    # 设置投影矩阵为透视投影
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)

    # 启用深度测试并设置深度测试函数
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    # 设置模型视图矩阵为单位矩阵（初始状态）
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # 设置相机位置和观察点
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # 在这里绘制场景的物体
    glBegin(GL_TRIANGLES)
    glVertex3f(-1.0, -1.0, -2.0)
    glVertex3f(1.0, -1.0, -2.0)
    glVertex3f(0.0, 1.0, -2.0)
    glEnd()

    # 刷新显示
    pygame.display.flip()


# 在主程序中设置透视投影和渲染场景
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    setup_perspective_projection(display[0], display[1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        render_scene()
        pygame.time.wait(500)


if __name__ == "__main__":
    main()

'''
透视投影（Perspective Projection）是OpenGL中常用的一种投影方式，用于创建具有远近感的视觉效果，类似于我们在现实世界中看到的景物。它通过透视变换将三维空间中的物体投影到二维平面上。

透视投影的特点和用途：
近大远小效果：

透视投影能够呈现出近处物体较大、远处物体较小的效果，符合人眼在现实世界中的观察感知。
视景体（View Frustum）：

透视投影定义了一个视景体，即一个锥形区域，位于相机（观察者）的位置。这个锥形区域由近裁剪面（Near Plane）和远裁剪面（Far Plane）定义，近裁剪面靠近相机，远裁剪面则远离相机。
参数设置：

在OpenGL中，透视投影通过 gluPerspective() 函数来设置，需要提供视场角（Field of View，FOV）、宽高比（Aspect Ratio）、近裁剪面距离和远裁剪面距离等参数。
应用场景：

透视投影常用于需要真实感的场景，如三维游戏、虚拟现实（VR）、建筑可视化等领域。
'''
