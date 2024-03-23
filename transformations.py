import numpy as np

AXES = np.eye(4, 3)
EPSILON = 1e-6  # fudge factor for floating point comparisons
# note: all the angles are in radians


def normalize(v):
    norm = np.linalg.norm(v)
    if norm < EPSILON:  # avoid division by zero
        return v * 0.0  # return a zero vector
    return v / norm


def translate(tx, ty, tz):
    return np.array(
        [
            [1.0, 0.0, 0.0, tx],
            [0.0, 1.0, 0.0, ty],
            [0.0, 0.0, 1.0, tz],
            [0.0, 0.0, 0.0, 1.0],
        ],
    )


def scale(sx, sy, sz):
    return np.array(
        [
            [sx, 0.0, 0.0, 0.0],
            [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
    )


def rotate_x(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c, -s, 0.0],
            [0.0, s, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
    )


def rotate_y(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array(
        [
            [c, 0.0, s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
    )


def rotate_z(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array(
        [
            [c, -s, 0.0, 0.0],
            [s, c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
    )


# transforms from view space to clip space
def perspective(fov, aspect, near, far):
    f = 1.0 / np.tan(fov / 2.0)
    # vulkan's canonical view volume
    # - has z in range [0, 1]
    # - follows right-handed coordinate system
    return np.array(
        [
            [f / aspect, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, far / (far - near), -far * near / (far - near)],
            [0.0, 0.0, -1.0, 0.0],
        ],
    )


def rotate(x, y, z):
    # tait-bryan angles y-x-z (random order, just for fun)
    return rotate_z(z) @ rotate_x(x) @ rotate_y(y)
