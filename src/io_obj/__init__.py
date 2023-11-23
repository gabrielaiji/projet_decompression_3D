from entropy import getEntropyValue
from objects import Mesh, Patch, Face
from typing import List

def getColorEntropy(mesh: Mesh) -> float:
    lst_lst_patch = mesh.getPatchesIterations

    lst_patch: List[Patch]  = [patch for lst_patch in lst_lst_patch for patch in lst_patch]

    lst_lst_face = list(map(lambda p: p.getPatchFaces(), lst_patch))
    lst_face: List[Face]  = [face for lst_face in lst_lst_face for face in lst_face]

    lst_color = list(map(lambda f:f.getColor(), lst_face))

    return getEntropyValue(lst_color)
    