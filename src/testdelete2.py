import numpy as np
import open3d as o3d
from delete.todelete import vertices_to_delete

def test_vertices_to_delete(mesh):
    # Extraire les faces et les vertices du mesh
    faces = np.asarray(mesh.triangles)
    vertices = np.asarray(mesh.vertices)

    # Appliquer votre fonction pour obtenir les vertices à supprimer
    vertices_to_del = vertices_to_delete(faces, vertices)

    # Colorer les sommets sélectionnés en rouge
    colors = np.zeros_like(vertices)  # Initialement, tous les vertices sont colorés en noir
    for v in vertices_to_del:
        colors[v] = [1, 0, 0]  # Rouge

    # Mettre à jour les couleurs du mesh et l'afficher
    mesh.vertex_colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([mesh])

if __name__ == "__main__":
    # Charger le mesh spécifié
    mesh = o3d.io.read_triangle_mesh('../example/bunny.obj')
    mesh.compute_vertex_normals()

    # Exécuter la fonction de test
    test_vertices_to_delete(mesh)