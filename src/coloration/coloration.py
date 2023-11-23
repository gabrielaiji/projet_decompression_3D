from objects import Patch
from mat.mat_adj import create_mat_adj
from .dsatur import dsatur_modif, dsatur_modif2
from copy import copy

from typing import List

def color_with_dsatur(l_patch: List[Patch], nb_color):
    """
    Colors the patches, and the faces according to
    the DSATUR (modified) algorithm.
    """
    adjacency_mat = create_mat_adj(l_patch)
    pacthes_colors = dsatur_modif2(adjacency_mat, nb_color)

    set_v_restore = set()
    set_f_restore = set()

    
    for patch in copy(l_patch):
        color = pacthes_colors[patch.id()-1]
        if color == -1:
            set_v_restore.add(patch.getDeletedVertex())

            set_add_f_restore = set(patch.getDeletedFaces())
            set_f_restore = set_f_restore.union(set_add_f_restore)
            #patch.delete()
            l_patch.remove(patch)
        else:
            patch.setColor(color)
    
    return l_patch

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