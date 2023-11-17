from objects import Vertex, Face, Patch, Mesh
from .order_vertices import orderVertices
from coloration.coloration import color_with_dsatur
from copy import copy

from typing import List, Tuple

def patch_mesh(mesh: Mesh, list_vertices_to_delete: List[Vertex]):
    id_f_start = mesh.getFaceNextId()

    print("\t\tflag 0 patch")

    lst_patches, nb_v_restored = create_all_patches(list_vertices_to_delete, id_f_start)

    nb_deleted_faces_in_patches = 0
    nb_added_faces_by_patches = 0
    for patch in lst_patches:
        nb_deleted_faces_in_patches += len(patch.getDeletedFaces())
        nb_added_faces_by_patches += len(patch.getPatchFaces())
    print("\t\tNb patches: ", str(len(lst_patches)))
    print("\t\tNb to be deleted faces : ", str(nb_deleted_faces_in_patches))
    print("\t\tNb to be added faces : ", str(nb_added_faces_by_patches))
    print("\t\tNb Vertices restore due to vertex degree : ", str(nb_v_restored))

    print("\n\t\tflag 1 patch")
    set_v_restore, set_f_restore = color_with_dsatur(lst_patches, 3)

    nb_deleted_faces_in_patches = 0
    nb_added_faces_by_patches = 0
    for patch in lst_patches:
        nb_deleted_faces_in_patches += len(patch.getDeletedFaces())
        nb_added_faces_by_patches += len(patch.getPatchFaces())
    print("\t\tNb patches: ", str(len(lst_patches)))
    print("\t\tNb to be deleted faces : ", str(nb_deleted_faces_in_patches))
    print("\t\tNb to be added faces : ", str(nb_added_faces_by_patches))
    print("\t\tNb Vertices restore due to coloration : ", str(len(set_v_restore)))
    print("\t\tNb Faces restore due to coloration : ", str(len(set_f_restore)))

    print("\n\t\tflag 2 patch")

    lst_new_faces = [face for sublist in\
                     list(map(lambda patch: patch.getPatchFaces(), lst_patches))\
                        for face in sublist]
    
    lst_deleted_faces = [face for sublist in\
                            list(map(lambda patch: patch.getDeletedFaces(), lst_patches))\
                            for face in sublist]
    
    list_vertices_to_delete = list(map(lambda patch: patch.getDeletedVertex(), lst_patches))

    #print("\t\t\tAvant delete, on a ", str(len(mesh.getFaces())), " faces")
    #print("\t\t\tAvant delete, on a ", str(len(mesh.getVertices())), " vertices")

    print("\t\tflag 3 patch")
    print("\t\tDeleted Vertices nb : ", str(len(list_vertices_to_delete)))
    print("\t\tDeleted faces nb : ", str(len(lst_deleted_faces)))
    print("\t\tNew faces nb : ", str(len(lst_new_faces)))

    # mesh.removeVertices(list_vertices_to_delete)
    #mesh.addVertices(list(set_v_restore))
    # mesh.removeFaces(lst_deleted_faces)
    # mesh.addFaces(lst_new_faces)
    # mesh.addPatchIteration(lst_patches)
    mesh.applyCompression(lst_patches)
    faces_ids = list(map(lambda f:f.id()+1,  mesh.getFaces()))
    print("final faces: {}".format(faces_ids))

    #print("\t\t\tAprès delete, on a ", str(len(mesh.getFaces())), " faces")
    #print("\t\t\tAprès delete, on a ", str(len(mesh.getVertices())), " vertices")
    return mesh


    

def create_all_patches(list_vertices_to_delete: List[Vertex], id_f_start: int)\
    -> Tuple[List[Patch], List[Vertex], List[Face]]:

    lst_patches = []
    nb_v_restored = 0
    for v_to_be_deleted in list_vertices_to_delete:
        old_faces = v_to_be_deleted.getFaces()
        ordered_v = orderVertices(old_faces, v_to_be_deleted)

        new_faces_local, id_f_start = create_z_simple(ordered_v, id_f_start)
        if new_faces_local != []:
            patch_id = len(lst_patches) + 1
            patch = Patch(patch_id, old_faces, new_faces_local, v_to_be_deleted)

            lst_patches.append(patch)
        else:
            nb_v_restored += 1


    return lst_patches, nb_v_restored


def create_z_simple(liste_vertices: List[Vertex], id_f_start: int):
    result: list[Face] = []

    if len(liste_vertices) == 4:
        result.append(Face(id_f_start, [liste_vertices[0],liste_vertices[1],liste_vertices[2]]))
        id_f_start += 1
        result.append(Face(id_f_start, [liste_vertices[0],liste_vertices[2],liste_vertices[3]]))
        id_f_start += 1
        return result, id_f_start

    if len(liste_vertices) < 3:
        return [], id_f_start

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