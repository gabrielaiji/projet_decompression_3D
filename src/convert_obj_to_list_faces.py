import obja
from objects import Vertex, Face

def convert_obj_to_list_faces(obj:obja.Model):

    list_vertices = []
    for (vertex_index, vertex) in enumerate(obj.vertices):
        my_vertex = Vertex(vertex_index + 1, vertex[0], vertex[1], vertex[2]) # "+ 1" car les indices commencent à partir de 1
        list_vertices.append(my_vertex)

    list_faces = []
    for (face_index, face) in enumerate(obj.faces):
        list_3_vertices = [list_vertices[face.a], list_vertices[face.b], list_vertices[face.c]]
        my_face = Face(face_index + 1, list_3_vertices) # "+ 1" car les indices commencent à partir de 1
        list_faces.append(my_face)

    return list_faces    
