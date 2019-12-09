class Model extends THREE.Mesh {
    constructor() {
        let geometry = new THREE.BufferGeometry();
        let vertices = new Float32Array(10000000);
        geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
        let normals = new Float32Array(10000000);
        geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
        let material = new THREE.MeshLambertMaterial({color: 0xffffff});
        super(geometry, material);
        this.frustumCulled = false;
        this.vertices = [];
        this.currentFace = 0;
    }

    manageElement(element) {
        switch (element.type) {
            case Element.AddVertex:
                this.vertices.push(element.value);
                break;

            case Element.AddFace:
                let buf = this.geometry.attributes.position.array;
                buf[this.currentFace * 9    ] = this.vertices[element.value.a - 1].x;
                buf[this.currentFace * 9 + 1] = this.vertices[element.value.a - 1].y;
                buf[this.currentFace * 9 + 2] = this.vertices[element.value.a - 1].z;
                buf[this.currentFace * 9 + 3] = this.vertices[element.value.b - 1].x;
                buf[this.currentFace * 9 + 4] = this.vertices[element.value.b - 1].y;
                buf[this.currentFace * 9 + 5] = this.vertices[element.value.b - 1].z;
                buf[this.currentFace * 9 + 6] = this.vertices[element.value.c - 1].x;
                buf[this.currentFace * 9 + 7] = this.vertices[element.value.c - 1].y;
                buf[this.currentFace * 9 + 8] = this.vertices[element.value.c - 1].z;
                this.geometry.attributes.position.needsUpdate = true;

                let normal =
                    this.vertices[element.value.b - 1].clone().sub(this.vertices[element.value.a - 1])
                        .cross(this.vertices[element.value.c - 1].clone().sub(this.vertices[element.value.a - 1]));
                normal.normalize();

                buf = this.geometry.attributes.normal.array;
                buf[this.currentFace * 9    ] = normal.x;
                buf[this.currentFace * 9 + 1] = normal.y;
                buf[this.currentFace * 9 + 2] = normal.z;
                buf[this.currentFace * 9 + 3] = normal.x;
                buf[this.currentFace * 9 + 4] = normal.y;
                buf[this.currentFace * 9 + 5] = normal.z;
                buf[this.currentFace * 9 + 6] = normal.x;
                buf[this.currentFace * 9 + 7] = normal.y;
                buf[this.currentFace * 9 + 8] = normal.z;
                this.geometry.attributes.normal.needsUpdate = true;

                this.currentFace++;
                break;

            default:
                throw new Error("unknown element type: " + element.type);
        }
        this.geometry.verticesNeedUpdate = true;
        this.geometry.elementsNeedUpdate = true;
    }
}
