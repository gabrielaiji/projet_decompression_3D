import numpy as np
from typing import Any
from itertools import permutations

def add_values_in_dict(dict: dict[Any, list], key, value_to_add):
    if key not in dict:
        dict[key] = list()
    dict[key].append(value_to_add)
    return dict

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



def dsatur_modif(adjacency: list[list[int]], k: int):
    """
    Colors the vertices with k colors at most.

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


    #sorted_indexes = np.argsort(degrees)
    #dsatur_values = [0 for _ in range(nb_vertices)]
    available_colors = [[True]*k for _ in range(nb_vertices)]
    colors = [0 for _ in range(nb_vertices)]

    for degree in present_degrees:
        vertices = degree_registry[degree]
        vertices_permutations = list(permutations(vertices))

        print("\n\n\n-----------------")
        print("degree : {}".format(degree))
        print("-----------------\n")
        
        for i in range(nb_vertices):
            print("available colors for vertex {} : {}".format(i+1, available_colors[i]))

        for vertices_order in vertices_permutations:
            #dsatur_values_copy = dsatur_values.copy()
            available_colors_copy = available_colors.copy()
            go_to_next_order = False
            found_good_order = False
            vertex_order = 0

            print("\n\nVertice Order : {}".format(vertices_order))
            

            while (not go_to_next_order) and vertex_order < len(vertices_order):
                vertex = vertices_order[vertex_order]
                #print("Vertex {} of degree {}, dsatur : {}".format(vertex+1, degrees[vertex], dsatur_values[vertex]))
                color_i = 0
                #check_next_color = True
                for color_i in range(k):
                #while check_next_color and color_i < k:
                    # Color the vertex 
                    #print("\nAvailable colors for vertex {}".format(vertex))
                    #print(available_colors_copy[vertex])
                    if available_colors_copy[vertex][color_i]:
                        #print("Vertex {} -> color {}".format(vertex, color_i))
                        colors[vertex] = color_i

                        for voisin in range(nb_vertices):
                            if adjacency[vertex][voisin] > 0:
                                available_colors_copy[voisin][color_i] = False
                        #check_next_color = False
                        break
                    
                    elif color_i == k-1:
                        #print("Vertex {} -> color None".format(vertex))
                        colors[vertex] = None
                        go_to_next_order = True
                        print(colors)
                    color_i +=1

                vertex_order +=1

        
        
        available_colors = available_colors_copy.copy()

    return colors
