"""from todelete import vertices_to_delete

vertices = [k for k in range(1,10)]

faces = [(1, 2, 5),
         (2, 3, 5),
         (2, 3, 4),
         (3, 4, 6),
         (4, 9, 6),
         (3, 5, 6),
         (5, 6, 7),
         (1, 5, 7),
         (1, 8, 7)]

print(vertices_to_delete(faces, vertices))"""

import obja
from io_obj.read_obj import read_obj, read_obj0, read_Mesh
from coloration.coloration import color_with_dsatur
from objects import Patch, Vertex
from mat.mat_adj import create_mat_adj
from coloration.dsatur import dsatur_modif
from io_obj.write_obj import write_mesh
from delete.todeletemaillage import getIndVerticesToDelete
from patch.create import patch_mesh



# Test coloration
"""model = obja.parse_file('../example/figure1.obj')
list_faces, list_vertices = read_obj(model)

patches = [Patch(1, [list_faces[23], list_faces[24], list_faces[35]], Vertex(1, 0, 0, 0)),
           Patch(2, [list_faces[25], list_faces[26], list_faces[2]], Vertex(1, 0, 0, 0)),
           Patch(3, [list_faces[27], list_faces[4], list_faces[5], list_faces[6]], Vertex(1, 0, 0, 0)),
           Patch(4, [list_faces[8], list_faces[9], list_faces[10]], Vertex(1, 0, 0, 0)),
           Patch(5, [list_faces[11], list_faces[12], list_faces[13]], Vertex(1, 0, 0, 0)),
           Patch(6, [list_faces[29], list_faces[30], list_faces[31]], Vertex(1, 0, 0, 0)),
           Patch(7, [list_faces[33], list_faces[32], list_faces[18], list_faces[17]], Vertex(1, 0, 0, 0)),
           Patch(8, [list_faces[20], list_faces[21], list_faces[34]], Vertex(1, 0, 0, 0)),
           Patch(9, [list_faces[36], list_faces[37], list_faces[38], list_faces[28]], Vertex(1, 0, 0, 0))]


color_with_dsatur(patches, 3)
write_obj(list_vertices, list_faces)"""



# Test trouver les sommets à supprimer
model = obja.parse_file('../example/figure1_raw.obj')
mesh = read_Mesh(model)


# Utiliser getVerticesToDelete qui renvoie directement
# les vertices s'il n'y a pas de vertices à supprimé
ind_vertices_to_delete = getIndVerticesToDelete(mesh)
print(ind_vertices_to_delete)

# Pour cet exemple, on annule la suppression des vertices sur les bords
#ind_vertices_to_delete.remove(0)
#ind_vertices_to_delete.remove(3)
"""ind_vertices_to_delete.remove(8)
ind_vertices_to_delete.remove(18)"""
print(ind_vertices_to_delete)

# Test créer les patchs
list_vertices_to_delete = mesh.getVerticesFromId(ind_vertices_to_delete)
patch_mesh(mesh, list_vertices_to_delete)

output_file = "../example/figure1_colore_exp.obj"
write_mesh(mesh, output_file)