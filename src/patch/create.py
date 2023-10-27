from objects import Vertex, Face, Patch
from .order_vertices import orderVertices



def create_all_patches(list_vertices_to_delete: list[Vertex], id_f_start: int)\
    -> tuple[dict[int, dict[str, list[Face]|Patch]], list[Patch]]:

    patches = {}
    lst_patches = []
    for v_to_be_deleted in list_vertices_to_delete:
        old_faces = v_to_be_deleted.getFaces()
        ordered_v = orderVertices(old_faces, v_to_be_deleted)

        new_faces_local, id_f_start = create_z_simple(ordered_v, id_f_start)
        patch_id = len(lst_patches) + 1
        patch = Patch(patch_id, new_faces_local, v_to_be_deleted)

        patches[patch_id] = {"old_faces": old_faces, "new_faces":new_faces_local, "patch":patch}
        lst_patches.append(patch)


    return patches, lst_patches


def create_z_simple(liste_vertices: list[Vertex], id_f_start: int):

    result: list[Face] = []

    n = len(liste_vertices)

    # Ajouter le face tout en haut
    result.append(Face(id_f_start, [liste_vertices[0],liste_vertices[1],liste_vertices[2]]))
    id_f_start +=1
    # Ajouter le face tout en bas
    result.append(Face(id_f_start,[liste_vertices[n-1],liste_vertices[n-2],liste_vertices[n-3]]))
    id_f_start +=1

    # le nombre des faces de chaque côté
    nb_f_cote = (n-2-2)/2

    # On ajoute les faces dont 2 vertices sont à gauche
    i = 0
    j = 2
    compteur = 0
    while compteur<nb_f_cote:
        result.append(Face(id_f_start, [liste_vertices[i%n],liste_vertices[j],liste_vertices[(i-1)%n]]))
        id_f_start +=1
        compteur += 1
        i -= 1
        j += 1

    # On ajoute les faces dont 2 vertices sont à droit
    i = 2
    j = n-1
    compteur = 0
    while compteur<nb_f_cote:
        result.append(Face(id_f_start, [liste_vertices[i],liste_vertices[j],liste_vertices[i+1]]))
        id_f_start +=1
        compteur += 1
        i += 1
        j -= 1

    return result, id_f_start