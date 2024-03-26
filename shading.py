import numpy as np
from transformations import normalize

AMBIENT_LIGHT = 0.1
DIFFUSE_LIGHT = 0.6
SPECULAR_LIGHT = 0.3
SPECULAR_EXPONENT = 10

# A pixel shader that calculates the color of the fragment (ie, pixel)
# assumes a single directional light source
# reference: https://www.youtube.com/watch?v=TEjDYtkLRdQ


class PixelShader:
    def __init__(
        self, light_direction=np.array([0.0, 0.0, 1.0]), light_color=(255, 255, 255)
    ):
        # the direction of the light source
        self.light_direction = light_direction
        self.light_color = light_color

    # calculates the intensity of the lighting at the fragment,
    # given the normal, position of the object and the camera
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

    # calculates the actual color of the pixel after applying the lighting,
    # given the ambient, diffuse, specular intensities and the texture color of the fragment
    def get_color(self, ambient, diffuse, specular, color=(255, 255, 255)):
        pixel_color = (
            np.array(color) * (ambient + diffuse)
            + np.array(self.light_color) * specular
        )

        return np.clip(pixel_color, 0, 255).astype(int)

    # computes the color of the fragment (pixel) given the normal, position of the object,
    # position of the camera and the texture color of the fragment (pixel)
    def compute_color(
        self, normal, object_position, camera_position, texture_color=(255, 255, 255)
    ):
        ambient, diffuse, specular = self.light_intensity(
            normal, object_position, camera_position
        )

        return self.get_color(ambient, diffuse, specular, texture_color)
