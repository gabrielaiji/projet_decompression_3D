import obja
from objects import Vertex, Face, Mesh

def read_obj(obj:obja.Model):

    list_vertices = []
    for (vertex_index, vertex) in enumerate(obj.vertices):
        my_vertex = Vertex(vertex_index + 1, vertex[0], vertex[1], vertex[2]) # "+ 1" car les indices commencent à partir de 1
        list_vertices.append(my_vertex)

    list_faces = []
    for (face_index, face) in enumerate(obj.faces):
        list_3_vertices = [list_vertices[face.a], list_vertices[face.b], list_vertices[face.c]]
        my_face = Face(face_index + 1, list_3_vertices) # "+ 1" car les indices commencent à partir de 1
        my_face.addRefToVertices()
        list_faces.append(my_face)

    return list_faces, list_vertices 


def read_obj0(obj:obja.Model):

    list_vertices = []
    for (vertex_index, vertex) in enumerate(obj.vertices):
        my_vertex = Vertex(vertex_index , vertex[0], vertex[1], vertex[2]) 
        list_vertices.append(my_vertex)

    list_faces = []
    for (face_index, face) in enumerate(obj.faces):
        list_3_vertices = [list_vertices[face.a], list_vertices[face.b], list_vertices[face.c]]
        my_face = Face(face_index , list_3_vertices)
        my_face.addRefToVertices()
        list_faces.append(my_face)

    return list_faces, list_vertices

def read_Mesh(obj: obja.Model):
    list_faces, list_vertices = read_obj0(obj)
    return Mesh(list_vertices, list_faces)