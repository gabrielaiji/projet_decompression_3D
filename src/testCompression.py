import obja
from io_obj.read_obj import read_Mesh
from io_obj.write_obj import write_mesh
from delete.todeletemaillage import getVerticesToDelete
from patch.create import patch_mesh

nb_iterations = 10
model = obja.parse_file('../example/Poule.obj')
mesh = read_Mesh(model)

nb_faces_original = len(mesh.getFaces())
nb_v_original = len(mesh.getVertices())

for i in range(nb_iterations):
    for face in mesh.getFaces():
        face.setColor(None)
    print("Iteration : " + str(i))
    print("\tflag 0 iteration")
    vertices_to_delete = getVerticesToDelete(mesh)
    #vertices_to_delete = [mesh.getVertexFromId(0)]
    vertices_to_delete_ids = list(map(lambda v: v.id()+1, vertices_to_delete))


    print("\tflag 1 iteration")
    mesh = patch_mesh(mesh, vertices_to_delete)
    print("\tflag 2 iteration")

    print("\t Nb_faces : {}".format(len(mesh.getFaces())))
    print("\t Nb_vertices : {}".format(len(mesh.getVertices())))

print("\nNb Faces debut : {}".format(nb_faces_original))
print("Nb Vertices debut : {}".format(nb_v_original))

print("\nNb Faces final : {}".format(len(mesh.getFaces())))
print("Nb Vertices final : {}".format(len(mesh.getVertices())))

output_file = "../example/Poule_compressee.obj"
write_mesh(mesh, output_file)

