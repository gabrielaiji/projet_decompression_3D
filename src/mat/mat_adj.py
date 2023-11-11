import numpy as np
from objects import Patch

from typing import List

# Ajouter une valeur dans un dictionnaire
# IN : 
# dict : Le dictionnaire en question
# key : la clé en question
# value_to_add : la valeur à attribuer au clé fourni
# OUT : le dictionnaire avec la clé key ajoutée et les nouvelles valeurs
# s'elle n'existait pas, et les nouvelles valeurs attribuées au clé s'elle
# existait déjà
def add_values_in_dict(dict, key, value_to_add):
    if key not in dict:
        dict[key] = list()
    dict[key].append(value_to_add)
    return dict


def create_mat_adj(l_patch: List[Patch]):

    nb_sommets = len(l_patch)
    mat_adj = np.zeros((nb_sommets, nb_sommets), dtype=int)

    # On crée 2 dicos, un qui lie les vertices au patchs (dico_v_patch) et l'autre qui lie les patchs au vertices (dico_patch_v)
    dico_v_patch = {}
    dico_patch_v = {}

    for patch in l_patch:
        vertices = patch.getVertices()
        for v in vertices:
            dico_v_patch = add_values_in_dict(dico_v_patch, v.id(), patch.id())
            dico_patch_v = add_values_in_dict(dico_patch_v,patch.id(),v.id())

    # On parcours tous les patchs
    for patch in l_patch[1:]:

        # On prends les vertices associés à notre patch et on parcous les patchs associés à ces vertices
        id_vertices = dico_patch_v[patch.id()]
        for id in id_vertices:
            id_patches = dico_v_patch[id]
            for id_patch in id_patches:

                # On voit combien il y a de vertex en commun avec notre patch et le patch en question
                id_vertices_neighbor = dico_patch_v[id_patch]
                ens1 = set(id_vertices)
                ens2 = set(id_vertices_neighbor)
                intersection = ens1 & ens2

                # S'ils ont 2 vertices en commun
                if len(intersection)==2:
                    # Alors les 2 patches sont adjacents et on le signale dans la matrice d'adjacence
                    mat_adj[patch.id()-1, id_patch-1] = 1
                    mat_adj[id_patch-1, patch.id()-1] = 1

    return mat_adj