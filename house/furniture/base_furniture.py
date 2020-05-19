from house.scene.textures import TextureLoader


class BaseFurniture:
    translate = (0, 0, 0)
    scale = (1, 1, 1)

    def __init__(self, texture_loader: TextureLoader):
        self.texture_loader = texture_loader

    def draw_on_scene(self):
        raise Exception("Every furnitures should implementing this method to be drawn on the scene")
