import obja
from io_obj.read_obj import read_Mesh
from io_obj.write_obj import write_mesh, write_obj_decompression
from delete.todeletemaillage import getDelete_distance, getVerticesToDelete
from patch.create import patch_mesh

nb_iterations = 8
model = obja.parse_file('../example/icosphere.obj')
mesh = read_Mesh(model)

nb_faces_original = len(mesh.getFaces())
nb_v_original = len(mesh.getVertices())

del_dist = getDelete_distance(mesh)

print("Delete Distance calculated : {}".format(del_dist))
for i in range(nb_iterations):
    print("Iteration : " + str(i))
    print("\tflag 0 iteration")
    vertices_to_delete = getVerticesToDelete(mesh, del_dist)
    #vertices_to_delete = [mesh.getVertexFromId(0)]
    vertices_to_delete_ids = list(map(lambda v: v.id()+1, vertices_to_delete))
    #print("Vertices to delete : {}".format(vertices_to_delete_ids))


    print("\tflag 1 iteration")
    mesh = patch_mesh(mesh, vertices_to_delete)
    print("\tflag 2 iteration")
    #output_file = "../example/bunny_comp.obj"
    #write_mesh(mesh, output_file)

#output_file = "../example/bunny_compressee.obj"
#write_mesh(mesh, output_file)

print("\nNb Faces debut : {}".format(nb_faces_original))
print("Nb Vertices debut : {}".format(nb_v_original))

print("\nNb Faces final : {}".format(len(mesh.getFaces())))
print("Nb Vertices final : {}".format(len(mesh.getVertices())))

output_file = "../example/icosphere_decompressee.obja"
write_obj_decompression(mesh, output_file)

