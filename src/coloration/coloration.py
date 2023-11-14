from objects import Patch
from mat.mat_adj import create_mat_adj
from .dsatur import dsatur_modif
from copy import copy

from typing import List

couleurs = [(1., 0., 0.), (0., 1., 0.), (1., 1., 0.)]

def color_with_dsatur(l_patch: List[Patch], nb_color):
    """
    Colors the patches, and the faces according to
    the DSATUR (modified) algorithm.
    """
    adjacency_mat = create_mat_adj(l_patch)
    pacthes_colors = dsatur_modif(adjacency_mat, nb_color)

    lst_v_restore = []
    set_f_restore = set()

    
    for patch in copy(l_patch):
        color = pacthes_colors[patch.id()-1]
        if color is None:
            lst_v_restore.append(patch.getDeletedVertex())
            set_add_f_restore = set(patch.getDeletedFaces())
            set_f_restore = set_f_restore.union(set_add_f_restore)
            l_patch.remove(patch)
        else:
            patch.setColor(couleurs[color])
    
    return lst_v_restore, set_f_restore

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

# Colorer les patch fourni en paramètres
# IN : l_patch : la liste des patch à colorier
# OUT : result : la liste des patch avec la couleur attribuée
def colorer(l_patch: List[Patch]):
    result = {}

    # On crée 2 dicos, un qui lie les vertices au patchs (dico_v_patch) et l'autre qui lie les patchs au vertices (dico_patch_v)
    dico_v_patch = {}
    dico_patch_v = {}

    for patch in l_patch:
        vertices = patch.getVertices()
        for v in vertices:
            dico_v_patch = add_values_in_dict(dico_v_patch, v.id(), patch.id())
            dico_patch_v = add_values_in_dict(dico_patch_v,patch.id(),v.id())

    # On colorie le premier patch
    result[l_patch[0].id()] = couleurs[1]

    # On parcours tous les patchs
    for patch in l_patch[1:]:
        #la liste des couleurs utilisées
        colors = couleurs.copy()

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
                    # On voit est-ce qu'il y a une couleur déjà attribuée à ce patch
                    if id_patch in result:
                        color = result[id_patch]
                        # S'elle existe, on l'enlève de notre liste de couleurs possible pour ce patch
                        # il faut qd mm tester est-ce que la couleur existe parce que ça peut
                        # arriver que le patch soit au milieu de plusieurs patchs et on va 
                        # enlever la même couleur plusieurs fois
                        if color in colors:
                            colors.remove(color)

        # On attribue à notre patch une couleur possible
        if colors == []:
            colors = couleurs.copy()
        patch.setColor(colors[0])
        result[patch.id()] = colors[0]

    return result