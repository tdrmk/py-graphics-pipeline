from transformations import *
import numpy as np


class Camera:
    def __init__(self, fov, aspect_ratio, near, far):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far

    @property
    def view_matrix(self):
        # to be implemented
        return np.eye(4)

    @property
    def projection_matrix(self):
        return perspective(self.fov, self.aspect_ratio, self.near, self.far)
