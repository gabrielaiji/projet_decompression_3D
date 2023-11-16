import numpy as np
from typing import Any, List, Dict
from itertools import permutations
import copy
from random import shuffle

def add_values_in_dict(dict: Dict[Any, List], key, value_to_add):
    if key not in dict:
        dict[key] = list()
    dict[key].append(value_to_add)
    return dict

def dsatur(adjacency: List[List[int]], k: int):
    """
    Colors the vertices with k colors at most according to 
    the DSATUR algorithme. It is not sure to find a solution

    :param: adjacency : Adjacency Matrix
    :param: k : maximum of colors
    """
    adjacency = np.array(adjacency)
    nb_vertices = len(adjacency)
    degrees = np.sum(adjacency, 1)

    sorted_indexes = np.argsort(degrees)

    available_colors = [[True]*k for _ in range(nb_vertices)]
    colors = [0 for _ in range(nb_vertices)]

    for vertex in sorted_indexes[::-1]:
        print("Vertex {} of degree {}".format(vertex+1, degrees[vertex]))

        for color_i in range(k):
            # Color the vertex 
            if available_colors[vertex][color_i]:
                print("color {}".format(color_i))
                colors[vertex] = color_i

                for voisin in range(nb_vertices):
                    if adjacency[vertex][voisin] > 0:
                        available_colors[voisin][color_i] = False
                break
            
            if color_i == k-1:
                print("DSATUR K-Coloring graph failed for vertex ", vertex+1)
                colors[vertex] = None

    return colors



def dsatur_modif(adjacency: List[List[int]], k: int):
    """
    Colors the vertices with k colors at most. It is inspired
    from the DSATUR algorithm. If a solution exists, it will
    find it.

    :param: adjacency : Adjacency Matrix
    :param: k : maximum of colors
    """
    adjacency = np.array(adjacency)
    nb_vertices = len(adjacency)
    degrees = np.sum(adjacency, 1)

    degree_registry = {}
    for vertex in range(nb_vertices):
        add_values_in_dict(degree_registry, degrees[vertex], vertex)
    
    present_degrees = list(degree_registry.keys())
    present_degrees.sort(reverse=True)

    available_colors = [[True]*k for _ in range(nb_vertices)]
    colors = [None for _ in range(nb_vertices)]

    max_permutation = 1000
    for degree in present_degrees:
        if degree == 0:
            break
        #print("\t\t degree ", str(degree))
        vertices = degree_registry[degree]
        vertices_permutations = list(permutations(vertices))
        shuffle(vertices_permutations)
        vertices_permutations \
            = vertices_permutations[:min(max_permutation, len(vertices_permutations))]

        colors_copy = copy.copy(colors)

        
        max_colored_vertices = 0
        best_coloration_map = []        
        for order_i, vertices_order in enumerate(vertices_permutations):
            #print("\t\t\t order ", str(order_i))
            available_colors_copy = copy.deepcopy(available_colors)
            
            colored_nb_vertices = 0
            nb_vertices_in_order = len(vertices_order)
            for vertex in vertices_order:
                #print("\t\t\t\t vertex ", str(vertex))
                for color_i in range(k):
                    # Color the vertex 
                    if available_colors_copy[vertex][color_i]:
                        colored_nb_vertices += 1
                        colors_copy[vertex] = color_i

                        for voisin in range(nb_vertices):
                            if adjacency[vertex][voisin] > 0:
                                available_colors_copy[voisin][color_i] = False
                        break
                    
                    elif color_i == k-1:
                        colors_copy[vertex] = None

            if colored_nb_vertices == nb_vertices_in_order:
                best_coloration_map = copy.copy(colors_copy)
                break
            elif colored_nb_vertices > max_colored_vertices:
                best_coloration_map = copy.copy(colors_copy)
                max_colored_vertices = colored_nb_vertices
        
        colors = copy.copy(best_coloration_map)
        available_colors = copy.deepcopy(available_colors_copy)

    return colors

import numpy as np

def dsatur_modif2(adjacency: np.ndarray, k: int) -> np.ndarray:
    """
    Optimized DSATUR algorithm using NumPy for vertex coloring.

    :param adjacency: Adjacency matrix as a NumPy array.
    :param k: Maximum number of colors.
    :return: Array of colors assigned to each vertex.
    """
    nb_vertices = len(adjacency)
    degrees = np.sum(adjacency, axis=1)

    # Sorting vertices by degree in descending order
    sorted_vertices = np.argsort(degrees)[::-1]

    # Initializing color assignments and available color tracking
    colors = np.full(nb_vertices, -1, dtype=int)
    available_colors = np.ones((nb_vertices, k), dtype=bool)

    for vertex in sorted_vertices:
        # Identifying available colors for this vertex
        neighbors = adjacency[vertex] > 0
        unavailable_colors = np.any(available_colors[neighbors], axis=0)
        available_color_indices = np.where(unavailable_colors)[0]

        if available_color_indices.size > 0:
            # Assigning the first available color
            selected_color = available_color_indices[0]
            colors[vertex] = selected_color
            # Updating available colors for neighbors
            available_colors[neighbors, selected_color] = False
        else:
            # No available color found, marking as uncolored
            colors[vertex] = -1

    return colors

