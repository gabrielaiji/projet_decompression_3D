def create_z_simple(liste_vertices):

    result = []

    n = len(liste_vertices)

    # Ajouter le face tout en haut
    result.append((liste_vertices[0],liste_vertices[1],liste_vertices[2]))
    # Ajouter le face tout en bas
    result.append((liste_vertices[n-1],liste_vertices[n-2],liste_vertices[n-3]))

    # le nombre des faces de chaque côté
    nb_f_cote = (n-2-2)/2

    # On ajoute les faces dont 2 vertices sont à gauche
    i = 0
    j = 2
    compteur = 0
    while compteur<nb_f_cote
        result.append((liste_vertices[i%n],liste_vertices[j],liste_vertices[(i-1)%n]))
        compteur += 1
        i -= 1
        j += 1

    # On ajoute les faces dont 2 vertices sont à droit
    i = 2
    j = n-1
    compteur = 0
    while compteur<nb_f_cote
        result.append((liste_vertices[i],liste_vertices[j],liste_vertices[i+1]))
        compteur += 1
        i += 1
        j -= 1

    return result