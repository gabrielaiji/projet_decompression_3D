from objects import Patch
import numpy as np

def predict(lst_patches: list[Patch]):
    
	for patch in lst_patches:
		vertices_coord = patch.getVertexCoords()
		coord_mean = np.mean(np.array(vertices_coord),1)
		deleted_vertex_coord = patch.getDeletedVertexCoords()
		patch.setDisplacementVector(list(deleted_vertex_coord - coord_mean))