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
    print("flag 0 iteration")
    vertices_to_delete = getVerticesToDelete(mesh)
    print("flag 1 iteration")
    patch_mesh(mesh, vertices_to_delete)
    print("flag 2 iteration")
    output_file = "../example/bunny_comp.obj"
    write_mesh(mesh, output_file)
    
output_file = "../example/cube_decompressee.obj"
#write_mesh(mesh, output_file)

