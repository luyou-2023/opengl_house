import os
import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluPerspective
from pygame.locals import DOUBLEBUF, OPENGL, QUIT

class TextureException(Exception):
    pass

class TextureLoader:
    def __init__(self, base_texture_path):
        self.base_texture_path = base_texture_path

    def load_texture(self, filename: str):
        # 构建完整的文件路径
        full_filepath = os.path.join(self.base_texture_path, filename)

        # 检查文件是否存在，如果不存在则抛出异常
        if not os.path.isfile(full_filepath):
            raise TextureException(f"{full_filepath} is not a valid file.")

        # 使用Pygame加载图像文件为纹理表面
        texture_surface = pygame.image.load(full_filepath)

        # 将纹理表面转换为字符串格式的数据
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)

        # 获取纹理表面的宽度和高度
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        # 生成一个纹理ID
        texture_id = glGenTextures(1)

        # 绑定纹理ID到2D纹理目标
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # 指定2D纹理图像
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        # 设置纹理环绕方式为重复
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # 设置纹理过滤方式为邻近过滤
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # 返回生成的纹理ID
        return texture_id

def render(texture_id):
    # 清除颜色和深度缓冲
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 启用纹理映射
    glEnable(GL_TEXTURE_2D)

    # 绑定纹理
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)

    # 前面
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0,  1.0)

    # 后面
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0, -1.0)

    # 顶面
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0,  1.0)

    # 底面
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, -1.0,  1.0)

    # 右面
    glTexCoord2f(0.0, 0.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f( 1.0,  1.0, -1.0)

    # 左面
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0,  1.0, -1.0)

    glEnd()

    # 刷新显示
    pygame.display.flip()

def main():
    # 初始化Pygame
    pygame.init()

    # 设置显示模式
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # 设置视口
    glViewport(0, 0, display[0], display[1])

    # 设置投影矩阵
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)

    # 设置模型视图矩阵
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

    # 启用深度测试
    glEnable(GL_DEPTH_TEST)

    # 启用纹理映射
    glEnable(GL_TEXTURE_2D)

    base_resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'opengl_house/resources/textures')

    # 创建纹理加载器实例
    texture_loader = TextureLoader(base_resources_path)

    # 加载纹理
    texture_id = texture_loader.load_texture('textura_cadeira.jpeg')

    rotation_angle = 0

    # 主循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        # 每次渲染之前重置模型视图矩阵
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

        # 旋转立方体
        rotation_angle += 1
        glRotatef(rotation_angle, 1, 1, 1)

        # 渲染场景
        render(texture_id)
        pygame.time.wait(10)

if __name__ == "__main__":
    main()


'''
图解说明
顶点坐标和纹理坐标：

glVertex3f(-1.0, -1.0, 1.0)：顶点坐标为 (-1.0, -1.0, 1.0)，即在OpenGL的坐标系中，x 轴向左为负，y 轴向下为负，z 轴朝屏幕外为正。
glTexCoord2f(0.0, 0.0)：对应的纹理坐标为 (0.0, 0.0)，表示纹理的起始坐标。
纹理映射示意：

通过 glTexCoord2f 指定的纹理坐标，将纹理映射到对应的顶点上。这里 (0.0, 0.0) 对应左下角的顶点，(1.0, 1.0) 对应右上角的顶点，依此类推。
形成面：

顶点的连接顺序是按照逆时针方向形成面的，以确保正面和背面的正确渲染。
图解示意图
  (-1.0, 1.0, 1.0)  (1.0, 1.0, 1.0)
   1.0            3.0
     +------------+
     |            |
     |            |
     |     正 面   |
     |            |
     |            |
     +------------+
   0.0            2.0
  (-1.
  
  
  立方体前面的绘制过程
在OpenGL中，绘制立方体的前面需要指定每个顶点的坐标和对应的纹理坐标，以便将纹理正确映射到立方体的表面。

顶点坐标和纹理坐标：

每个顶点有一个三维坐标 (x, y, z) 和一个二维纹理坐标 (s, t)。在这里，(x, y, z) 是顶点在3D空间中的位置，(s, t) 是纹理上的坐标，通常取值范围是 [0, 1]。
顶点描述：

顶点描述的顺序和方式对于绘制面很重要。OpenGL通过连接顶点来形成三角形或四边形，并根据顶点的顺序来确定面的方向。
纹理映射：

纹理映射通过将纹理上的点映射到顶点上来实现。每个顶点指定一个纹理坐标，OpenGL在顶点之间插值来得到其它点的纹理坐标，从而在表面上显示纹理。
示意图解释
  (-1.0, 1.0, 1.0)  (1.0, 1.0, 1.0)
  +--------------+--------------+
  |              |              |
  |              |              |
  |    (0,0)     |    (1,0)     |
  |              |              |
  |              |              |
  +--------------+--------------+
  (-1.0, -1.0, 1.0)             (1.0, -1.0, 1.0)
  +--------------+--------------+

  
解释立方体的前面绘制过程
在OpenGL中，立方体的前面是一个平面，由两个三角形组成。每个三角形有三个顶点，我们需要指定每个顶点的三维坐标 (x, y, z) 和对应的纹理坐标 (s, t)。这些坐标帮助OpenGL将纹理正确映射到立方体的表面上。

顶点坐标和纹理坐标解释：
顶点坐标 (x, y, z)：

在立方体的情况下，我们定义了四个顶点来构成一个正方形平面。每个顶点的坐标如下：
左下角顶点：(-1.0, -1.0, 1.0)
右下角顶点：(1.0, -1.0, 1.0)
右上角顶点：(1.0, 1.0, 1.0)
左上角顶点：(-1.0, 1.0, 1.0)
这些坐标定义了平面的形状和位置，其中 (x, y) 坐标决定了在屏幕上的位置，而 z 坐标定义了顶点的深度或距离视点的距离。
纹理坐标 (s, t)：

纹理坐标是指定在纹理图像上的位置，通常取值范围在 [0, 1]。这些坐标告诉OpenGL如何将纹理映射到三角形的每个顶点上，以便纹理可以正确地贴在立方体的表面上。
例如，(0.0, 0.0) 表示纹理的左下角，(1.0, 1.0) 表示纹理的右上角。
示意图解释：
下面是一个简化的示意图，用于说明立方体前面的顶点和纹理映射过程：

scss
复制代码
  (-1.0, 1.0, 1.0)  (1.0, 1.0, 1.0)
   1.0            3.0
     +------------+
     |            |
     |            |
     |            |
     |            |
     |            |
     +------------+
  (-1.0, -1.0, 1.0)             (1.0, -1.0, 1.0)
   0.0                       2.0
顶点坐标：

左上角 (1)：坐标为 (-1.0, 1.0, 1.0)
右上角 (3)：坐标为 (1.0, 1.0, 1.0)
右下角 (2)：坐标为 (1.0, -1.0, 1.0)
左下角 (0)：坐标为 (-1.0, -1.0, 1.0)
纹理坐标：

(0, 0) 对应左下角顶点
(1, 0) 对应右下角顶点
(1, 1) 对应右上角顶点
(0, 1) 对应左上角顶点
'''


'''
视口（Viewport）
视口定义了OpenGL渲染的最终输出区域，通常是屏幕或窗口的一部分。它指定了OpenGL可以渲染图形的像素区域的位置和大小。视口的设置由 glViewport 函数控制，其参数为 (x, y, width, height)，分别表示视口在窗口中的左下角位置 (x, y) 和它的宽度和高度。

模型视图矩阵（Model-View Matrix）
模型视图矩阵用于定义场景中物体的位置和方向，以及相机的位置和方向。它将物体的坐标系转换到观察者的视角，同时定义了从世界坐标系到相机坐标系的变换。通过 glMatrixMode(GL_MODELVIEW) 和 glLoadIdentity() 来加载并重置模型视图矩阵，然后通过 gluLookAt 函数设置相机的位置、观察点和上方向。

投影矩阵（Projection Matrix）
投影矩阵定义了三维场景如何投影到二维视口上。它影响了视景体（viewing volume）内的对象如何映射到屏幕上，决定了场景中物体的透视效果和远近感。通常使用 glMatrixMode(GL_PROJECTION) 和 glLoadIdentity() 来加载并重置投影矩阵，然后通过 gluPerspective 函数设置透视投影或者通过 glOrtho 函数设置正交投影。

理解和使用
视口：确定OpenGL将渲染的窗口或屏幕区域。
模型视图矩阵：定义场景中物体和相机的位置和方向，将物体的坐标转换到相机视角。
投影矩阵：决定了三维场景如何投影到二维视口上，影响透视和远近效果。
这些矩阵的理解对于控制场景的可视化效果至关重要，它们的正确使用能够确保渲染出符合预期的视觉效果。
'''


'''
图解模型视图矩阵
在这个图示中，我们将展示一个简单的场景，包括一个物体和一个相机，以及它们之间的坐标变换过程。

世界坐标系：表示整个场景的坐标系统，包括物体和相机的位置。

模型坐标系：每个物体都有自己的局部坐标系，以便于描述物体的形状和位置。

观察坐标系（相机坐标系）：相机的坐标系定义了观察者的视角和方向，决定了场景中物体如何被观察到。

模型视图矩阵变换：模型视图矩阵负责将物体的模型坐标系变换到观察者的视角，即从世界坐标系变换到相机坐标系。

示意图解释
sql
复制代码
      +-------------------+      +-------------------+
      |                   |      |                   |
      |    World Space    |      |   Camera Space    |
      |                   |      |                   |
      +-------------------+      +-------------------+
              |                            |
              |                            |
              |                            |
              |                            |
              |                            |
              v                            |
      +-------------------+                |
      |                   |                |
      |   Model Space     |                |
      |                   |                |
      +-------------------+                |
              |                            |
              |                            |
              |                            |
              |                            |
              |                            |
              v                            v
      +-------------------+      +-------------------+
      |                   |      |                   |
      |   View Space      |      |  Projection Space |
      |                   |      |                   |
      +-------------------+      +-------------------+
World Space（世界坐标系）：整个场景的坐标系统，包括所有的物体和相机的位置。

Model Space（模型坐标系）：每个物体自己的局部坐标系，用来描述物体的形状和位置。

View Space（观察坐标系/相机坐标系）：相机的坐标系，定义了观察者的视角和方向，决定了如何从世界中观察物体。

Projection Space（投影坐标系）：通过投影矩阵定义的坐标系，将三维场景投影到二维视口上，影响透视和远近效果。

在OpenGL中，通过加载和组合这些不同的矩阵，可以将物体的本地坐标系转换到最终的屏幕上的坐标系，确保场景正确渲染和呈现给观察者。
'''

'''
图解投影矩阵
在这个图示中，我们将展示一个简单的场景，包括一个观察者（相机）和场景中的物体，以及投影矩阵如何将三维场景投影到二维视口上。

三维世界：表示整个场景的三维坐标系，包括物体和相机的位置。

视口：二维平面，表示最终渲染结果呈现的屏幕或窗口区域。

投影矩阵：定义了从三维世界到二维视口的投影方式，影响了透视和远近效果。

示意图解释
lua
复制代码
   +---------------------+
   |    三维世界坐标系    |
   |                     |
   |                     |
   |                     |
   |                     |
   |                     |
   +---------------------+
              |
              |
              |
              |
              |
              v
   +---------------------+
   |                     |
   |    投影矩阵变换     |
   |                     |
   +---------------------+
              |
              |
              |
              |
              v
   +---------------------+
   |                     |
   |      二维视口       |
   |                     |
   +---------------------+
三维世界坐标系：表示整个场景的三维坐标系统，包括所有的物体和相机的位置。

投影矩阵变换：投影矩阵的作用是将三维世界坐标系中的物体位置转换为二维视口上的位置。它可以是透视投影（Perspective Projection）或正交投影（Orthographic Projection），影响了场景中物体的远近感和大小比例。

二维视口：表示最终渲染结果呈现的屏幕或窗口区域，是观察者最终看到的画面。

投影矩阵的选择和设置对于呈现场景的逼真度和艺术效果至关重要。通过合理设置投影矩阵，可以控制观众在观看场景时的视角感受，从而达到更好的视觉效果。
'''

'''
在OpenGL中，大部分以 gl 开头的函数（例如 glGenTextures、glBindTexture、glTexImage2D 等）用于定义和配置OpenGL的状态和对象，比如纹理、顶点缓冲区、着色器等。这些函数实际上是在OpenGL的状态机中设置和配置了各种状态和对象的参数和数据。

具体到你提到的3D模型的情况：

定义和配置阶段：在程序初始化或者其他适当的时机调用 gl 开头的函数来定义和配置OpenGL的状态和对象，比如定义顶点数组、创建纹理、加载着色器等。这些操作实际上是在OpenGL的上下文（Context）中设置了相应的状态和数据。

渲染阶段：在渲染循环中，例如 render 函数中，实际的渲染工作发生。这时候调用的函数会根据之前定义和配置的状态和对象进行实际的绘制操作，例如设置顶点数据、绑定纹理、配置着色器程序等。

所以，OpenGL的工作流程可以简单描述为：首先设置和配置OpenGL的状态和对象（使用 gl 开头的函数），然后在渲染时执行绘制操作，利用之前设置的状态和对象来完成绘制任务。

这种分离定义和渲染的方式有助于提高渲染效率和灵活性，使得程序可以在不同的时机和情况下定义和修改OpenGL的状态，然后根据需要执行渲染操作。
'''
