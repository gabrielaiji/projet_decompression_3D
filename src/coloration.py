# liste des patch, liste des faces

def colorer(l_patch, l_face):
    result = []
    
    for face in l_face:
        result.append((face,(1,1,1)))

    dico_v = {}

    for patch in l_patch:
        