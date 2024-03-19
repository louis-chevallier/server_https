

//console.log(document.navigator.userAgentData.brands);


//const detailedUserAgentData = await window.navigator.userAgentData. then(d => { EKOX(d) });



//const isMobile = window.navigator.userAgentData.mobile; //resolves true/false
//EKOX(isMobile)


/*
function arbre() {
    EKOX("")
    // prettier-ignore
    let data = [{ "id": "0", "text": "node-0", "children": [{ "id": "0-0", "text": "node-0-0", "children": [{ "id": "0-0-0", "text": "node-0-0-0" }, { "id": "0-0-1", "text": "node-0-0-1" }, { "id": "0-0-2", "text": "node-0-0-2" }] }, { "id": "0-1", "text": "node-0-1", "children": [{ "id": "0-1-0", "text": "node-0-1-0" }, { "id": "0-1-1", "text": "node-0-1-1" }, { "id": "0-1-2", "text": "node-0-1-2" }] }, { "id": "0-2", "text": "node-0-2", "children": [{ "id": "0-2-0", "text": "node-0-2-0" }, { "id": "0-2-1", "text": "node-0-2-1" }, { "id": "0-2-2", "text": "node-0-2-2" }] }] }, { "id": "1", "text": "node-1", "children": [{ "id": "1-0", "text": "node-1-0", "children": [{ "id": "1-0-0", "text": "node-1-0-0" }, { "id": "1-0-1", "text": "node-1-0-1" }, { "id": "1-0-2", "text": "node-1-0-2" }] }, { "id": "1-1", "text": "node-1-1", "children": [{ "id": "1-1-0", "text": "node-1-1-0" }, { "id": "1-1-1", "text": "node-1-1-1" }, { "id": "1-1-2", "text": "node-1-1-2" }] }, { "id": "1-2", "text": "node-1-2", "children": [{ "id": "1-2-0", "text": "node-1-2-0" }, { "id": "1-2-1", "text": "node-1-2-1" }, { "id": "1-2-2", "text": "node-1-2-2" }] }] }, { "id": "2", "text": "node-2", "children": [{ "id": "2-0", "text": "node-2-0", "children": [{ "id": "2-0-0", "text": "node-2-0-0" }, { "id": "2-0-1", "text": "node-2-0-1" }, { "id": "2-0-2", "text": "node-2-0-2" }] }, { "id": "2-1", "text": "node-2-1", "children": [{ "id": "2-1-0", "text": "node-2-1-0" }, { "id": "2-1-1", "text": "node-2-1-1" }, { "id": "2-1-2", "text": "node-2-1-2" }] }, { "id": "2-2", "text": "node-2-2", "children": [{ "id": "2-2-0", "text": "node-2-2-0" }, { "id": "2-2-1", "text": "node-2-2-1" }, { "id": "2-2-2", "text": "node-2-2-2" }] }] }]


    let tree = new Tree('.container',
                        {
                            data: [{ id: '-1', text: 'root', children: data }],
                            closeDepth: 3,
                            loaded: function () {
                                this.values = ['0-0-0', '0-1-1'];
                                console.log(this.selectedNodes);
                                console.log(this.values);
                                this.disables = ['0-0-0', '0-0-1', '0-0-2']
                            },
                            onChange: function () {
                                console.log(this.values);
                            }
                        })
}

arbre();
*/



let camera, renderer, cameraControls;
let mouseX = 0, mouseY = 0;
let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;
let object;

const session = new onnx.InferenceSession()
//const session = new onnx.InferenceSession({ backendHint: 'webgl' });

function preprocess(data, width, height) {
  const dataFromImage = ndarray(new Float32Array(data), [width, height, 4]);
  const dataProcessed = ndarray(new Float32Array(width * height * 3), [1, 3, height, width]);

  // Normalize 0-255 to (-1)-1
  ndarray.ops.subseq(dataFromImage.pick(2, null, null), 103.939);
  ndarray.ops.subseq(dataFromImage.pick(1, null, null), 116.779);
  ndarray.ops.subseq(dataFromImage.pick(0, null, null), 123.68);

  // Realign imageData from [224*224*4] to the correct dimension [1*3*224*224].
  ndarray.ops.assign(dataProcessed.pick(0, 0, null, null), dataFromImage.pick(null, null, 2));
  ndarray.ops.assign(dataProcessed.pick(0, 1, null, null), dataFromImage.pick(null, null, 1));
  ndarray.ops.assign(dataProcessed.pick(0, 2, null, null), dataFromImage.pick(null, null, 0));

  return dataProcessed.data;
}

async function load_model(){
    EKOX("loading model")
    await session.loadModel('get_model')
    EKOX("model loaded");
}

async function local_predict() {
    // load image.
    const imageSize = 224;
    const imageLoader = new ImageLoader(imageSize, imageSize);
    const imageData = await imageLoader.getImageData('./brocoli.jpg');

    // preprocess the image data to match input dimension requirement, which is 1*3*224*224
    const width = 224; //imageSize;
    const height = 224; //imageSize;
    const preprocessedData = preprocess(imageData.data, width, height);
    
    const inputTensor = new onnx.Tensor(preprocessedData, 'float32', [1, 3, width, height]);
    // Run model with Tensor inputs and get the result.
    const outputMap = await session.run([inputTensor]);
    const outputData = outputMap.values().next().value.data;
    
    // Render the output result in html.
    EKOX(outputData);
    dataurl.value = outputData;
}

async function remote_predict() {

    const imageSize = 224;
    const imageLoader = new ImageLoader(imageSize, imageSize);
    const imageData = await imageLoader.getImageData('./brocoli.jpg');
    let image_data_url = imageLoader.canvas.toDataURL('image/jpeg');
    
    let data = JSON.stringify({image: image_data_url});
    const chunk = data.split(',').pop()
    EKOX("fetching");
    const response = await fetch('chunk', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            chunk: chunk
        })
    })
    EKOX('fetched');
    const json = await response.json();
    EKOX(json.status)
    /*
    var httpPost = new XMLHttpRequest()
    //httpPost.setHeader('Content-Type', 'application/json');
    httpPost.open("POST",  "/get_photo", true);
    httpPost.send(data);
    EKOX("sent");
    */
    if (json.status == "ok")  {
        dataurl.value = json.name + " p=" + json.probability;
    }
    //dataurl.value = image_data_url;
    dataurl_container.style.display = 'block';

}


function date() {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = date+' '+time;
    return dateTime
}    

function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

function onDocumentMouseMove( event ) {
    mouseX = ( event.clientX - windowHalfX ) / 2;
    mouseY = ( event.clientY - windowHalfY ) / 2;
}

function trace(txt) {
    let t = document.getElementById("json").innerHTML;    
    if (txt == "clear") {
        t = "";
    }
    if (t.length > 2000) {
        t = t.slice(0, 2000);
    }
    document.getElementById("json").innerHTML  =  date() + txt + "<br>" + t;        
}




var selectPhoto = document.getElementById('photoselect');
var formPhoto   = document.getElementById('uploadPhoto')
console.log('init');


// trick pour rendre ces fct accessibles depuis le html ..
//window.doReset = doReset;
//window.doGo = doGo;
//window.activate = activate;



//let activer_alarm_button = document.querySelector("#alarm-on");
//activer_alarm_button.addEventListener('click', activer_alarmf)

//let desactiver_alarm_button = document.querySelector("#alarm-off");
//desactiver_alarm_button.addEventListener('click', desactiver_alarmf)

async function activer_alarmf() {
    alarmf(true, activer_alarm_button);
}
async function desactiver_alarmf() {
    alarmf(false, desactiver_alarm_button);
}

async function alarmf(alarm_on, button) {
    EKOX("activate alarm " + alarm_on);    
    const xhr1 = new XMLHttpRequest();
    xhr1.onreadystatechange = () => {
        if (xhr1.readyState === 4) {
            let old = button.innerText;
            let ss = xhr1.responseText;            
            button.innerText =  ss;
            EKOX(ss);
            setInterval(function() {
                button.innerText =  old;
            }, 2000)
        }
    };

    const onoff = alarm_on ? 'AWAY_MODE' : 'HOME_MODE';
    xhr1.open("GET", "alarm?onoff=" + onoff );
    xhr1.send();
}


EKOX("starting");



