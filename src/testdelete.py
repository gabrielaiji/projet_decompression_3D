import open3d as o3d
import numpy as np
from todelete import vertices_to_delete,vertices_to_delete2

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
    """print("delverts[0] : ", delverts[0])
    print("delverts[1] : ", delverts[1])
    print("delverts[2] : ", delverts[2])
    print("vertice de delverts[0]  : ", vertices[delverts[0]])
    print("vertice de delverts[1]  : ", vertices[delverts[1]])
    print("vertice de delverts[2]  : ", vertices[delverts[2]])"""
    vertex_colors = np.ones((len(np.asarray(mesh.vertices)), 3)) * [0, 1, 0]  # Vert par défaut

    # Changer la couleur des sommets qui doivent être supprimés en rouge
    vertex_colors[delverts] = [1, 0, 0]  # Rouge pour les sommets à supprimer

    mesh.vertex_colors = o3d.utility.Vector3dVector(vertex_colors)

    # Extraire les arêtes du maillage
    edges = np.asarray(mesh.triangles).reshape(-1, 3)
    lines = [[edges[i, 0], edges[i, 1]] for i in range(edges.shape[0])] + \
            [[edges[i, 1], edges[i, 2]] for i in range(edges.shape[0])] + \
            [[edges[i, 2], edges[i, 0]] for i in range(edges.shape[0])]

    # Créer un LineSet à partir des arêtes
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(np.asarray(mesh.vertices)),
        lines=o3d.utility.Vector2iVector(lines),
    )

    # Définir la couleur des lignes (par exemple, bleu)
    line_colors = np.ones((len(lines), 3)) * [0, 0, 1]
    line_set.colors = o3d.utility.Vector3dVector(line_colors)

    print("On a supprimé " + str(len(delverts)/len(np.asarray(mesh.vertices))*100) + "% des sommets du maillage")

    # Visualiser à la fois le maillage triangulaire et le wireframe
    o3d.visualization.draw_geometries([mesh, line_set])
    o3d.io.write_triangle_mesh("mon_maillage.ply", mesh)
    
    
if __name__ == "__main__":
    test()