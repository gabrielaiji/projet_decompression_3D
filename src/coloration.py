from objects import Patch

# Ajouter une valeur dans un dictionnaire
# IN : 
# dict : Le dictionnaire en question
# key : la clé en question
# list_of_values : la liste des valeurs à attribuer au clé fourni
# OUT : le dictionnaire avec la clé key ajoutée et les nouvelles valeurs
# s'elle n'existait pas, et les nouvelles valeurs attribuées au clé s'elle
# existait déjà
def add_values_in_dict(dict, key, list_of_values):
    if key not in dict:
        dict[key] = list()
    dict[key].extend(list_of_values)
    return dict

# Colorer les patch fourni en paramètres
# IN : l_patch : la liste des patch à colorier
# OUT : result : la liste des patch avec la couleur attribuée
def colorer(l_patch: list[Patch]):
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
    result[l_patch[0].id()] = (0.5,0.5,0.5)

    # On parcours tous les patchs
    for patch in l_patch[1:]:
        #la liste des couleurs utilisées
        colors = [(0.75,0.75,0.75),(0.5,0.5,0.5),(0.25,0.25,0.25)]

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
                if len(intersection)>2:
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
        patch.setColor(colors[0])
        result[patch.id] = colors[0]

    return result