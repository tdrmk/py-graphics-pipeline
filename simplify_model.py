#!/usr/bin/env python3

import argparse
from mesh import load_mesh_from_obj


# this function takes a model and outputs another model
# with same geometry, ignores all properties, except vertices, and textures
# removes unused vertices and textures
def simplify_model(input_obj_file, output_obj_file):
    mesh = load_mesh_from_obj(input_obj_file)
    vertices, textures = [], []

    with open(output_obj_file, "w") as f:

        for face in mesh.faces:
            for vertex in face.model_vertices.T:
                vertex = tuple(vertex)
                if vertex not in vertices:
                    print("v", *vertex[:3], sep=" ", file=f)
                    vertices.append(vertex)
        for face in mesh.faces:
            for texture in face.texture_coordinates.T:
                texture = tuple(texture)
                if texture not in textures:
                    print("vt", *texture, sep=" ", file=f)
                    textures.append(texture)

        for face in mesh.faces:
            texture_indices = [
                textures.index(tuple(texture)) + 1
                for texture in face.texture_coordinates.T
            ]
            vertex_indices = [
                vertices.index(tuple(vertex)) + 1 for vertex in face.model_vertices.T
            ]
            zipped = zip(vertex_indices, texture_indices)
            print("f", *(f"{v}/{t}" for v, t in zipped), sep=" ", file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Takes a model and outputs another model with same geometry, ignores all properties, except vertices, and textures, removes unused vertices and textures.",
        prog="python3 simplify_model.py",
    )
    parser.add_argument("input_obj_file", help="input wavefront obj file to simplify")
    parser.add_argument("output_obj_file", help="output filename")
    args = parser.parse_args()
    simplify_model(args.input_obj_file, args.output_obj_file)
