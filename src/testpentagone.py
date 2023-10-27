from objects import Vertex, Face
from patch.order_vertices import orderVertices
from patch.create import create_z_simple

v1 = Vertex(1, 0, 0, 0)
v18 = Vertex(18, 0, 0, 0)
v23 = Vertex(23, 0, 0, 0)
v15 = Vertex(15, 0, 0, 0)
v20 = Vertex(20, 0, 0, 0)
v19 = Vertex(19, 0, 0, 0)
v30 = Vertex(30, 0, 0, 0)

f1 = Face(1, [v18, v23, v1])
f4 = Face(4, [v15, v23, v1])
f6 = Face(6, [v15, v20, v1])
f3 = Face(3, [v30, v20, v1])
#f5 = Face(5, [v19, v30, v1])
f2 = Face(2, [v18, v30, v1])

faces = [f1, f4, f6, f3, f2]

ordered_v = orderVertices(faces, v1)

returned_faces, _ = create_z_simple(ordered_v, 7)

for face in returned_faces:
    print("\nface {}".format(face.id()))
    print("vertices : {}".format(face.getVertexIds()))


