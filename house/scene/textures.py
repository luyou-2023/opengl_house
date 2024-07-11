import os
import pygame
from OpenGL.GL import *


class TextureException(Exception):
    pass


class TextureLoader:
    def __init__(self, base_texture_path: str):
        if not os.path.isdir(base_texture_path):
            raise TextureException(f"{base_texture_path} is not a valid directory.")

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
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        # 设置纹理环绕方式为重复
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # 设置纹理过滤方式为邻近过滤
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # 返回生成的纹理ID
        return texture_id
