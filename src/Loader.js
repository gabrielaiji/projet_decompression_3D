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
            console.log("Loading finished: " + this.currentByte + " / " + this.dataLength);
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
