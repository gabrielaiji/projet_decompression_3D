

import numpy as np


def get_edges(face):
    """Return edges from a given face."""
    return [(face[0], face[1]), (face[1], face[2]), (face[0], face[2])]

def compute_normal(triangle):
    """Compute the normal of a triangle."""
    v1 = np.array(triangle[1]) - np.array(triangle[0])
    v2 = np.array(triangle[2]) - np.array(triangle[0])
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)

def classify_vertex(vertex, triangles):
    """Return the classification of the vertex."""
    edges = [get_edges(triangle) for triangle in triangles]
    flat_edges = [edge for triangle_edges in edges for edge in triangle_edges]
    
    edge_counts = {edge: flat_edges.count(edge) for edge in flat_edges}
    
    # Check if vertex is complex
    for edge, count in edge_counts.items():
        if vertex in edge and (count < 1 or count > 2):
            return "complex",None
    
    boundary_edge = []
    for edge, count in edge_counts.items():
        if vertex in edge and count == 1:
            boundary_edge = edge
            return "boundary",boundary_edge

    


def is_cycle(triangles):
    """Check if the triangles form a cycle around the vertex."""
    visited_triangles = set()
    queue = [triangles[0]]
    
    while queue:
        current_triangle = queue.pop()
        if current_triangle in visited_triangles:
            continue
        visited_triangles.add(current_triangle)
        
        for neighbor_triangle in triangles:
            if neighbor_triangle not in visited_triangles and \
               len(set(current_triangle).intersection(set(neighbor_triangle))) == 2:
                queue.append(neighbor_triangle)
                
    return len(visited_triangles) == len(triangles)

def vertices_to_delete(faces,vertices):
    """Return a list of vertices to delete from the model.
    
    Args:
        faces (list): List of faces(List of 3-uplet containing the vertices index in their list).
        vertices (list): List of vertices(List of 3-uplet containing the vertices coordinates).    
    Returns:
        list: List of vertices to delete from the model.
    """
    triangles_per_vertex = [[] for i in range(len(vertices))]
    for face in faces:
        for vertex in face.vertices:
            triangles_per_vertex[vertex].append(face)
    vertices_to_delete = []
    for trianglelist,vertex in enumerate(triangles_per_vertex):
        if is_cycle(trianglelist):
            #simple
            toDelete = distance_to_plane(vertex,trianglelist,deldist=0.2)
        else:
            #boundary or complexe
            type,boundaryedge = classify_vertex(vertex, trianglelist)
            if type == "boundary":
                toDelete = distance_to_edge(vertex,boundaryedge,deldist=0.1)
            elif type == "complex":
                toDelete = False
        if toDelete:
            vertices_to_delete.append(vertex)
    
    return vertices_to_delete

def distance_to_plane(vertex,triangles,deldist=0.2):
    """Return True if the vertex is close enough to the plane formed by the triangles.
    
    Args:
        vertex (list): List of 3-uplet containing the vertex coordinates.
        triangles (list): List of triangles(List of 3-uplet containing the vertices index in their list).
        deldist (float): Distance that define the close enoughness.
    Returns:
        bool: True if the vertex is close enough to the plane formed by the triangles.
    """
    normals = np.array([compute_normal(triangle) for triangle in triangles])
    
    average_normal = np.mean(normals, axis=0)
    d = -np.dot(average_normal, vertex)
    
    distance = abs(np.dot(average_normal, vertex) + d) / np.linalg.norm(average_normal)
    return distance < deldist

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
    
    return distance < deldist
    

def main():
    pass

if __name__ == "__main__":
    main()