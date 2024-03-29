# functions for each of the clipping planes
# six functions for each of the six clipping planes
# and one function for clipping at w = 0, (ie, the vertices behind the camera)

# each function returns two functions:
#   - check_inside
#   - get_intersection

# check_inside takes a clip vertex and returns a boolean
# indicating if the vertex is inside the clip volume or not

# get_intersection takes two clip vertices (V0, V1) and returns a scalar (t)
# the intersection point is computes as V0 + t * (V1 - V0)


# w >= 0
def w_equals_0():
    check_inside = lambda cv: cv[3] > 0
    get_intersection = lambda cv1, cv2: cv1[3] / (cv1[3] - cv2[3])

    return check_inside, get_intersection


# x <= w
def w_equals_x():
    check_inside = lambda cv: cv[0] <= cv[3]
    get_intersection = lambda cv1, cv2: (cv1[3] - cv1[0]) / (
        (cv1[3] - cv1[0]) - (cv2[3] - cv2[0])
    )

    return check_inside, get_intersection


# x >= -w
def w_equals_neg_x():
    check_inside = lambda cv: cv[0] >= -cv[3]
    get_intersection = lambda cv1, cv2: (cv1[3] + cv1[0]) / (
        (cv1[3] + cv1[0]) - (cv2[3] + cv2[0])
    )

    return check_inside, get_intersection


# y <= w
def w_equals_y():
    check_inside = lambda cv: cv[1] <= cv[3]
    get_intersection = lambda cv1, cv2: (cv1[3] - cv1[1]) / (
        (cv1[3] - cv1[1]) - (cv2[3] - cv2[1])
    )

    return check_inside, get_intersection


# y >= -w
def w_equals_neg_y():
    check_inside = lambda cv: cv[1] >= -cv[3]
    get_intersection = lambda cv1, cv2: (cv1[3] + cv1[1]) / (
        (cv1[3] + cv1[1]) - (cv2[3] + cv2[1])
    )

    return check_inside, get_intersection


# z <= w
def w_equals_z():
    check_inside = lambda cv: cv[2] <= cv[3]
    get_intersection = lambda cv1, cv2: (cv1[3] - cv1[2]) / (
        (cv1[3] - cv1[2]) - (cv2[3] - cv2[2])
    )

    return check_inside, get_intersection


# z >= -w
def w_equals_neg_z():
    check_inside = lambda cv: cv[2] >= -cv[3]
    get_intersection = lambda cv1, cv2: (cv1[3] + cv1[2]) / (
        (cv1[3] + cv1[2]) - (cv2[3] + cv2[2])
    )

    return check_inside, get_intersection


# z >= 0
def z_equals_0():
    check_inside = lambda cv: cv[2] >= 0
    get_intersection = lambda cv1, cv2: cv1[2] / (cv1[2] - cv2[2])

    return check_inside, get_intersection
