from objects import Mesh, Vertex
from .todelete import vertices_to_delete2, vertices_to_delete3

from typing import List


def getVerticesToDelete(maillage: Mesh, delete_distance: float) -> List[Vertex]:
    print("longueur de getfaces", len(maillage.getFaces()))
    

    ind_vertices_to_delete = vertices_to_delete3(maillage, delete_distance)
    ind_vertices_to_delete = list(map(lambda id:id, ind_vertices_to_delete))
    
    return maillage.getVerticesFromId(ind_vertices_to_delete)

def getIndVerticesToDelete(maillage: Mesh) -> List[int]:
    list_faces = maillage.getFaces()
    return vertices_to_delete2(list_faces)

def getDelete_distance(maillage: Mesh) ->float:
    nb_original_v = len(maillage.getVertices())

    delete_distance = 0.001

    nb_v_choisi = len(getVerticesToDelete(maillage, delete_distance))
    taux_choisi = nb_v_choisi /  nb_original_v
    taux_min = 0.2

    while taux_choisi < 0.2:
        delete_distance *= (taux_min/taux_choisi)*1.5
        nb_v_choisi = len(getVerticesToDelete(maillage, delete_distance))
        taux_choisi = nb_v_choisi /  nb_original_v

    return delete_distance