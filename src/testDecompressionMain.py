import obja
from objects import Face, Patch, Mesh
from io_obj.read_obj import read_Mesh
from io_obj.write_obj import write_obj_decompression, write_mesh


nb_iterations = 1
model = obja.parse_file('../example/cube.obj')
mesh = read_Mesh(model)

""" for vertex in mesh.getVertices():
    print(vertex.id())
    print(vertex.printToObja())
print("\n")
for face in mesh.getFaces():
    print(face.id())
    print(face.printToObja()) """



idNewFace = len(mesh.getFaces())

newFace1 = Face(idNewFace, [mesh.getVertexFromId(0), mesh.getVertexFromId(7), mesh.getVertexFromId(5)])
idNewFace = idNewFace + 1
newFace2 = Face(idNewFace, [mesh.getVertexFromId(0), mesh.getVertexFromId(3), mesh.getVertexFromId(7)])
idNewFace = idNewFace + 1
newFace3 = Face(idNewFace, [mesh.getVertexFromId(5), mesh.getVertexFromId(7), mesh.getVertexFromId(2)])
idNewFace = idNewFace + 1
newFace4 = Face(idNewFace, [mesh.getVertexFromId(4), mesh.getVertexFromId(5), mesh.getVertexFromId(2)])
idNewFace = idNewFace + 1

mesh.addFaces([newFace1, newFace2, newFace3, newFace4])



patches = []

patch1 = Patch(0, [mesh.getFaceFromId(1), mesh.getFaceFromId(2), mesh.getFaceFromId(3), mesh.getFaceFromId(9)], [newFace1, newFace2], mesh.getVertexFromId(1))
patch1.setColor([0.0, 1.0, 0.0])
patches.append(patch1)
patch2 = Patch(1, [mesh.getFaceFromId(5), mesh.getFaceFromId(4), mesh.getFaceFromId(10), mesh.getFaceFromId(6)], [newFace3, newFace4], mesh.getVertexFromId(6))
patch2.setColor([1.0, 1.0, 0.0])
patches.append(patch2)

mesh.addPatchIteration(patches)



verticesToRemove = mesh.getVerticesFromId([1, 6])
mesh.removeVertices(verticesToRemove)

facesToRemove = mesh.getFacesFromId([1, 2, 3, 9, 5, 4, 10, 6])
mesh.removeFaces(facesToRemove)


output_file = "../example/cube_compressee_main.obj"
write_mesh(mesh, output_file)


output_file = "../example/cube_decompressee_main.obj"
write_obj_decompression(mesh, output_file)