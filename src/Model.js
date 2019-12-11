class Model extends THREE.Mesh {
    constructor() {
        let geometry = new THREE.Geometry();
        let material = new THREE.MeshLambertMaterial({color: 0xffffff});
        super(geometry, material);
        this.frustumCulled = false;
        this.vertices = [];
    }

    manageElement(element) {
        switch (element.type) {
            case Element.AddVertex:
                this.geometry.vertices.push(element.value);
                this.geometry.verticesNeedUpdate = true;
                break;

            case Element.EditVertex:
                this.geometry.vertices[element.id].copy(element.value);
                this.geometry.verticesNeedUpdate = true;
                this.geometry.elementsNeedUpdate = true;
                break;

            case Element.AddFace:

                let vertices = this.geometry.vertices;
                let f = element.value;
                let normal =
                    vertices[f.b].clone().sub(vertices[f.a])
                        .cross(vertices[f.c].clone().sub(vertices[f.a]));
                normal.normalize();

                f.normal = normal;
                this.geometry.faces.push(f);
                this.geometry.elementsNeedUpdate = true;
                break;

            default:
                throw new Error("unknown element type: " + element.type);
        }
    }
}
