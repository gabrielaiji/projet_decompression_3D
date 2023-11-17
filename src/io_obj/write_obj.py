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
            if face.getColor() != None:
                color = face.getColor()
                f.write(f"fc {face.id()} {color[0]} {color[1]} {color[2]}\n")

def write_obj_decompression(mesh: Mesh, output_file: str):
    vertices = mesh.getVertices()
    faces = mesh.getFaces()
    patches = mesh.getPatchesIterations()

    for (vertex_index, _) in enumerate(vertices):
        vertices[vertex_index].setId(vertex_index+1)
        last_vertex_index = vertex_index

    for (face_index, _) in enumerate(faces):
        faces[face_index].setId(face_index+1)

    with open(output_file, "w") as f:
        for vertex in vertices:
                f.write(f"v {vertex.x()} {vertex.y()} {vertex.z()}\n")

        for face in faces:
            vertex_ids = face.getVertexIds()
            f.write(f"f {vertex_ids[0]} {vertex_ids[1]} {vertex_ids[2]}\n")
            if face.getColor() != None:
                color = face.getColor()
                f.write(f"fc {face.id()} {color[0]} {color[1]} {color[2]}\n")

        for list_patch in patches:
            for patch in list_patch:
                patch_faces = patch.getPatchFaces()

                for face_a_supprimer in patch_faces:
                    id = face_a_supprimer.id()
                    f.write(f"df {id}\n")
                    
                    #faces.remove(face)
                    for face in faces:
                        if face_a_supprimer.getVertexIds() == face.getVertexIds():
                            faces.remove(face)
                        
                
                for (face_index, _) in enumerate(faces):
                    faces[face_index].setId(face_index+1)

                deleted_vertex = patch.getDeletedVertex()
                deleted_vertex.setId(last_vertex_index + 1)
                last_vertex_index += 1
                f.write(f"v {deleted_vertex.x()} {deleted_vertex.y()} {deleted_vertex.z()}\n")

                deleted_faces = patch.getDeletedFaces()

                for face in deleted_faces:
                    vertex_ids = face.getVertexIds()
                    f.write(f"f {vertex_ids[0]} {vertex_ids[1]} {vertex_ids[2]}\n")
                    faces.append(face)
                    if face.getColor() != None:
                        color = face.getColor()
                        f.write(f"fc {face.id()} {color[0]} {color[1]} {color[2]}\n")

                for (face_index, _) in enumerate(faces):
                    faces[face_index].setId(face_index+1)

                