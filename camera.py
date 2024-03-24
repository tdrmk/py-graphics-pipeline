from transformations import *
import numpy as np


class Camera:
    def __init__(self, fov, aspect_ratio, near, far):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        # initialising the camera's position and orientation
        # the camera is looking down the positive z-axis
        # and centered at the origin
        self.look_at(
            eye=np.array([0.0, 0.0, 0.0]),
            forward=np.array([0.0, 0.0, 1.0]),
            up=np.array([0.0, 1.0, 0.0]),
        )

    def look_at(self, eye, forward=None, up=np.array([0, 1.0, 0]), target=None):
        # using the right-handed coordinate system
        # eye: the position of the camera
        # camera's orientation is specified either by forward or target
        # forward: the direction the camera is facing
        # target: the position the camera is looking at
        # up: the direction of the camera's up (may not be orthogonal to forward)
        self.position = eye  # camera's position
        self.forward = normalize(forward if forward is not None else target - eye)
        self.right = normalize(np.cross(up, self.forward))
        self.up = np.cross(self.forward, self.right)
        print(f"forward: {self.forward}, right: {self.right}, up: {self.up}")
        print(f"position: {self.position}")
        print(f"view_matrix: {self.view_matrix}")

    @property
    def view_matrix(self):
        u = self.right
        v = self.up
        w = self.forward
        tx = -np.dot(self.position, u)
        ty = -np.dot(self.position, v)
        tz = -np.dot(self.position, w)
        return np.array(
            [
                [u[0], u[1], u[2], tx],
                [v[0], v[1], v[2], ty],
                [w[0], w[1], w[2], tz],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @property
    def projection_matrix(self):
        return perspective(self.fov, self.aspect_ratio, self.near, self.far)
