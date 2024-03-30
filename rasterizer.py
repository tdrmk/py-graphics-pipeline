import numpy as np


# draws the triangle defined by the vertices (and the color) onto the display buffer,
# using the z-buffer for identifying the visible pixels
def draw_triangle(vertices, display_buffer, z_buffer, color):
    # assuming vertices are in screen space (ie, face.screen_vertices)

    width, height, _ = display_buffer.shape
    # sort vertices based on y-coordinate
    order = np.argsort(vertices[1])
    vertices = vertices[:, order]

    x0, x1, x2, y0, y1, y2, z0, z1, z2 = vertices.flatten()
    x0, x1, x2, y0, y1, y2 = map(int, (x0, x1, x2, y0, y1, y2))

    # calculate the x values along the edges 01, 02, 12
    x01 = np.linspace(x0, x1, y1 - y0 + 1)
    x02 = np.linspace(x0, x2, y2 - y0 + 1)
    x12 = np.linspace(x1, x2, y2 - y1 + 1)

    # calculate the z values along the edges
    z01 = np.linspace(z0, z1, y1 - y0 + 1)
    z02 = np.linspace(z0, z2, y2 - y0 + 1)
    z12 = np.linspace(z1, z2, y2 - y1 + 1)

    for y in range(y0, y2 + 1):
        if y < y1:
            # top half of the triangle
            x3, x4 = int(x01[y - y0]), int(x02[y - y0])
            z3, z4 = z01[y - y0], z02[y - y0]
        else:
            # bottom half of the triangle
            x3, x4 = int(x12[y - y1]), int(x02[y - y0])
            z3, z4 = z12[y - y1], z02[y - y0]
        if x3 > x4:
            x3, x4 = x4, x3
            z3, z4 = z4, z3

        # z values along line 34
        z34 = np.linspace(z3, z4, x4 - x3 + 1)
        for x in range(x3, x4 + 1):
            z = z34[x - x3]
            # make sure x and y are within the screen
            if 0 <= x < width and 0 <= y < height:
                # if the pixel is closer to the camera than the previous one
                if z < z_buffer[x, y]:
                    # update the z-buffer and display buffer
                    z_buffer[x, y] = z
                    display_buffer[x, y] = color


def draw_textured_triangle(
    vertices,
    texture_coordinates,
    display_buffer,
    z_buffer,
    texture,
    light_intensity=(1.0, 0.0, 0.0),
    shader=None,
):
    # assuming vertices are in screen space (ie, face.screen_vertices)
    # and texture_coordinates are in texture space (ie, face.texture_coordinates)

    if texture_coordinates is None or texture is None:
        # no texture or texture coordinates, just draw the triangle
        draw_triangle(vertices, display_buffer, z_buffer, (255, 255, 255))
        return

    width, height, _ = display_buffer.shape

    # sort vertices based on y-coordinate
    order = np.argsort(vertices[1])
    vertices = vertices[:, order]
    # sort the texture coordinates in the same order
    texture_coordinates = texture_coordinates[:, order]

    x0, x1, x2, y0, y1, y2, z0, z1, z2 = vertices.flatten()
    x0, x1, x2, y0, y1, y2 = map(int, (x0, x1, x2, y0, y1, y2))
    u0, u1, u2, v0, v1, v2 = texture_coordinates.flatten()

    # calculate the x values along the edges 01, 02, 12
    x01 = np.linspace(x0, x1, y1 - y0 + 1)
    x02 = np.linspace(x0, x2, y2 - y0 + 1)
    x12 = np.linspace(x1, x2, y2 - y1 + 1)

    # calculate the z values along the edges
    z01 = np.linspace(z0, z1, y1 - y0 + 1)
    z02 = np.linspace(z0, z2, y2 - y0 + 1)
    z12 = np.linspace(z1, z2, y2 - y1 + 1)

    # calculate the u, v values along the edges
    u01 = np.linspace(u0, u1, y1 - y0 + 1)
    u02 = np.linspace(u0, u2, y2 - y0 + 1)
    u12 = np.linspace(u1, u2, y2 - y1 + 1)

    v01 = np.linspace(v0, v1, y1 - y0 + 1)
    v02 = np.linspace(v0, v2, y2 - y0 + 1)
    v12 = np.linspace(v1, v2, y2 - y1 + 1)

    for y in range(y0, y2 + 1):
        if y < y1:
            # top half of the triangle
            x3, x4 = int(x01[y - y0]), int(x02[y - y0])
            z3, z4 = z01[y - y0], z02[y - y0]
            u3, u4 = u01[y - y0], u02[y - y0]
            v3, v4 = v01[y - y0], v02[y - y0]
        else:
            # bottom half of the triangle
            x3, x4 = int(x12[y - y1]), int(x02[y - y0])
            z3, z4 = z12[y - y1], z02[y - y0]
            u3, u4 = u12[y - y1], u02[y - y0]
            v3, v4 = v12[y - y1], v02[y - y0]
        if x3 > x4:
            x3, x4 = x4, x3
            z3, z4 = z4, z3
            u3, u4 = u4, u3
            v3, v4 = v4, v3

        # z values along line 34
        z34 = np.linspace(z3, z4, x4 - x3 + 1)
        u34 = np.linspace(u3, u4, x4 - x3 + 1)
        v34 = np.linspace(v3, v4, x4 - x3 + 1)
        for x in range(x3, x4 + 1):
            z = z34[x - x3]
            u = u34[x - x3]
            v = v34[x - x3]
            # make sure x and y are within the screen
            if 0 <= x < width and 0 <= y < height:
                # if the pixel is closer to the camera than the previous one
                if z < z_buffer[x, y]:
                    # update the z-buffer and display buffer
                    z_buffer[x, y] = z
                    color = texture.sample(u, v)
                    if shader is not None:
                        color = shader.get_color(*light_intensity, color)
                    display_buffer[x, y] = color
