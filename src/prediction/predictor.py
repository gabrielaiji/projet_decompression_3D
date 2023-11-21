import numpy as np

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
	from objects import Patch, Face, Vertex


"""def predict(lst_patches: List[Patch]):
    
	for patch in lst_patches:
		vertices_coord = patch.getVertexCoords()
		coord_mean = np.mean(np.array(vertices_coord),0)
		deleted_vertex_coord = patch.getDeletedVertexCoords()
		patch.setDisplacementVector(list(deleted_vertex_coord - coord_mean))"""


def predict(deleted_faces, deleted_Vertex):

	vertices = set()

	for face in deleted_faces:
		vertices = vertices.union(set(face.getVertices()))

	vertices.remove(deleted_Vertex)

	vertices_coord = np.array(list(map(lambda v:v.getCoords(), vertices)))
	coord_mean = np.mean(np.array(vertices_coord),0)

	return coord_mean