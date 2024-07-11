import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def setup_perspective_projection(width, height):
    # 设置视口
    glViewport(0, 0, width, height)

    # 设置投影矩阵为透视投影
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)  # 调整远裁剪面距离为 100.0

    # 设置模型视图矩阵为单位矩阵（初始状态）
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def render_scene(camera_position):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # 设置相机位置和观察点
    gluLookAt(camera_position[0], camera_position[1], camera_position[2],  # 相机位置
              0, 0, 0,  # 观察点位置
              0, 1, 0)  # 上方向向量

    # 在这里绘制场景的物体
    glBegin(GL_TRIANGLES)
    glVertex3f(-1.0, -1.0, -5.0)  # 将物体位置调整到更远处
    glVertex3f(1.0, -1.0, -5.0)
    glVertex3f(0.0, 1.0, -5.0)
    glEnd()

    # 刷新显示
    pygame.display.flip()

# 在主程序中设置透视投影和渲染场景
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    setup_perspective_projection(display[0], display[1])

    camera_position = [0, 0, 5]  # 初始相机位置

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    camera_position[2] -= 0.1  # 向前移动相机
                elif event.key == pygame.K_DOWN:
                    camera_position[2] += 0.1  # 向后移动相机

        render_scene(camera_position)
        clock.tick(60)  # 控制帧率为60fps

if __name__ == "__main__":
    main()
