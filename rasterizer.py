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
