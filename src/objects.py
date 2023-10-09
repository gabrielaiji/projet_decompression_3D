
class Vertice:

	def __init__(self, v_id: int, x: float, y: float, z: float):
		self._id = v_id
		self._x = x
		self._y = y
		self._z = z

	def setX(self, x: float):
		self._x = x

	def setY(self, y: float):
		self._y = y

	def setZ(self, z: float):
		self._z = z

	def getCoords(self) -> list[float]:
		return [self._x, self._y, self._z]

	def id() -> int:
		return self._id

	def x() -> float:
		return self._x

	def y() -> float:
		return self._y

	def z() -> float:
		return self._z


class Face:

	def __init__(self, f_id: int, vertices: list[Vertice]):
		self._id = f_id
		self._vertices = vertices
		self._color = None

	def getVertices() -> list[Vertice]:
		return self._vertices

	def setColor(color: list[float]):
		self._color = color

	def getColor() -> list[float]:
		return self._color

	def getVerticesCoords() -> list[list[float]]:
		return list.map(lambda vertice : vertice.getCoords(), self._vertices)

	def getVerticesIds() -> list[list[int]]:
		return list.map(lambda vertice : vertice.id(), self._vertices)

	def id() -> int:
		return self._id


class Patch:

	def __init__(self, p_id: int, faces: list[Face]):
		self._id = p_id
		self._faces = faces
		self._color = None

	def setColor(color: list[float]):
		for face in self._faces:
			face.setColor(color)
		self._color = color

	def getColor() -> list[float]:
		return self._color

	def getVertices() -> list[Vertice]:
		vertices_dico = {}

		for face in faces:
			local_vertices = face.getVertices()
			for vertice in local_vertices:
				v_id = vertice.id()
				if v_id not in vertices_dico:
					vertices_dico[v_id] = vertice

		return vertices_dico.values()

	def getVerticesCoords() -> list[list[float]]:
		return list.map(lambda vertice : vertice.getCoords(), self.getVertices())

	def getVerticesIds() -> list[list[int]]:
		return list.map(lambda vertice : vertice.id(), self.getVertices())

	def id() -> int:
		return self._id