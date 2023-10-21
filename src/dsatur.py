import numpy as np


def dsatur(adjacency: list[list[int]], k: int):
    """
    Colors the vertices with k colors at most.

    :param: adjacency : Adjacency Matrix
    :param: k : maximum of colors
    """
    adjacency = np.array(adjacency)
    nb_vertices = len(adjacency)
    degrees = np.sum(adjacency, 1)
    sorted_indexes = np.argsort(degrees)
    dsatur_values = [i for i in range(nb_vertices)]
    colors = [0 for _ in range(nb_vertices)]

    for i in sorted_indexes:
        if dsatur_values[i] >= k:
            colors[i] = None
            print("DSATUR K-Coloring graph failed for vertex ", i)
        else:
            # Color the graph
            colors[i] = dsatur_values[i]

            # Update neighbors dsatur values
            for voisin in range(nb_vertices):
                if adjacency[i][voisin] > 0:
                    dsatur_values[voisin] += 1

    return colors
