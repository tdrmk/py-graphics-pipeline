import pygame
from transformations import viewport, normalize
import numpy as np


class GraphicsPipeline:
    def __init__(self, meshs, camera, screen: pygame.Surface):
        self.meshs = meshs
        self.camera = camera
        self.screen = screen

    def update(self):
        # transform vertices from model space to screen space
        # ie, the vertex shader step
        view_matrix = self.camera.view_matrix
        projection_matrix = self.camera.projection_matrix
        camera_matrix = projection_matrix @ view_matrix
        viewport_matrix = viewport(*self.screen.get_size())
        camera_position = self.camera.position

        self.faces_to_draw = []
        for mesh in self.meshs:
            faces_to_draw = []  # we'll computes faces to draw for each mesh

            world_matrix = mesh.world_matrix
            model_vertices = mesh.model_vertices
            world_vertices = world_matrix @ model_vertices

            # backface culling
            # here we'll be culling in world space
            for face in mesh.faces:
                face.world_vertices = world_vertices[:, face.vertex_indices]
                world_normal = face.world_normal
                camera_to_face = normalize(face.world_vertices[:3, 0] - camera_position)

                # if face normal and camera_to_face are in the same direction
                # then the face is facing away from the camera
                if np.dot(world_normal, camera_to_face) >= 0:
                    continue

                faces_to_draw.append(face)

            # world space to clip space
            clip_vertices = camera_matrix @ world_vertices

            # perspective division
            image_vertices = clip_vertices / clip_vertices[3]
            # viewport transformation
            screen_vertices = viewport_matrix @ image_vertices

            # update the face's with transformed vertices
            for face in faces_to_draw:
                face.screen_vertices = screen_vertices[:, face.vertex_indices]

            self.faces_to_draw.extend(faces_to_draw)

    def draw(self):
        # draws the mesh's screen vertices onto the screen
        # ie, the rasterization step
        self.screen.fill((0, 0, 0))
        for face in self.faces_to_draw:
            if face.screen_vertices is None:
                continue
            color = (255, 255, 255)
            points = face.screen_vertices[:2].T
            pygame.draw.polygon(self.screen, color, points, 1)
