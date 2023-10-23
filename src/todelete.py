
import obja
import numpy as np
import open3d as o3d

from convert_obj_to_list_faces import read_obj,read_obj0


def get_edges(face):
    """Return edges from a given face."""
    return [(face[0], face[1]), (face[1], face[2]), (face[0], face[2])]

def compute_normal(triangle,vertices):
    """Compute the normal of a triangle."""
    v1 = np.array(vertices[triangle[1]-1]) - np.array(vertices[triangle[0]-1])
    v2 = np.array(vertices[triangle[2]-1]) - np.array(vertices[triangle[0]-1])
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)

def classify_vertex(vertex, triangles):
    """Return the classification of the vertex."""
    edges = [get_edges(triangle) for triangle in triangles]
    flat_edges = [edge for triangle_edges in edges for edge in triangle_edges]
    
    edge_counts = {edge: flat_edges.count(edge) for edge in flat_edges}
    
    for edge, count in edge_counts.items():
        if vertex in edge and (count < 1 or count > 2):
            return "complex",None
    
    boundary_edge = []
    for edge, count in edge_counts.items():
        if vertex in edge and count == 1:
            boundary_edge = edge
            return "boundary",boundary_edge
    return "unclassified", None

def is_cycle(triangles):
    """Check if the triangles form a cycle around the vertex."""
    visited_triangles = set()
    start_triangle = set(triangles[0])
    current_triangle = start_triangle
    
    while True:
        visited_triangles.add(tuple(sorted(list(current_triangle))))
        
        
        next_triangle = None
        for triangle in triangles:
            if tuple(sorted(triangle)) in visited_triangles:
                continue
            if len(current_triangle.intersection(set(triangle))) == 2:
                next_triangle = set(triangle)
                break
        
        # If no neighboring triangle is found
        if next_triangle is None:
            break
        
        current_triangle = next_triangle

    
    return len(visited_triangles) == len(triangles) #Il faudrait refaire le parcour en partant d'un autre triangle de l'ensemble de triangle et vérifier que les taille sont égale


def vertices_to_delete(faces,vertices):
    """Return a list of vertices to delete from the model.
    
    Args:
        faces (list): List of faces(List of 3-uplet containing the vertices index in their list).
        vertices (list): List of vertices(List of 3-uplet containing the vertices coordinates).    
    Returns:
        list: List of vertices to delete from the model.
    """


    forbidden_vertices = set()

    triangles_per_vertex = [[] for i in range(len(vertices))]
    for face in faces:
        for vertex in face:
            #print("C'est l'indice du vertex : ", str(vertex)+ " or la liste est de taille : ", str(len(triangles_per_vertex)))
            triangles_per_vertex[vertex].append(face)
    vertices_to_delete = []
    for vertex,trianglelist in enumerate(triangles_per_vertex):
        #print("Trianglelist est : ", trianglelist)
        #print("Vertex est : ", vertex)
        if is_cycle(trianglelist):
            #simple
            toDelete = distance_to_plane(vertex,trianglelist,vertices,deldist=0.01)
        else:
            #boundary or complexe
            print("pas de cycle")
            type,boundaryedge = classify_vertex(vertex, trianglelist)
            if type == "boundary":
                toDelete = distance_to_edge(vertex,boundaryedge,deldist=0.6)
            elif type == "complex" or "unclassified":
                toDelete = False
        if toDelete and not (vertex in forbidden_vertices):
            vertices_to_delete.append(vertex)
            forbidden_vertices.add(vertex)  # Add the current vertex to forbidden_vertices
            # Add adjacent vertices of the deleted vertex to the forbidden set
            #print("trianglelist : ", trianglelist)
            #print("vertex : ", vertex)
            for triangle in trianglelist:
                for adj_vertex_index in triangle:
                    """print("triangle : ", triangle)
                    print('adj_vertex_index : ', adj_vertex_index)"""
                    forbidden_vertices.add(adj_vertex_index)

    
    return vertices_to_delete

def distance_to_plane(vertex,triangles,vertices,deldist=0.2):
    """Return True if the vertex is close enough to the plane formed by the triangles.
    
    Args:
        vertex (list): List of 3-uplet containing the vertex coordinates.
        triangles (list): List of triangles(List of 3-uplet containing the vertices index in their list).
        deldist (float): Distance that define the close enoughness.
    Returns:
        bool: True if the vertex is close enough to the plane formed by the triangles.
    """
    normals = np.array([compute_normal(triangle,vertices) for triangle in triangles])
    
    """print("Vertex:", vertices[vertex])

    print("Computed normals[0]:", normals[0])"""
    average_normal = np.mean(normals, axis=0)
    dot_product = np.dot(average_normal, vertices[vertex])
    norm = np.linalg.norm(average_normal)
    distance = abs(dot_product) / norm
    """print("Dot product: ", dot_product)
    print("Norm: ", norm)
    print("Distance: ", distance)"""
    
    return (distance < deldist)

def distance_to_edge(vertex,boundaryedge,deldist=0.1):
    """Return True if the vertex is close enough to the edge formed by the triangles.
    
    Args:
        vertex (list): List of 3-uplet containing the vertex coordinates.
        triangles (list): List of triangles(List of 3-uplet containing the vertices index in their list).
        deldist (float): Distance that define the close enoughness.
    Returns:
        bool: True if the vertex is close enough to the edge formed by the triangles.
    """
    A = boundaryedge[0]
    B = boundaryedge[1]
    AP = np.array(vertex) - A
    AB = B - A
    magnitude_AB = np.linalg.norm(AB)
    projection = np.dot(AP, AB) / magnitude_AB
    
    if projection < 0:
        distance = np.linalg.norm(AP)
    elif projection > 1:
        distance = np.linalg.norm(np.array(vertex) - B)
    else:
        distance = np.linalg.norm(AP - projection * (AB / magnitude_AB))
    
    #print("Distance to edge : ", distance)
    return (distance < deldist)
    

def vertices_to_delete2(faces):
    """Return a list of vertices to delete from the model.
    
    Args:
        faces (list): List of faces(List Face object).    
    Returns:
        list: List of vertices to delete from the model.
    """

    all_vertices = {vertex.id(): vertex.getCoords() for face in faces for vertex in face.getVertices()}
    faceslist = [face.getVertexIds() for face in faces]
    verticeslist = [coords for _, coords in sorted(all_vertices.items())]

    return vertices_to_delete(faceslist, verticeslist)




def main():
    faces,_ = read_obj0(obja.parse_file('example/suzanne.obj'))
    delverts = vertices_to_delete2(faces)
    print(delverts)

if __name__ == "__main__":
    main()