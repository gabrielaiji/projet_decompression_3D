from objects import Vertex, Face, Patch
from prediction.predictor import predict

v1 = Vertex(1, 6.0, 2.0, 0.0)
v2 = Vertex(2, 4.0, 4.0, 0.0)
v3 = Vertex(3, 2.0, 4.0, 0.0)
v4 = Vertex(4, 0.0, 2.0, 0.0)
v5 = Vertex(5, 2.0, 0.0, 0.0)
v6 = Vertex(6, 4.0, 0.0, 0.0)
# deleted_Vertex :
v7 = Vertex(7, 4.0, 3.0, 0.0)

# deleted_faces :
f1 = Face(1, [v1, v2, v7])
f2 = Face(2, [v2, v3, v7])
f3 = Face(3, [v7, v3, v4])
f4 = Face(4, [v7, v4, v5])
f5 = Face(5, [v6, v7, v5])
f6 = Face(6, [v1, v7, v6])

# patch_faces :
f7 = Face(7, [v1, v2, v6])
f8 = Face(8, [v2, v3, v6])
f9 = Face(9, [v6, v3, v5])
f10 = Face(10, [v3, v4, v5])

patches = []
p1 = Patch(1, [f1, f2, f3, f4, f5, f6], [f7, f8, f9, f10], v7)
patches.append(p1)

predict(patches)

DispVect = patches[0].getDisplacementVector()
print(DispVect)