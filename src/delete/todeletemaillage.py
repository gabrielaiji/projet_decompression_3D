from objects import Mesh, Vertex
from .todelete import vertices_to_delete2

from typing import List


def getVerticesToDelete(maillage: Mesh) -> List[Vertex]:
    list_faces = maillage.getFaces()
    ind_vertices_to_delete = vertices_to_delete2(list_faces)
    
    return maillage.getVerticesFromId(ind_vertices_to_delete)

def getIndVerticesToDelete(maillage: Mesh) -> List[int]:
    list_faces = maillage.getFaces()
    return vertices_to_delete2(list_faces)