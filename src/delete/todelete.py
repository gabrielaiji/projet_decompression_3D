
import obja
import numpy as np
from collections import Counter
# import open3d as o3d

from io_obj.read_obj import read_obj,read_obj0


def get_edges(face):
    """Return edges from a given face."""
    return [(face[0], face[1]), (face[1], face[2]), (face[0], face[2])]

def compute_normal(triangle,vertices):
    """Compute the normal of a triangle."""
    v1 = np.array(vertices[triangle[1]]) - np.array(vertices[triangle[0]])
    v2 = np.array(vertices[triangle[2]]) - np.array(vertices[triangle[0]])
    """print("v1 : ", v1)
    print("v2 : ", v2)
    print("triange[2] : ", triangle[2])
    print("vertices[triangle[2]-1] : ", vertices[triangle[2]-1])"""
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
    bound=False
    for edge, count in edge_counts.items():
        if vertex in edge and count == 1:
            boundary_edge.append(edge) #probleme ici, il faut bien définir le boundary edge
            bound = True
    if bound:
        flv = [v for edge in boundary_edge for v in edge]
        vertex_counts = Counter(flv)
        new_edge = [vertex for vertex, count in vertex_counts.items() if count == 1]
        return "boundary",new_edge
        
    #rajouter classification corner, qu'il ne faudra pas supprrimer
    
    #rajouter classification interior edge, qu'il faudra evaluer avec distance to edge 
    """If the dihedral angle between two
    adjacent triangles is greater than a specified feature angle,
    then a feature edge exists"""
    
    #les deux sont des cas particulier de vertex simple (vertex qui vérifie iscycle)
        
    return "unclassified", None

def is_cycle(triangles):
    """Check if the triangles form a cycle around the vertex."""
    if len(triangles) == 0:
        return False
    if len(triangles) == 1:
         return dumb_cycle(triangles)
    else:
        return (dumb_cycle(triangles) and dumb_cycle(triangles, triangles[1]))
     #Il faudrait refaire le parcour en partant d'un autre triangle de l'ensemble de triangle et vérifier que les taille sont égale
     #C'est fait, à tester

def dumb_cycle(triangles,start_triangle=None):
    #print("triangles : ", triangles)
    visited_triangles = set()
    if start_triangle is None:
        start_triangle = set(triangles[0])
    else:
        start_triangle = set(start_triangle)
    current_triangle = start_triangle
    
    count = 0

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
        if count > 15:
            return False
        count += 1
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
            #print("C'est l'indice du vertex : ", str(vertex)+ " or la liste est de taille(nombre de vertex) : ", str(len(triangles_per_vertex)))
            
            triangles_per_vertex[vertex].append(face)
    vertices_to_delete = []
    for vertex,trianglelist in enumerate(triangles_per_vertex):
        edges = [get_edges(triangle) for triangle in trianglelist]
        flat_edges = [edge for triangle_edges in edges for edge in triangle_edges]
        edge_lengths = [np.linalg.norm(np.array(edge[1]) - np.array(edge[0])) for edge in flat_edges]
        mean_edge_length = np.mean(edge_lengths)
        #print("mean_edge_length : ", mean_edge_length)
        #print("Trianglelist est : ", trianglelist)
        #print("Vertex est : ", vertex)
        if len(trianglelist) == 0:
            toDelete = True
        elif is_cycle(trianglelist):
            #print("cycle")
            #simple
            toDelete = distance_to_plane(vertex,trianglelist,vertices,deldist=0.001,edgelmoy=mean_edge_length)
        else:
            #boundary or complexe
            #print("pas de cycle")
            type,boundaryedge = classify_vertex(vertex, trianglelist)
            if type == "boundary":
                toDelete = distance_to_edge(vertices,vertex,boundaryedge,deldist=0.01,edgelmoy=mean_edge_length)
                
            elif type == "complex" or "unclassified":
                toDelete = False
        """print("juste anvant le if, vertex est : ", vertex)
        print("juste avant le if, toDelete est : ", toDelete)"""
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

def distance_to_plane(vertex,triangles,vertices,deldist=0.2,edgelmoy=1):
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
    print("Norm: ", norm)"""
    """print("Average normal: ", average_normal)
    print("Vertex: ", vertices[vertex])
    print("Dot product: ", dot_product)
    print("norm: ", norm)
    print("Distance to plane: ", distance)
    """
    return (distance/edgelmoy < deldist) #conditionner la distance par la moyenne des longueurs des edge du vertex, ça marchera mieux (pas besoin de changer de thershold pour chaque mesh)

def distance_to_edge(vertices,vertex,boundaryedge,deldist=0.1,edgelmoy=1):
    """Return True if the vertex is close enough to the edge formed by the triangles.
    
    Args:
        vertices (list): List of 3-uplet containing the vertices coordinates.
        vertex (list): List of 3-uplet containing the vertex coordinates.
        boundaryedge (list): List of 2-uplet containing the vertices index in their list.
        deldist (float): Distance that define the close enoughness.
    Returns:
        bool: True if the vertex is close enough to the edge formed by the triangles.
    """
    if boundaryedge and len(boundaryedge) == 2 and boundaryedge is not None:
        A = np.array(vertices[boundaryedge[0]])
        B = np.array(vertices[boundaryedge[1]])
        #print("vertex : ", vertices[vertex])
        AP = np.array(vertices[vertex]) - A
        AB = B - A
        magnitude_AB = np.linalg.norm(AB)
        #print("Magnitude AB : ", magnitude_AB)
        #print("Magnitude AP : ", np.linalg.norm(AP))
        projection = np.dot(AP, AB) / magnitude_AB
        
        #print("Projection : ", projection)
        if projection < 0:
            distance = np.linalg.norm(AP)
        elif projection > 1:
            distance = np.linalg.norm(np.array(vertex) - B)
        else:
            distance = np.linalg.norm(AP - projection * (AB / magnitude_AB))
        
        #print("Distance to edge : ", distance)
        return (distance/edgelmoy < deldist)
    else:
        return False
    


def add_1_to_list_id_vertices(id_vertices):
    for i in range(len(id_vertices)):
        id_vertices[i] += 1
    
    return id_vertices



def vertices_to_delete2(faces):
    """Return a list of vertices to delete from the model.
    
    Args:
        faces (list): List of faces(List Face object).    
    Returns:
        list: List of vertices to delete from the model.
    """

    all_vertices = {vertex.id(): vertex.getCoords() for face in faces for vertex in face.getVertices()}
    faceslist = [face.getVertexIds() for face in faces]
    range = max([max(face) for face in faceslist])
    verticeslist = [0]*(range)
    for id,vertex in all_vertices.items():
        print("on est dans vertices_to_delete2 et on a id et vertex : ", id, vertex)
        verticeslist[id] = vertex


    vertices_to_del = vertices_to_delete(faceslist, verticeslist)

    print("On a supprimé " + str(len(vertices_to_del)/len(np.asarray(verticeslist))*100) + "% des sommets du maillage")

    return vertices_to_del

def vertices_to_delete3(maillage):
    """Return a list of vertices to delete from the model.
    
    Args:
        maillage (Mesh): Mesh object.    
    Returns:
        list: List of vertices to delete from the model.
    """

    
    faceslist = [face.getVertexIds() for face in maillage.getFaces()]
    range = max([max(face) for face in faceslist])
    verticeslist = [0]*(range+1)
    for vertex in sorted(maillage.getVertices(), key=lambda vertex: vertex.id()):
        #print("Sachant que range est : ", range)
        #print("on est dans vertices_to_delete3 et on a vertex.id() et vertex.getCoords() : ", vertex.id(), vertex.getCoords())
        if vertex.id() <= range:
            verticeslist[vertex.id()] = vertex.getCoords()

    vertices_to_del = vertices_to_delete(faceslist, verticeslist)

    
    try:
        print("On a supprimé " + str(len(vertices_to_del)/len(np.asarray(verticeslist))*100) + "% des sommets du maillage")
    except:
        try:
            print("On a supprimé " + str(len(vertices_to_del)/len((verticeslist))*100) + "% des sommets du maillage")
        except Exception as e:
            print("Problème de print du '%' suppr, exception : ", e)

    return vertices_to_del


def main():
    faces,_ = read_obj0(obja.parse_file('example/suzanne.obj'))
    delverts = vertices_to_delete2(faces)
    print(delverts)

if __name__ == "__main__":
    main()