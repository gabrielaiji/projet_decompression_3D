from objects import Vertex, Face, Patch, Mesh
from .order_vertices import orderVertices
from coloration.coloration import color_with_dsatur

from typing import List, Tuple

def patch_mesh(mesh: Mesh, list_vertices_to_delete: List[Vertex]):
    id_f_start = mesh.getFaceNextId()


    lst_patches, lst_v_restore, set_f_restore = create_all_patches(list_vertices_to_delete, id_f_start)
    color_with_dsatur(lst_patches, 3)

    lst_new_faces = [face for sublist in\
                     list(map(lambda patch: patch.getPatchFaces(), lst_patches))\
                        for face in sublist]
    
    lst_deleted_faces = [face for sublist in\
                            list(map(lambda patch: patch.getDeletedFaces(), lst_patches))\
                            for face in sublist]

    mesh.removeFaces(lst_deleted_faces, set_f_restore)
    mesh.addFaces(lst_new_faces)
    mesh.removeVertices(list_vertices_to_delete, lst_v_restore)
    mesh.addPatchIteration(lst_patches)

    

def create_all_patches(list_vertices_to_delete: List[Vertex], id_f_start: int)\
    -> Tuple[List[Patch], List[Vertex], List[Face]]:

    lst_patches = []
    lst_vertices_to_restore = []
    set_faces_to_restore = set()
    for v_to_be_deleted in list_vertices_to_delete:
        old_faces = v_to_be_deleted.getFaces()
        ordered_v = orderVertices(old_faces, v_to_be_deleted)

        new_faces_local, id_f_start = create_z_simple(ordered_v, id_f_start)
        if new_faces_local == []:
            lst_vertices_to_restore.append(v_to_be_deleted)
            set_faces_to_restore = set_faces_to_restore.union(old_faces)
        else:
            patch_id = len(lst_patches) + 1
            patch = Patch(patch_id, old_faces, new_faces_local, v_to_be_deleted)

            lst_patches.append(patch)


    return lst_patches, lst_vertices_to_restore, set_faces_to_restore


def create_z_simple(liste_vertices: List[Vertex], id_f_start: int):
    if len(liste_vertices) < 5:
        return [], id_f_start

    result: list[Face] = []

    n = len(liste_vertices)

    # Ajouter le face tout en haut
    result.append(Face(id_f_start, [liste_vertices[0],liste_vertices[1],liste_vertices[2]]))
    id_f_start +=1

    if n%2 == 0:
        # Ajouter le face tout en bas
        result.append(Face(id_f_start,[liste_vertices[n//2],liste_vertices[1+n//2],liste_vertices[2+n//2]]))
        id_f_start +=1

        # le nombre des faces de chaque côté
        nb_f_cote = (n-2-2)/2
    else:
        # le nombre des faces de chaque côté
        nb_f_cote = (n-2-1)/2

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