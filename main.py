from mesh import load_mesh_from_obj
from graphics_pipeline import GraphicsPipeline
from game import Game, WIDTH, HEIGHT
from camera import Camera
import numpy as np


FOV = np.deg2rad(60)
if __name__ == "__main__":
    mesh = load_mesh_from_obj("models/cube.obj")
    camera = Camera(FOV, WIDTH / HEIGHT, 0.1, 1000)
    game = Game()
    graphics_pipeline = GraphicsPipeline([mesh], camera, game.screen)
    game.add_draw_func(graphics_pipeline.draw)
    mesh.position = np.array([0, 0, 5])

    def rotate_mesh(dt):
        mesh.rotation += np.array([1, 0, 0]) * dt

    game.add_update_func(camera.update)
    game.add_update_func(rotate_mesh)
    game.add_update_func(lambda _: graphics_pipeline.update())
    game.run()
