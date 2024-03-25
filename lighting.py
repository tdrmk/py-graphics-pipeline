import numpy as np
from transformations import normalize

AMBIENT_LIGHT = 0.1
DIFFUSE_LIGHT = 0.6
SPECULAR_LIGHT = 0.3
SPECULAR_EXPONENT = 10

# 3D lighting model
# reference: https://www.youtube.com/watch?v=TEjDYtkLRdQ


class Lighting:
    def __init__(
        self, light_direction=np.array([0.0, 0.0, 1.0]), light_color=(255, 255, 255)
    ):
        self.light_direction = light_direction
        self.light_color = light_color

    def light_intensity(self, normal, object_position, camera_position):
        ambient = AMBIENT_LIGHT
        diffuse = DIFFUSE_LIGHT * max(0, np.dot(normal, -self.light_direction))
        point_to_camera = normalize(camera_position - object_position)
        specular = (
            SPECULAR_LIGHT
            * max(
                0,
                np.dot(normal, normalize(point_to_camera + -self.light_direction)),
            )
            ** SPECULAR_EXPONENT
        )
        return ambient, diffuse, specular

    # a simple fragment shader that calculates the color of the fragment (ie, pixel)
    def fragment_shader(
        self, normal, object_position, camera_position, texture_color=(255, 255, 255)
    ):
        ambient, diffuse, specular = self.light_intensity(
            normal, object_position, camera_position
        )
        color = (
            np.array(texture_color) * (ambient + diffuse)
            + np.array(self.light_color) * specular
        )

        return np.clip(color, 0, 255).astype(int)
