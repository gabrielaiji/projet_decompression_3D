from objects import Vertex, Face
from coloration.dsatur import add_values_in_dict

from typing import List


def orderVertices(faces: List[Face], v_delete: Vertex) -> List[Vertex]:
    """
    Orders the vertices in a patch to
    make it easier to create the faces
    of the patch.

    :param faces: old faces to be deleted.
    :param v_delete: vertex to be deleted.
    :output: Vertices on the border of the patch
    in the order.
    """

    related_v = {}
    for i, face in enumerate(faces):
        vertices = face.getVertices()
        vertices.remove(v_delete)
        
        v0 = vertices[0]
        v1 = vertices[1]

        add_values_in_dict(related_v, v0, v1)
        add_values_in_dict(related_v, v1, v0)

        if i == 0:
            v_start = v0

    ordered_v = [v_start]
    for i in range(len(faces)-1):
        potential_next_v = related_v[ordered_v[i]]

        potential_indice = 0
        while potential_next_v[potential_indice] in ordered_v:
            potential_indice +=1
        
        ordered_v.append(potential_next_v[potential_indice])
    
    return ordered_v


    