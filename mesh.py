import pygame
import numpy as np


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
