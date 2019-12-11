class Model extends THREE.Mesh {
    constructor(path) {
        let geometry = new THREE.Geometry();
        let materials = [
            new THREE.MeshLambertMaterial( { color: 0xffffff, side: THREE.DoubleSide } ),
            new THREE.MeshBasicMaterial( { transparent: true, opacity: 0 } )
        ];
        super(geometry, materials);
        this.frustumCulled = false;
        this.path = path;
        this.vertices = [];
        this.currentLine = 1;
    }

    throwError(message) {
        let e = new Error("In " + this.path + ":L" + this.currentLine + " " + message);
        e.type = "custom";
        throw e;
    }

    checkVertex(id) {
        if (this.geometry.vertices[id] === undefined) {
            this.throwError("EditVertex requires vertex " + (id + 1) + " but there is no such vertex");
        }
    }

    checkFaceId(id) {
        if (this.geometry.faces[id] === undefined) {
            this.throwError("EditFace requires face " + (id + 1) + " but there is no such face");
        }
    }

    checkFace(f) {
        let vertices = this.geometry.vertices;

        if (vertices[f.a] === undefined) {
            this.throwError("Face requires vertex " + (f.a + 1) + " but there is no such vertex");
        }

        if (vertices[f.b] === undefined) {
            this.throwError("Face requires vertex " + (f.b + 1) + " but there is no such vertex");
        }

        if (vertices[f.c] === undefined) {
            this.throwError("Face requires vertex " + (f.c + 1) + " but there is no such vertex");
        }

    }

    manageElement(element) {

        let vertices = this.geometry.vertices;
        let f, normal;

        switch (element.type) {
            case Element.AddVertex:
                this.geometry.vertices.push(element.value);
                this.geometry.verticesNeedUpdate = true;
                break;

            case Element.EditVertex:
                this.checkVertex(element.id);
                this.geometry.vertices[element.id].copy(element.value);
                this.geometry.verticesNeedUpdate = true;
                break;

            case Element.AddFace:

                f = element.value;
                this.checkFace(f);
                normal =
                    vertices[f.b].clone().sub(vertices[f.a])
                        .cross(vertices[f.c].clone().sub(vertices[f.a]));
                normal.normalize();

                f.normal = normal;
                f.materialIndex = 0;
                this.geometry.faces.push(f);
                this.geometry.elementsNeedUpdate = true;
                break;

            case Element.AddTriangleStrip:
            case Element.AddTriangleFan:

                for (let f of element.value) {

                    this.checkFace(f);
                    let normal =
                        vertices[f.b].clone().sub(vertices[f.a])
                        .cross(vertices[f.c].clone().sub(vertices[f.a]));
                    normal.normalize();

                    f.normal = normal;
                    f.materialIndex = 0;
                    this.geometry.faces.push(f);

                }

                this.geometry.elementsNeedUpdate = true;

                break;

            case Element.EditFace:

                f = element.value;
                this.checkFaceId(element.id);
                this.checkFace(f);
                normal =
                    vertices[f.b].clone().sub(vertices[f.a])
                        .cross(vertices[f.c].clone().sub(vertices[f.a]));
                normal.normalize();

                f.normal = normal;


                this.geometry.faces[element.id] = f;
                this.geometry.elementsNeedUpdate = true;
                break;

            case Element.DeleteFace:
                this.geometry.faces[element.id].materialIndex = 1;
                this.geometry.elementsNeedUpdate = true;
                break;


            default:
                throw new Error("unknown element type: " + element.type);
        }

        this.currentLine++;
    }
}