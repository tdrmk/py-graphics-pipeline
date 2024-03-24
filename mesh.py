import pygame
import numpy as np
from transformations import translate, rotate, scale


class Face:
    def __init__(self, model_vertices, texture_coordinates=None, vertex_indices=None):
        # storing the indices of the vertices wrt the mesh's vertices array
        self.vertex_indices = vertex_indices
        self.model_vertices = model_vertices
        self.texture_coordinates = texture_coordinates
        # world coordinates after model transformation
        self.world_vertices = None
        # coordinates after camera transformation (wrt camera)
        self.view_vertices = None
        # homogeneous coordinates after perspective transformation
        self.clip_vertices = None
        # normalized device coordinates after perspective division
        self.image_vertices = None
        # screen coordinates after viewport transformation
        self.screen_vertices = None


class Mesh:
    def __init__(self, model_vertices, faces):
        # storing all the vertices of the model together
        # to speed up the calculations involving matrix multiplications
        # each column of the matrix is a vertex in homogeneous coordinates (x, y, z, w)
        self.model_vertices = model_vertices
        self.faces = faces
        self.texture = None

        # position, rotation, scale of the mesh wrt the world
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.scale = np.array([1.0, 1.0, 1.0])

    @property
    def world_matrix(self):
        # transforms from model space to world space
        return translate(*self.position) @ rotate(*self.rotation) @ scale(*self.scale)


def load_texture_from_image(filename) -> np.ndarray:
    texture = pygame.image.load(filename)
    # Note: flip the texture vertically, to align the coordinate systems
    texture = pygame.transform.flip(texture, False, True)
    texture = pygame.surfarray.array3d(texture)
    return texture


def load_mesh_from_obj(filename) -> Mesh:
    vertices = []
    faces = []
    texture_coordinates = []
    normals = []  # not used in this implementation

    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            splits = line.strip().split()
            if not splits:
                continue
            if splits[0] == "v":
                # x, y, z, (w=1.0)
                vertex = list(map(float, splits[1:]))
                if len(vertex) == 3:
                    vertex.append(1.0)
                vertices.append(vertex)
            elif splits[0] == "vt":
                # u, v
                texture_coordinate = list(map(float, splits[1:]))
                texture_coordinates.append(texture_coordinate)
            elif splits[0] == "vn":
                normals.append(list(map(float, splits[1:])))
            elif splits[0] == "f":
                # face can be in the following formats:
                # f v1 v2 v3 ....
                # f v1/vt1 v2/vt2 v3/vt3 ....
                # f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3 ....
                # f v1//vn1 v2//vn2 v3//vn3 ....
                face = []
                for vertex in splits[1:]:
                    vertex = vertex.split("/")
                    indices = {"v": None, "vt": None, "vn": None}
                    indices["v"] = int(vertex[0]) - 1
                    if len(vertex) > 1 and vertex[1] != "":
                        indices["vt"] = int(vertex[1]) - 1
                    if len(vertex) > 2:
                        indices["vn"] = int(vertex[2]) - 1

                    face.append(indices)

                if len(face) == 3:
                    faces.append(face)
                elif len(face) > 3:
                    # triangulate the face
                    for i in range(1, len(face) - 1):
                        faces.append([face[0], face[i], face[i + 1]])
    mesh_faces = []
    for face in faces:
        face_vertex_indices = [v["v"] for v in face]
        face_model_vertices = np.array([vertices[v["v"]] for v in face]).T
        face_texture = None
        if all(v["vt"] is not None for v in face):
            face_texture = np.array([texture_coordinates[v["vt"]] for v in face]).T
        mesh_faces.append(
            Face(
                model_vertices=face_model_vertices,
                texture_coordinates=face_texture,
                vertex_indices=face_vertex_indices,
            )
        )

    mesh = Mesh(model_vertices=np.array(vertices).T, faces=mesh_faces)
    return mesh


if __name__ == "__main__":
    # test the mesh loading
    mesh = load_mesh_from_obj("models/cube.obj")
    print(mesh.model_vertices)

    for i, face in enumerate(mesh.faces):
        print(f"\nFace {i}")
        print("model vertices:\n", face.model_vertices)
        print("texture coordinates:\n", face.texture_coordinates)
        print("vertex indices:", face.vertex_indices)
