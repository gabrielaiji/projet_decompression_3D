
import obja
import numpy as np
import open3d as o3d

from convert_obj_to_list_faces import read_obj


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
        
        # Find a neighboring triangle
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

    # Check if all triangles have been visited
    return len(visited_triangles) == len(triangles)



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
            #print("On cycle")
            toDelete = False#distance_to_plane(vertex,trianglelist,vertices,deldist=1)
        else:
            print("On cycle pas")
            #boundary or complexe
            type,boundaryedge = classify_vertex(vertex, trianglelist)
            if type == "boundary":
                print("On est sur un boundary")
                toDelete = distance_to_edge(vertex,boundaryedge,deldist=10)
            elif type == "complex" or "unclassified":
                toDelete = False
        if toDelete and not (vertex in forbidden_vertices):
            vertices_to_delete.append(vertex)
            forbidden_vertices.add(vertex)  # Add the current vertex to forbidden_vertices
            # Add adjacent vertices of the deleted vertex to the forbidden set
            """print("trianglelist : ", trianglelist)
            print("vertex : ", vertex)"""
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
    
    print("Distance to edge : ", distance)
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

def test():
    
    """addedvert = []
    with open('example/suzanne.obja', 'w') as output:
        output_model = obja.Output(output, random_color=False)
        for i,face in enumerate(faceslist):
            verts = [verticeslist[face[0]-1],verticeslist[face[1]-1],verticeslist[face[2]-1]]
            #print("verts[0] : ", verts[0])
            if face[0] not in addedvert:
                output_model.add_vertex(face[0], verts[0])
                addedvert.append(face[0])
            if face[1] not in addedvert:
                output_model.add_vertex(face[1], verts[1])
                addedvert.append(face[1])
            if face[2] not in addedvert:
                output_model.add_vertex(face[2], verts[2])
                addedvert.append(face[2])
            
            f = obja.Face(face[0],face[1],face[2])
            if face[0] == face[1] or face[0] == face[2] or face[1] == face[2]:
                print(("C EGAL"))
            output_model.add_face(i, f)"""
    """faces,_ = read_obj(obja.parse_file('example/suzanne.obj'))
    all_vertices = {vertex.id(): vertex.getCoords() for face in faces for vertex in face.getVertices()}
    faceslist = [face.getVertexIds() for face in faces]
    verticeslist = [coords for _, coords in sorted(all_vertices.items())]
    delverts = vertices_to_delete2(faces)
    #print("Nombre de sommets à supprimer : ", len(delverts))
    #APRES ICI : 
    with open('example/suzanne.obja', 'w') as output:
        output_model = obja.Output(output, random_color=True)
        editedfaces = []
        deletedfaces = []
        addedvert = []
        for face in faceslist:
            if any (vertex in delverts for vertex in face):
                deletedfaces.append(face)
            else:
                editedfaces.append(face)
        for face in editedfaces:
            verts = [verticeslist[face[0]-1],verticeslist[face[1]-1],verticeslist[face[2]-1]]
            #print("verts[0] : ", verts[0])
            if face[0] not in addedvert:
                output_model.add_vertex(face[0], verts[0])
                addedvert.append(face[0])
            if face[1] not in addedvert:
                output_model.add_vertex(face[1], verts[1])
                addedvert.append(face[1])
            if face[2] not in addedvert:
                output_model.add_vertex(face[2], verts[2])
                addedvert.append(face[2])
            f = obja.Face(face[0],face[1],face[2])
            output_model.add_face(0, f)
        for i,face in enumerate(deletedfaces):
            verts = [verticeslist[face[0]-1],verticeslist[face[1]-1],verticeslist[face[2]-1]]
            #print("verts[0] : ", verts[0])
            if face[0] not in addedvert:
                output_model.add_vertex(face[0], verts[0])
                addedvert.append(face[0])
            if face[1] not in addedvert:
                output_model.add_vertex(face[1], verts[1])
                addedvert.append(face[1])
            if face[2] not in addedvert:
                output_model.add_vertex(face[2], verts[2])
                addedvert.append(face[2])
            f = obja.Face(face[0],face[1],face[2])
            output_model.add_face(i, f)"""
    mesh = o3d.io.read_triangle_mesh('example/bunny.obj')
    # Transformer le mesh en numpy arrays pour faciliter les manipulations
    vertices = np.asarray(mesh.vertices)
    triangles = np.asarray(mesh.triangles)
    delverts = vertices_to_delete(triangles,vertices)
    print("delverts[0] : ", delverts[0])
    print("delverts[1] : ", delverts[1])
    print("delverts[2] : ", delverts[2])
    print("vertice de delverts[0]  : ", vertices[delverts[0]])
    print("vertice de delverts[1]  : ", vertices[delverts[1]])
    print("vertice de delverts[2]  : ", vertices[delverts[2]])
    vertex_colors = np.ones((len(np.asarray(mesh.vertices)), 3)) * [0, 1, 0]  # Vert par défaut

    # Changer la couleur des sommets qui doivent être supprimés en rouge
    vertex_colors[delverts] = [1, 0, 0]  # Rouge pour les sommets à supprimer

    mesh.vertex_colors = o3d.utility.Vector3dVector(vertex_colors)

    edges = np.asarray(mesh.triangles).reshape(-1, 3)
    lines = [[edges[i, 0], edges[i, 1]] for i in range(edges.shape[0])] + \
            [[edges[i, 1], edges[i, 2]] for i in range(edges.shape[0])] + \
            [[edges[i, 2], edges[i, 0]] for i in range(edges.shape[0])]


    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(np.asarray(mesh.vertices)),
        lines=o3d.utility.Vector2iVector(lines),
    )


    line_colors = np.ones((len(lines), 3)) * [0, 0, 1]
    line_set.colors = o3d.utility.Vector3dVector(line_colors)

    o3d.visualization.draw_geometries([mesh, line_set])
    o3d.io.write_triangle_mesh("mon_maillage.ply", mesh)


def main():
    test()

if __name__ == "__main__":
    main()