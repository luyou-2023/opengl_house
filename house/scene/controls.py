from .camera import Camera
from pygame.constants import *


class Controls:
    key_map = {
        K_w: 'move_frontwards',
        K_s: 'move_backwards',
        K_d: 'move_right',
        K_a: 'move_left',

        K_UP: 'look_up',
        K_DOWN: 'look_down',
        K_RIGHT: 'look_right',
        K_LEFT: 'look_left',

    }

    def __init__(self, camera: Camera):
        self.camera = camera

    def handle_key(self, key):
        if key not in self.key_map:
            return

        func = self.__getattribute__(self.key_map[key])
        func()

    def move_frontwards(self):
        self.camera.eye_move_frontwards()

    def move_backwards(self):
        self.camera.eye_move_backwards()

    def move_right(self):
        self.camera.eye_move_right()

    def move_left(self):
        self.camera.eye_move_left()

    def look_up(self):
        self.camera.eye_look_up()

    def look_down(self):
        self.camera.eye_look_down()

    def look_right(self):
        self.camera.eye_look_right()

    def look_left(self):
        self.camera.eye_look_left()
