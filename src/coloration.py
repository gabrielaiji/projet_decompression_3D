from objects import Patch

def add_values_in_dict(dict, key, list_of_values):
    if key not in dict:
        dict[key] = list()
    dict[key].extend(list_of_values)
    return dict

# liste des patch, liste des faces

def colorer(l_patch: list[Patch], l_face):
    result = []
    
    for face in l_face:
        result.append((face,(1,1,1)))

    dico_v = {}

    for patch in l_patch:
        vertices = patch.getVertices()
        for v in vertices:
            dico_v = add_values_in_dict(dico_v, v, patch.id())

    
    for patch in l_patch:
        