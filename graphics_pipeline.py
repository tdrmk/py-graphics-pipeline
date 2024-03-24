import pygame
from transformations import viewport


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
        viewport_matrix = viewport(*self.screen.get_size())
        for mesh in self.meshs:
            world_matrix = mesh.world_matrix
            model_vertices = mesh.model_vertices
            # transform vertices from model space to screen space
            clip_vertices = (
                projection_matrix @ view_matrix @ world_matrix @ model_vertices
            )
            # perspective division
            image_vertices = clip_vertices / clip_vertices[3]
            # viewport transformation
            screen_vertices = viewport_matrix @ image_vertices

            # update the face's with transformed vertices
            for face in mesh.faces:
                face.screen_vertices = screen_vertices[:, face.vertex_indices]

    def draw(self):
        # draws the mesh's screen vertices onto the screen
        # ie, the rasterization step
        self.screen.fill((0, 0, 0))
        for mesh in self.meshs:
            for face in mesh.faces:
                if face.screen_vertices is None:
                    continue
                color = (255, 255, 255)
                points = face.screen_vertices[:2].T
                pygame.draw.polygon(self.screen, color, points, 1)
