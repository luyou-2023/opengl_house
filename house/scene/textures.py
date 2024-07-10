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
        full_filepath = os.path.join(self.base_texture_path, filename)
        if not os.path.isfile(full_filepath):
            raise TextureException(f"{full_filepath} is not a valid file.")

        texture_surface = pygame.image.load(full_filepath)
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
