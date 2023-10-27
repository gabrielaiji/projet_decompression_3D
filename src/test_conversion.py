import obja
from io_obj.read_obj import read_obj

model = obja.parse_file('example/suzanne.obj')
list_faces = read_obj(model)
my_list_map = list(map(lambda face : face.toString(), list_faces))
for face in my_list_map:
    print(face)