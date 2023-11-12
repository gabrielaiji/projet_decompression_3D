from objects import Mesh, Vertex
from .todelete import vertices_to_delete2, vertices_to_delete3

from typing import List


def getVerticesToDelete(maillage: Mesh) -> List[Vertex]:
    print("longueur de getfaces", len(maillage.getFaces()))
    

    ind_vertices_to_delete = vertices_to_delete3(maillage)
    ind_vertices_to_delete = list(map(lambda id:id+1, ind_vertices_to_delete))
    
    return maillage.getVerticesFromId(ind_vertices_to_delete)

def getIndVerticesToDelete(maillage: Mesh) -> List[int]:
    list_faces = maillage.getFaces()
    return vertices_to_delete2(list_faces)