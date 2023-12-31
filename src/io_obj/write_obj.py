from objects import Vertex, Face, Mesh
from coloration import couleurs

from typing import List
from . import getColorEntropy

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
                color = couleurs[face.getColor()]
                f.write(f"fc {face.id()} {color[0]} {color[1]} {color[2]}\n")

def write_obj_decompression(mesh: Mesh, output_file: str):
    vertices = mesh.getVertices()
    faces = mesh.getFaces()
    patches = mesh.getPatchesIterations()

    for (vertex_index, _) in enumerate(vertices):
        vertices[vertex_index].setId(vertex_index+1)
        last_vertex_index = vertex_index + 1

    for (face_index, _) in enumerate(faces):
        faces[face_index].setId(face_index+1)
        last_face_index = face_index + 1

    #color_entropy_octet = getColorEntropy(mesh)/8
    #nb_octet = 0

    with open(output_file, "w") as f:
        for vertex in vertices:
                f.write(f"v {vertex.x()} {vertex.y()} {vertex.z()}\n")

        for face in faces:
            vertex_ids = face.getVertexIds()
            f.write(f"f {vertex_ids[0]} {vertex_ids[1]} {vertex_ids[2]}\n")


        for list_patch in patches:
            
            for patch in list_patch:
                for face in patch.getPatchFaces():
                    if face.getColor() != None:
                        color = couleurs[face.getColor()]
                        f.write(f"fc {face.id()} {color[0]} {color[1]} {color[2]}\n")

            for patch in list_patch:
                patch_faces = patch.getPatchFaces()

                for face_a_supprimer in patch_faces:
                    id = face_a_supprimer.id()
                    f.write(f"df {id}\n")
                        
                deleted_vertex = patch.getDeletedVertex()
                deleted_vertex.setId(last_vertex_index + 1)
                last_vertex_index += 1
                f.write(f"v {deleted_vertex.x()} {deleted_vertex.y()} {deleted_vertex.z()}\n")

                displacement_coords = patch.getDisplacementCoords()
                f.write(f"tv {deleted_vertex.id()} {displacement_coords[0]} {displacement_coords[1]} {displacement_coords[2]}\n")

                deleted_faces = patch.getDeletedFaces()

                for face_a_ajouter in deleted_faces:
                    face_a_ajouter.setId(last_face_index + 1)
                    last_face_index += 1
                    vertex_ids = face_a_ajouter.getVertexIds()
                    f.write(f"f {vertex_ids[0]} {vertex_ids[1]} {vertex_ids[2]}\n")



                