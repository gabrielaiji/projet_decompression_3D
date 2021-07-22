#!/usr/bin/env python

import obja
import numpy as np
import sys

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()

    def contract(self, output):
        """
        Decimates the model stupidly, and write the resulting obja in output.
        """
        operations = []

        # Iterate through the vertex
        for (vertex_index, vertex) in enumerate(self.vertices):

            for (face_index, face) in enumerate(self.faces):

                # Delete any face that depends on this vertex
                if face_index not in self.deleted_faces:
                    self.deleted_faces.add(face_index)
                    operations.append(('face', face_index, face))

            # Delete the vertex
            operations.append(('vertex', vertex_index, vertex))

        # To rebuild the model, run operations in reverse order
        operations.reverse()

        output_model = obja.Output(output)

        for (ty, index, value) in operations:
            if ty == "vertex":
                output_model.add_vertex(index, value)
            else:
                output_model.add_face(index, value)

def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('exemple/suzanne.obj')

    with open('exemple/suzanne.obja', 'w') as output:
        model.contract(output)


if __name__ == '__main__':
    main()
