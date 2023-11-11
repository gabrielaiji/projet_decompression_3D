from objects import Vertex, Face, Mesh

from typing import List

def write_mesh(mesh: Mesh, output_file: str):
    write_obj(mesh.getVertices(), mesh.getFaces(), output_file)

def write_obj(list_vertices: List[Vertex],
              list_faces: List[Face],
              output_file):

    # On redéfinit les ids pour pas qu'il y ait de "trous"
    for (vertex_index, _) in enumerate(list_vertices):
        list_vertices[vertex_index].setId(vertex_index+1)

    for (face_index, _) in enumerate(list_faces):
        list_faces[face_index].setId(face_index+1)


    with open(output_file, "w") as f:
        for vertex in list_vertices:
            f.write(f"v {vertex.x()} {vertex.y()} {vertex.z()}\n")

        for face in list_faces:
            vertex_ids = face.getVertexIds()
            f.write(f"f {vertex_ids[0]} {vertex_ids[1]} {vertex_ids[2]}\n")

        # Coloration
        for face in list_faces:
            if face.getColor() != None:
                color = face.getColor()
                f.write(f"fc {face.id()} {color[0]} {color[1]} {color[2]}\n")