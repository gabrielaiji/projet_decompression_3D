from __future__ import annotations
from copy import copy

from typing import List, Set

class Vertex:

	def __init__(self, v_id: int, x: float, y: float, z: float):
		self._id = v_id
		self._x = x
		self._y = y
		self._z = z
		self.faces : Set[Face] = set()

	def setId(self, id: int):
		self._id = id

	def setX(self, x: float):
		self._x = x

	def setY(self, y: float):
		self._y = y

	def setZ(self, z: float):
		self._z = z

	def getCoords(self) -> List[float]:
		return [self._x, self._y, self._z]
	
	def toString(self):
		return "Vertex : Id : {} ;  Coords : {} {} {}".format(self._id, self._x, self._y, self._z)
	
	def printToObja(self):
		return "v {} {} {}".format(self._x, self._y, self._z)
	
	def printToFacesId(self):
		facesids = list(map(lambda face: face.id()+1, self.getFaces()))
		return "Vertex {} : F : {}".format(self.id()+1, facesids)

	def id(self) -> int:
		return self._id

	def x(self) -> float:
		return self._x

	def y(self) -> float:
		return self._y

	def z(self) -> float:
		return self._z
	
	def addFace(self, face: Face):
		self.faces.add(face)
	
	def removeFace(self, face: Face):
		self.faces.remove(face)
	
	def removeFaces(self, faces: Set[Face]):
		self.faces = self.faces.difference(faces)
	
	def addFaces(self, faces: Set[Face]):
		self.faces = self.faces.union(faces)
	
	def getFaces(self) -> set[Face]:
		return self.faces

class Face:

	def __init__(self, f_id: int, vertices: List[Vertex]):
		self._id = f_id
		self._vertices = vertices
		self._color = None
	
	def addRefToVertices(self):
		for vertex in self._vertices:
			vertex.addFace(self)

	def setId(self, id: int):
		self._id = id

	def getVertices(self) -> List[Vertex]:
		return self._vertices

	def setColor(self, color: List[float]):
		self._color = color

	def getColor(self) -> List[float]:
		return self._color

	def getVertexCoords(self) -> List[List[float]]:
		return list(map(lambda vertex : vertex.getCoords(), self._vertices))

	def getVertexIds(self) -> List[List[int]]:
		return list(map(lambda vertex : vertex.id(), self._vertices))

	def id(self) -> int:
		return self._id
	
	def toString(self):
		id1 = self._vertices[0].id()
		id2 = self._vertices[1].id()
		id3 = self._vertices[2].id()
		return "Face : Id : {} ;  V_Ids : {} {} {}".format(self._id, id1, id2, id3)
	
	def printToObja(self):
		id1 = self._vertices[0].id()
		id2 = self._vertices[1].id()
		id3 = self._vertices[2].id()
		return "f {} {} {}".format(id1, id2, id3)
	
	def printToVerticesId(self):
		verticesids = list(map(lambda v: v.id()+1, self.getVertices()))
		return "Face {} : V : {}".format(self.id()+1, verticesids)
	
	"""
	def deleteVertexReferences(self, deletedVertex: Vertex):
		for vertex in self._vertices:
			if vertex != deletedVertex:
				vertex.removeFace(self)"""

class Patch:

	def __init__(self, p_id: int,
			  deleted_faces: List[Face],
			  patch_faces: List[Face],
			  deleted_Vertex: Vertex):

		self._id = p_id
		self._patch_faces = patch_faces
		self._deleted_faces = deleted_faces
		self._color = None
		self._deleted_vertex = deleted_Vertex

	def setColor(self, color: List[float]):
		for face in self._patch_faces:
			face.setColor(color)
		self._color = color

	def getColor(self) -> List[float]:
		return copy(self._color)
	
	def getDeletedVertex(self) -> Vertex:
		return self._deleted_vertex
	
	def getDeletedVertexCoords(self) -> List[float]:
		return self._deleted_vertex.getCoords()
	
	def getPatchFaces(self) -> List[Face]:
		return copy(self._patch_faces)
	
	def getDeletedFaces(self) -> List[Face]:
		return copy(self._deleted_faces)

	def getVertices(self) -> List[Vertex]:
		vertices_dico = {}

		for face in self._patch_faces:
			local_vertices = face.getVertices()
			for vertice in local_vertices:
				v_id = vertice.id()
				if v_id not in vertices_dico:
					vertices_dico[v_id] = vertice

		return vertices_dico.values()

	def getVertexCoords(self) -> List[List[float]]:
		return list(map(lambda vertex : vertex.getCoords(), self.getVertices()))

	def getVertexIds(self) -> List[List[int]]:
		return list(map(lambda vertex : vertex.id(), self.getVertices()))
	
	def setDisplacementVector(self, vector: List[float]):
		self._displacement_vector = vector
	
	def getDisplacementVector(self) -> List[float]:
		return copy(self._displacement_vector)

	def id(self) -> int:
		return self._id

	"""
	def delete(self):
		for face in self.getPatchFaces():
			face.deleteVertexReferences(self.getDeletedVertex())"""
	
	def updateFacesVerticesReferences(self):
		deleted_f_ids = list(map(lambda f: f.id(), self.getDeletedFaces()))
		for face in self.getDeletedFaces():
			face_vertices = face.getVertices()
			for vertex in face_vertices:
				if vertex != self.getDeletedVertex():
					vertex.removeFace(face)

		
		for face in self.getPatchFaces():
			face.addRefToVertices()

	
class Mesh:

	def __init__(self, vertices: List[Vertex], faces: List[Face]):

		self._vertices = set(vertices)
		self._faces = set(faces)
		self._patches = []

		self._vertex_register = {vertex.id(): vertex for vertex in vertices}
		self._face_register = {face.id() : face for face in faces}

	def getVertices(self) -> List(Vertex):
		return list(self._vertices)
	
	def getVertexFromId(self, id:int) -> Vertex:
		return self._vertex_register[id]
	
	def getVerticesFromId(self, ids:List[int]) -> List[Vertex]:
		return list(map(lambda id : self.getVertexFromId(id), ids))
	
	def getFaces(self) -> List(Face):
		return list(self._faces)
	
	def getFaceFromId(self, id:int) -> Face:
		return self._face_register[id]
	
	def getFacesFromId(self, ids:List[int]) -> List[Face]:
		return list(map(lambda id : self.getFaceFromId(id), ids))

	def removeVertices(self, vertices_to_remove: List[Vertex]):
		self._vertices = self._vertices.difference(vertices_to_remove)

	def addVertices(self, vertices: List[Vertex]):
		self._vertices = self._vertices.union(set(vertices))
		register_update = {vertex.id(): vertex for vertex in vertices}
		self._vertex_register.update(register_update)

	def removeFaces(self, faces_to_remove: List[Face]):
		self._faces = self._faces.difference(faces_to_remove)
	
	def addFaces(self, faces: List[Face]):
		self._faces = self._faces.union(set(faces))
		register_update = {face.id(): face for face in faces}
		self._face_register.update(register_update)

	def getFaceNextId(self) -> int:
		ids = self._face_register.keys()
		return max(ids) + 1

	# Patches
	
	def addPatchIteration(self, patches: List[Patch]):
		self._patches.append(copy(patches))
	
	def getPatchesIterations(self) -> List[List[Patch]]:
		copy_lst = copy(self._patches)
		copy_lst.reverse()
		return copy_lst
	
	def applyCompression(self, patches: List[Patch]):
		for patch in patches:
			patch.updateFacesVerticesReferences()
			self._vertices.remove(patch.getDeletedVertex())

			for face in patch.getDeletedFaces():
				self._faces.remove(face)
			
			self.addFaces(patch.getPatchFaces())
			
	
		self.addPatchIteration(patches)
	