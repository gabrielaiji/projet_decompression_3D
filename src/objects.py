from __future__ import annotations

class Vertex:

	def __init__(self, v_id: int, x: float, y: float, z: float):
		self._id = v_id
		self._x = x
		self._y = y
		self._z = z
		self.faces = set()

	def setId(self, id: int):
		self._id = id

	def setX(self, x: float):
		self._x = x

	def setY(self, y: float):
		self._y = y

	def setZ(self, z: float):
		self._z = z

	def getCoords(self) -> list[float]:
		return [self._x, self._y, self._z]
	
	def toString(self):
		return "Vertex : Id : {} ;  Coords : {} {} {}".format(self._id, self._x, self._y, self._z)
	
	def printToObja(self):
		return "v {} {} {}".format(self._x, self._y, self._z)

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
		if face in self.faces:
			self.faces.remove(face)
	
	def getFaces(self) -> set[Face]:
		return self.faces
	


class Face:

	def __init__(self, f_id: int, vertices: list[Vertex]):
		self._id = f_id
		self._vertices = vertices
		self._color = None

		for vertex in vertices:
			vertex.addFace(self)

	def setId(self, id: int):
		self._id = id

	def getVertices(self) -> list[Vertex]:
		return self._vertices

	def setColor(self, color: list[float]):
		self._color = color

	def getColor(self) -> list[float]:
		return self._color

	def getVertexCoords(self) -> list[list[float]]:
		return list(map(lambda vertex : vertex.getCoords(), self._vertices))

	def getVertexIds(self) -> list[list[int]]:
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
	
	def delete(self):
		for vertex in self._vertices:
			vertex.removeFace(self)


class Patch:

	def __init__(self, p_id: int, faces: list[Face], deleted_Vertex: Vertex):
		self._id = p_id
		self._faces = faces
		self._color = None
		self._deleted_vertex = deleted_Vertex

	def setColor(self, color: list[float]):
		for face in self._faces:
			face.setColor(color)
		self._color = color

	def getColor(self) -> list[float]:
		return self._color
	
	def getDeletedVertexCoords(self) -> list[float]:
		return self._deleted_vertex.getCoords()
	
	def getFaces(self) -> list[Face]:
		return self._faces

	def getVertices(self) -> list[Vertex]:
		vertices_dico = {}

		for face in self._faces:
			local_vertices = face.getVertices()
			for vertice in local_vertices:
				v_id = vertice.id()
				if v_id not in vertices_dico:
					vertices_dico[v_id] = vertice

		return vertices_dico.values()

	def getVertexCoords(self) -> list[list[float]]:
		return list(map(lambda vertex : vertex.getCoords(), self.getVertices()))

	def getVertexIds(self) -> list[list[int]]:
		return list(map(lambda vertex : vertex.id(), self.getVertices()))
	
	def setDisplacementVector(self, vector: list[float]):
		self._displacement_vector = vector
	
	def getDisplacementVector(self) -> list[float]:
		return self._displacement_vector

	def id(self) -> int:
		return self._id