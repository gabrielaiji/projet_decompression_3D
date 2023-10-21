from objects import Vertex, Face

def coloration_to_obj(list_vertices: list[Vertex], list_faces: list[Face]):

    output_file = "../example/figure1_colore_exp.obj"

    # On redéfinit les ids pour pas qu'il y ait de "trous"
    for (vertex_index, _) in enumerate(list_vertices):
        list_vertices[vertex_index].setId(vertex_index)

    for (face_index, _) in enumerate(list_faces):
        list_faces[face_index].setId(face_index)


    with open(output_file, "w") as f:
        for vertex in list_vertices:
            f.write(f"v {vertex.x()} {vertex.y()} {vertex.z()}\n")

        for face in list_faces:
            f.write(f"f {face.getVertices[0].id()} {face.getVertices[1].id()} {face.getVertices[2].id()}\n")

            # Coloration
            if face.getColor() != None:
                f.write(f"fc {face.id()} {face.getColor[0]} {face.getColor[1]} {face.getColor[2]}\n")