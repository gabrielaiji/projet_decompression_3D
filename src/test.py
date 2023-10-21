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
from convert_obj_to_list_faces import convert_obj_to_list_faces
from coloration import colorer
from objects import Patch, Vertex
from mat_adj import create_mat_adj
from dsatur import dsatur_modif
from coloration_to_obj import coloration_to_obj

model = obja.parse_file('../example/figure1_colore.obj')
list_faces = convert_obj_to_list_faces(model)
list_faces = list_faces

patches = [Patch(1, [list_faces[23], list_faces[24], list_faces[35]], Vertex(1, 0, 0, 0)),
           Patch(2, [list_faces[25], list_faces[26], list_faces[2]], Vertex(1, 0, 0, 0)),
           Patch(3, [list_faces[27], list_faces[4], list_faces[5], list_faces[6]], Vertex(1, 0, 0, 0)),
           Patch(4, [list_faces[8], list_faces[9], list_faces[10]], Vertex(1, 0, 0, 0)),
           Patch(5, [list_faces[11], list_faces[12], list_faces[13]], Vertex(1, 0, 0, 0)),
           Patch(6, [list_faces[29], list_faces[30], list_faces[31]], Vertex(1, 0, 0, 0)),
           Patch(7, [list_faces[32], list_faces[32], list_faces[18], list_faces[17]], Vertex(1, 0, 0, 0)),
           Patch(8, [list_faces[20], list_faces[21], list_faces[34]], Vertex(1, 0, 0, 0)),
           Patch(9, [list_faces[36], list_faces[37], list_faces[38], list_faces[28]], Vertex(1, 0, 0, 0))]


couleurs = colorer(patches)
for patch_id in couleurs:
    couleur = couleurs[patch_id]
    print("patch {} : {}".format(patch_id, couleur))



mat_adj = create_mat_adj(patches)
print(mat_adj)



list_num_color = dsatur_modif(mat_adj, 3)
print(list_num_color)



# coloration_to_obj()