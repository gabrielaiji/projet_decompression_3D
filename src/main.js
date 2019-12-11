let camera, scene, renderer, loader, light1, light2, controls, model;

init();
animate();

function init() {

    loader = new Loader('assets/bunny_translate.obj');
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
