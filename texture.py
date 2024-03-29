import pygame
import numpy as np


class Texture:
    def __init__(self, texture: np.ndarray):
        self.texture = texture
        self.width, self.height, _ = texture.shape

    def sample(self, u, v):
        # u, v are texture coordinates
        # we'll clamp the texture coordinates to the range [0, 1]
        x = np.clip(int(u * self.width), 0, self.width - 1)
        y = np.clip(int(v * self.height), 0, self.height - 1)
        return self.texture[x, y]


def load_texture_from_image(filename) -> Texture:
    texture = pygame.image.load(filename)
    # Note: flip the texture vertically, to align the coordinate systems
    texture = pygame.transform.flip(texture, False, True)
    texture = pygame.surfarray.array3d(texture)
    return Texture(texture)


def random_texture(width, height):
    return Texture(np.random.randint(0, 255, (width, height, 3), dtype=np.uint8))
