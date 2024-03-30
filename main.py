from mesh import load_mesh_from_obj
from graphics_pipeline import GraphicsPipeline
from game import Game, WIDTH, HEIGHT
from camera import Camera
from shading import PixelShader, init_lighting
from texture import load_texture_from_image
import numpy as np


FOV = np.deg2rad(60)

# initialize the lighting
init_lighting(ambient=0.4, diffuse=0.4, specular=0.2, specular_exponent=10)

if __name__ == "__main__":
    # load the mesh
    mesh = load_mesh_from_obj("models/cottage.obj")
    mesh.scale = np.array([0.1, -0.1, 0.1])
    mesh.rotation = np.array([0.0, 0.0, 0.0])
    mesh.position = np.array([0.0, 0.0, 10.0])

    # load the texture
    texture = load_texture_from_image("models/cottage.png")
    mesh.texture = texture

    # create the camera, shader, game, and graphics pipeline
    camera = Camera(FOV, WIDTH / HEIGHT, 1, 50.0)
    shader = PixelShader(light_direction=np.array([0, 1, 1]))
    game = Game()
    graphics_pipeline = GraphicsPipeline([mesh], camera, game.screen, shader=shader)

    # add update and draw functions
    game.add_update_func(camera.update)
    game.add_update_func(lambda _: graphics_pipeline.update())
    game.add_draw_func(graphics_pipeline.draw_textured)

    # run the game loop
    game.run()
