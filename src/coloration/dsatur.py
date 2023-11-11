import numpy as np
from typing import Any, List, Dict
from itertools import permutations
import copy

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
    #dsatur_values = [0 for _ in range(nb_vertices)]

    available_colors = [[True]*k for _ in range(nb_vertices)]
    colors = [0 for _ in range(nb_vertices)]

    for vertex in sorted_indexes[::-1]:
        print("Vertex {} of degree {}".format(vertex+1, degrees[vertex]))
        #if dsatur_values[vertex] >= k:
            #colors[vertex] = None
        for color_i in range(k):
            # Color the vertex 
            if available_colors[vertex][color_i]:
                print("color {}".format(color_i))
                colors[vertex] = color_i

                for voisin in range(nb_vertices):
                    if adjacency[vertex][voisin] > 0:
                        available_colors[voisin][color_i] = False
                        #dsatur_values[voisin] += 1
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
    colors = [0 for _ in range(nb_vertices)]

    for degree in present_degrees:
        vertices = degree_registry[degree]
        vertices_permutations = list(permutations(vertices))

        for vertices_order in vertices_permutations:
            found_good_order = False
            available_colors_copy = copy.deepcopy(available_colors)
            go_to_next_order = False
            vertex_order = 0
            
            while (not go_to_next_order) and vertex_order < len(vertices_order):
                vertex = vertices_order[vertex_order]
                color_i = 0
                for color_i in range(k):
                    # Color the vertex 
                    if available_colors_copy[vertex][color_i]:
                        colors[vertex] = color_i

                        for voisin in range(nb_vertices):
                            if adjacency[vertex][voisin] > 0:
                                available_colors_copy[voisin][color_i] = False
                        break
                    
                    elif color_i == k-1:
                        colors[vertex] = None
                        go_to_next_order = True

                if vertex_order == len(vertices_order)-1 and (not go_to_next_order):
                    found_good_order = True

                vertex_order +=1
            
            if found_good_order:
                break
        
        available_colors = copy.deepcopy(available_colors_copy)

    return colors
