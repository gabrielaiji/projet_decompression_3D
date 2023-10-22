import obja
from convert_obj_to_list_faces import convert_obj_to_list_faces

model = obja.parse_file('example/suzanne.obj')
list_faces = convert_obj_to_list_faces(model)
my_list_map = list(map(lambda face : face.toString(), list_faces))
for face in my_list_map:
    print(face)