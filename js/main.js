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
            element.value = new THREE.Vector3(parseFloat(split[1]), parseFloat(split[2]), parseFloat(split[3]));
            return element;

        case "f":
            element.type = Element.AddFace;
            element.value = new THREE.Face3(parseInt(split[1], 10), parseInt(split[2], 10), parseInt(split[3], 10));
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

class Loader {
    constructor(path, chunkSize = 1024, timeout = 20) {
        this.path = path;
        this.chunkSize = chunkSize;
        this.timeout = timeout;
        this.currentByte = 0;
        this.remainder = "";
    }

    start(callback) {
        this.downloadAndParseNextChunk((data) => {
            callback(data);
            setTimeout(() => {
                this.start(callback);
            }, this.timeout);
        });
    }

    downloadAndParseNextChunk(callback) {
        fetchData(this.path, this.currentByte, this.currentByte + this.chunkSize, (data) => {

            if (data.length === 0) {
                console.log("Loading finished");
                return;
            }

            this.currentByte += this.chunkSize;

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

let camera, scene, renderer, loader, light1, light2, controls, model;

init();
animate();

function init() {

    loader = new Loader('assets/bunny_low_res_scaled.obj');
    loader.start(function(elements) {
        for (let element of elements) {
            if (element !== undefined) {
                model.manageElement(element);
            }
        }
    });

    camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.0001, 1000);
    camera.position.z = 3;

    scene = new THREE.Scene();

    model = new Model();
    scene.add(model);

    light1 = new THREE.AmbientLight(0x999999);
    scene.add(light1);

    light2 = new THREE.DirectionalLight(0xffffff, 1.0);
    light2.position.set(0.0, 1.0, 0.0);
    scene.add(light2);

    renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);

}

function animate() {

    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);

}

