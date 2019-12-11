function fetchDataLength(path, callback) {
    let xhr = new XMLHttpRequest();

    xhr.open('HEAD', path, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(xhr.getResponseHeader('Content-Length'));
            }
        }
    };
    xhr.send();
}

function fetchData(path, start, end, callback) {
    let xhr = new XMLHttpRequest();

    xhr.open('GET', path, true);
    xhr.setRequestHeader('Range', 'bytes=' + start + "-" + (end - 1));
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 206) {
                callback(xhr.responseText);
            }
        }
    };
    xhr.send();
}

function parseLine(line) {
    let element = {};
    let split = line.split(/[ \t]+/);

    if (split.length === 0) {
        return;
    }

    switch (split[0]) {
        case "v":
            element.type = Element.AddVertex;
            element.value = new THREE.Vector3(
                parseFloat(split[1]),
                parseFloat(split[2]),
                parseFloat(split[3]),
            );
            return element;

        case "f":
            element.type = Element.AddFace;
            element.value = new THREE.Face3(
                parseInt(split[1], 10) - 1,
                parseInt(split[2], 10) - 1,
                parseInt(split[3], 10) - 1,
            );
            return element;

        case "ts":
            element.type = Element.AddTriangleStrip;
            element.value = [];
            for (let i = 1; i < split.length - 2; i++) {
                element.value.push(new THREE.Face3(
                    parseInt(split[i]  , 10) - 1,
                    i % 2 === 1 ? parseInt(split[i+1], 10) - 1 : parseInt(split[i+2], 10) - 1,
                    i % 2 === 1 ? parseInt(split[i+2], 10) - 1 : parseInt(split[i+1], 10) - 1,
                ));
            }
            return element;

        case "tf":
            element.type = Element.AddTriangleFan;
            element.value = [];
            for (let i = 1; i < split.length - 2; i++) {
                element.value.push(new THREE.Face3(
                    parseInt(split[1]  , 10) - 1,
                    parseInt(split[i+1], 10) - 1,
                    parseInt(split[i+2], 10) - 1,
                ));
            }
            return element;

        case "ev":
            element.type = Element.EditVertex;
            element.id = parseInt(split[1], 10) - 1;
            element.value = new THREE.Vector3(
                parseFloat(split[2]),
                parseFloat(split[3]),
                parseFloat(split[4]),
            );
            return element;

        case "ef":
            element.type = Element.EditFace;
            element.id = parseInt(split[1], 10) - 1;
            element.value = new THREE.Face3(
                parseInt(split[2], 10) - 1,
                parseInt(split[3], 10) - 1,
                parseInt(split[4], 10) - 1,
            );
            return element;

        case "df":
            element.type = Element.DeleteFace;
            element.id = parseInt(split[1], 10) - 1;
            return element;

        case "":
        case "#":
            return;

        default:
            throw new Error(split[0] + " is not a defined macro");
    }

}

const Element = {};
Element.AddVertex = "AddVertex";
Element.AddFace = "AddFace";
Element.AddTriangleStrip = "AddTriangleStrip";
Element.AddTriangleFan = "AddTriangleFan";
Element.EditVertex = "EditVertex";
Element.EditFace = "EditFace";
Element.DeleteFace = "DeleteFace";

class Loader {
    constructor(path, chunkSize = 1024, timeout = 20) {
        this.path = path;
        this.chunkSize = chunkSize;
        this.timeout = timeout;
        this.currentByte = 0;
        this.remainder = "";
    }

    start(callback) {
        fetchDataLength(this.path, (length) => {
            this.dataLength = length;
            this.next(callback);
        });
    }

    percentage() {
        return 100 * this.currentByte / this.dataLength;
    }

    next(callback) {
        this.downloadAndParseNextChunk((data) => {
            callback(data);
            setTimeout(() => {
                this.next(callback);
            }, this.timeout);
        });
    }

    downloadAndParseNextChunk(callback) {

        let upperBound = Math.min(this.currentByte + this.chunkSize, this.dataLength);

        if (upperBound <= this.currentByte) {
            return;
        }

        fetchData(this.path, this.currentByte, upperBound, (data) => {

            this.currentByte = upperBound;

            let elements = [];
            let split = data.split('\n');
            split[0] = this.remainder + split[0];
            this.remainder = split.pop();

            for (let line of split) {
                elements.push(parseLine(line));
            }

            callback(elements);

        });
    }
}

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
