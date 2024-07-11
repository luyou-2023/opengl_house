import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# 从 house 模块导入家具类
from house.furniture import X, Bed, Tv, Armario, Fogao, CadeiraDr
from house.scene import Controls, Camera, Lighting, draw_ground, TextureLoader, HouseStructure
import os

class Core:
    # 定义资源文件夹的基础路径
    base_resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')

    # 相机变量 (x, y, z)
    eye = (0, 0, 10)  # 相机位置
    target = (0, 0, 0)  # 相机目标位置（看向哪里）
    up = (0, 1, 0)  # 相机的上方向

    # 在计算机图形学中，光照模型通常使用一个四维向量来表示光的颜色和强度，其中前三个分量分别表示红色、绿色和蓝色（RGB）通道，第四个分量通常表示透明度或不透明度（alpha通道）。这个四维向量通常称为RGBA。
    # 光照变量
    luz_ambiente = (0.4, 0.4, 0.4, 1.0)  # 环境光颜色
    luz_difusa = (0.7, 0.7, 0.7, 1.0)  # 漫反射光颜色
    luz_especular = (1.0, 1.0, 1.0, 1.0)  # 镜面反射光颜色，第四个值是透明度
    posicao_luz = (0, 10, 0, 1.0)  # 光源位置
    especularidade = (1.0, 1.0, 1.0, 1.0)  # 高光度
    espec_material = 50  # 材质的高光反射指数

    def __init__(self, **kwargs):
        # 根据传入的参数初始化对象属性
        for key, value in kwargs.items():
            if self.__getattribute__(key):
                self.__setattr__(key, value)

        # 初始化纹理加载器 texture 通常指的是应用到3D模型表面上的二维图像。纹理可以用来增加模型表面的细节和真实感，而不需要增加几何复杂度。
        # 它从文件中读取图像数据并将其转换成可以在图形硬件（如GPU）上使用的格式。在OpenGL、DirectX或其他图形API中，加载的纹理会被应用到3D模型的表面上，从而在渲染时显示出图像细节。
        self.texture_loader = TextureLoader(os.path.join(self.base_resources_path, 'textures'))

        # 初始化 Pygame
        pygame.init()
        display = (1600, 900)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        # OpenGL 基础设置
        glClearColor(0.761, 0.773, 0.824, 1.0)  # 设置清除颜色为浅灰色
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # 设置多边形正反面为填充模式
        glEnable(GL_DEPTH_TEST)  # 启用深度测试
        glEnable(GL_TEXTURE_2D)  # 启用二维纹理映射

        # 设置透视投影
        gluPerspective(60, (display[0] / display[1]), 0.1, 90.0)

        # 待办事项：可能自动从家具模块检索类
        # clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

        # 初始化家具列表
        self.furnitures = [
            # X(self.texture_loader),
            Armario(self.texture_loader),
            Bed(self.texture_loader),
            Tv(self.texture_loader),
            Fogao(self.texture_loader),
            CadeiraDr(self.texture_loader, 15, 0, -30, init_rotate_y=1, init_angle_rotate=90),  # 卧室的椅子
            CadeiraDr(self.texture_loader, -50, 0, 5, init_rotate_y=1, init_angle_rotate=180),  # 厨房朝卧室的椅子
            CadeiraDr(self.texture_loader, -40, 0, 5, init_rotate_y=1, init_angle_rotate=180),  # 厨房朝卧室的椅子
            CadeiraDr(self.texture_loader, -30, 0, 5, init_rotate_y=1, init_angle_rotate=180),  # 厨房朝卧室的椅子
            CadeiraDr(self.texture_loader, 10, 0, -88)  # 厨房朝向炉子和柜子的椅子
        ]

        # 初始化相机、控制器、灯光和地面纹理
        self.camera = Camera(self.eye, self.target, self.up)
        self.controls = Controls(self.camera)
        self.controls.scene_objects = self.furnitures
        self.lighting = Lighting(
            self.especularidade,
            self.espec_material,
            self.luz_ambiente,
            self.luz_difusa,
            self.luz_especular,
            self.posicao_luz
        )
        self.lighting.set_lighting()

        # 加载地面纹理
        self.ground_texture = self.texture_loader.load_texture('ground_texture.png')
        # 绘制房屋结构
        self.house_structure = HouseStructure(self.texture_loader)

    def main_loop(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # 设置相机视角和灯光位置
        self.camera.set_look_at()
        self.lighting.set_lighting_position()

        # 处理事件
        self.event_capture_loop()

        # 绘制房屋结构
        self.house_structure.draw_structure()

        # 绘制家具
        self.draw_furniture_loop()

        # 绘制地面
        draw_ground(self.ground_texture)

        glPopMatrix()

        # 刷新显示
        pygame.display.flip()
        pygame.time.wait(33)

    def draw_furniture_loop(self):
        # 循环绘制每个家具
        for f in self.furnitures:
            glPushMatrix()
            f.draw_on_scene()  # 调用家具的绘制方法
            glPopMatrix()

    def event_capture_loop(self):
        # 处理事件循环
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                self.controls.handle_key(event.key)  # 处理键盘事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.controls.orbital_control(event.button)  # 处理鼠标事件
