from objects import Vertex, Face, Patch, Mesh
from .order_vertices import orderVertices
from coloration.coloration import color_with_dsatur
from copy import copy

from typing import List, Tuple

def patch_mesh(mesh: Mesh, list_vertices_to_delete: List[Vertex]):
    id_f_start = mesh.getFaceNextId()

    print("\t\tflag 0 patch : Patches creation")

    lst_patches, nb_v_restored = create_all_patches(list_vertices_to_delete, id_f_start)

    print("\n\t\tflag 1 patch : Coloration")
    lst_patches = color_with_dsatur(lst_patches, 3)
    
    print("\n\t\tflag 2 patch : Compression Application")
    #list_vertices_to_delete = list(map(lambda patch: patch.getDeletedVertex(), lst_patches))

    mesh.applyCompression(lst_patches)

    return mesh


    

def create_all_patches(list_vertices_to_delete: List[Vertex], id_f_start: int)\
    -> Tuple[List[Patch], List[Vertex], List[Face]]:

    lst_patches = []
    nb_v_restored = 0
    for v_to_be_deleted in list_vertices_to_delete:
        old_faces = v_to_be_deleted.getFaces()
        ordered_v = orderVertices(old_faces, v_to_be_deleted)
        if ordered_v != []:

            new_faces_local, id_f_start = create_z_simple(ordered_v, id_f_start)
            if new_faces_local != []:
                patch_id = len(lst_patches) + 1
                patch = Patch(patch_id, old_faces, new_faces_local, v_to_be_deleted)

                lst_patches.append(patch)
            else:
                nb_v_restored += 1
        else:
            nb_v_restored += 1


    return lst_patches, nb_v_restored


def create_z_simple(liste_vertices: List[Vertex], id_f_start: int):
    result: list[Face] = []
    n = len(liste_vertices)
    if n < 3:
        return [], id_f_start

    if n == 4:
        result.append(Face(id_f_start, [liste_vertices[0],liste_vertices[1],liste_vertices[2]]))
        id_f_start += 1
        result.append(Face(id_f_start, [liste_vertices[0],liste_vertices[2],liste_vertices[3]]))
        id_f_start += 1
        return result, id_f_start



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
        result.append(Face(id_f_start, [liste_vertices[i],liste_vertices[i+1],liste_vertices[j]]))
        id_f_start +=1
        compteur += 1
        i += 1
        j -= 1
    return result, id_f_start