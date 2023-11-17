import obja
from io_obj.read_obj import read_Mesh
from io_obj.write_obj import write_mesh
from delete.todeletemaillage import getVerticesToDelete
from patch.create import patch_mesh

nb_iterations = 1
model = obja.parse_file('../example/cube.obj')
mesh = read_Mesh(model)

for i in range(nb_iterations):
    print("Iteration : " + str(i))
    print("\tflag 0 iteration")
    #vertices_to_delete = getVerticesToDelete(mesh)
    vertices_to_delete = [mesh.getVertexFromId(0), mesh.getVertexFromId(7)]
    vertices_to_delete_ids = list(map(lambda v: v.id()+1, vertices_to_delete))
    print("Vertices to delete : {}".format(vertices_to_delete_ids))


    print("\tflag 1 iteration")
    patch_mesh(mesh, vertices_to_delete)
    print("\tflag 2 iteration")
    output_file = "../example/bunny_comp.obj"
    write_mesh(mesh, output_file)

for vertex in mesh.getVertices():
    print(vertex.printToFacesId())

for face in mesh.getFaces():
    print(face.printToVerticesId())
    
output_file = "../example/cube_compressee.obj"
write_mesh(mesh, output_file)

