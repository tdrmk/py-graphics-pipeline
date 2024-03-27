import pygame
from transformations import viewport, normalize
import numpy as np
from rasterizer import draw_triangle


class GraphicsPipeline:
    def __init__(self, meshs, camera, screen: pygame.Surface, shader=None):
        self.meshs = meshs
        self.camera = camera
        self.screen = screen
        self.shader = shader

    def update(self):
        # transform vertices from model space to screen space
        # ie, the vertex shader step
        view_matrix = self.camera.view_matrix
        projection_matrix = self.camera.projection_matrix
        camera_matrix = projection_matrix @ view_matrix
        viewport_matrix = viewport(*self.screen.get_size())
        camera_position = self.camera.position

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

                if self.shader is not None:
                    face_center = face.world_vertices[:3].mean(axis=1)
                    # store the face's light intensity for later use
                    # will be combined with the texture color to get the final color at the pixel
                    face.light_intensity = self.shader.light_intensity(
                        world_normal, face_center, camera_position
                    )
                faces_to_draw.append(face)

            # world space to clip space
            clip_vertices = camera_matrix @ world_vertices

            # perspective division
            image_vertices = clip_vertices / clip_vertices[3]
            # viewport transformation
            screen_vertices = viewport_matrix @ image_vertices

            # update the face's with transformed vertices
            for face in faces_to_draw:
                # w component is not needed anymore (it's always 1)
                face.screen_vertices = screen_vertices[:3, face.vertex_indices]

            mesh.faces_to_draw = faces_to_draw

    def draw(self):
        # draws the mesh's screen vertices onto the screen
        # ie, the rasterization step
        width, height = self.screen.get_size()

        # z buffer for hidden surface removal
        z_buffer = np.full((width, height), 1.0, dtype=np.float32)
        # display buffer to store the final image to be displayed
        display_buffer = np.zeros((width, height, 3), dtype=np.uint8)

        for mesh in self.meshs:
            for face in mesh.faces_to_draw:
                if face.screen_vertices is None:
                    continue
                color = self.shader.get_color(*face.light_intensity, (255, 255, 255))
                # draw the triangle onto the display buffer,
                # looking up the z buffer for hidden surface removal
                draw_triangle(face.screen_vertices, display_buffer, z_buffer, color)

        # blit the display buffer onto the screen
        pygame.surfarray.blit_array(self.screen, display_buffer)

        # draw wireframe
        for mesh in self.meshs:
            for face in mesh.faces_to_draw:
                if face.screen_vertices is None:
                    continue
                color = (255, 0, 0)
                points = face.screen_vertices[:2].T
                pygame.draw.polygon(self.screen, color, points, 1)
