from transformations import *
import numpy as np
import pygame

TRANSLATION_SPEED = 5.0
ROTATION_SPEED = 1.0


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

    def update(self, dt):
        # update the camera's position and orientation
        # based on user input
        pressed = pygame.key.get_pressed()
        translation = np.array([0.0, 0.0, 0.0])
        rotation = np.array([0.0, 0.0, 0.0])

        if pressed[pygame.K_w]:  # move forward
            translation += np.array([0.0, 0.0, 1.0])
        if pressed[pygame.K_s]:  # move backward
            translation += np.array([0.0, 0.0, -1.0])
        if pressed[pygame.K_a]:  # move left
            translation += np.array([-1.0, 0.0, 0.0])
        if pressed[pygame.K_d]:  # move right
            translation += np.array([1.0, 0.0, 0.0])
        if pressed[pygame.K_r]:  # move up (wrt screen)
            translation += np.array([0.0, -1.0, 0.0])
        if pressed[pygame.K_f]:  # move down (wrt screen)
            translation += np.array([0.0, 1.0, 0.0])

        if pressed[pygame.K_UP]:  # rotate up (wrt screen)
            rotation += np.array([1.0, 0.0, 0.0])
        if pressed[pygame.K_DOWN]:  # rotate down (wrt screen)
            rotation += np.array([-1.0, 0.0, 0.0])
        if pressed[pygame.K_LEFT]:  # rotate left
            rotation += np.array([0.0, -1.0, 0.0])
        if pressed[pygame.K_RIGHT]:  # rotate right
            rotation += np.array([0.0, 1.0, 0.0])

        # we'll first translate the camera, and then rotate it

        if np.any(translation != 0.0):
            # compute the translation in camera space, based on user input
            translation = normalize(translation) * TRANSLATION_SPEED * dt

            # we'll need to translate in world space
            # we'll use the camera's right, up, and forward vectors
            # to determine the translation in world space
            position = self.position
            position += self.right * translation[0]
            position += self.up * translation[1]
            position += self.forward * translation[2]

            self.look_at(eye=position, forward=self.forward)

        if np.any(rotation != 0.0):
            # compute the rotation angles based on user input
            rotation = normalize(rotation) * ROTATION_SPEED * dt
            # we'll rotate the camera's forward vector those angles
            # and then update the camera to look at the new forward vector
            forward = rotate(*rotation) @ np.array([*self.forward, 1.0]).T
            forward = normalize(forward[:3])

            self.look_at(eye=self.position, forward=forward)

        # note: we are doing two look at operations in the update function
        # one for translation and one for rotation
