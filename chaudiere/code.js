const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const info = document.getElementById('info');
const log = document.getElementById('log');
var timer = 0;

log.innerHTML = "version 3"

function eko(x) {
    console.log(x)
}

// Adaptation responsive
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// Points de division (normalisés 0 à 1, multipliés par largeur)
let points = [0.2, 0.4, 0.6, 0.8]; // Segments initiaux
let draggedIndex = -1;
const lineY = 100;
const lineHeight = 10;
const handleRadius = 8;

function fractionToTime(fraction) {
  // fraction entre 0 et 1
  const totalHours = fraction * 24;
  const hours = Math.floor(totalHours);
  const minutes = Math.round((totalHours - hours) * 60);

  const hh = String(hours).padStart(2, '0');
  const mm = String(minutes).padStart(2, '0');
  return `${hh}:${mm}`; // ex: "06:00" pour 0.25
}

function clean() {
    const thr = 10 / (24*60);
    console.log(points);
    const a = points;
    const a1 = points.slice(1).concat([99900]);
    const z = a1.map((e, i) => [e, a[i]]);
    const r = z.filter((ab,i) => ab[0]-ab[1]>thr).map(a => a[1])
    points = r;
    console.log(points);
    
}


function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Ligne principale
    ctx.strokeStyle = '#333';
    ctx.lineWidth = lineHeight;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(lineY, 0);
    ctx.lineTo(lineY, canvas.height);
    ctx.stroke();

    // Segments colorés
    const sortedPoints = [0, ...points.sort((a, b) => a - b), 1];
    for (let i = 0; i < sortedPoints.length - 1; i++) {
        const x1 = sortedPoints[i] * canvas.height;
        const x2 = sortedPoints[i + 1] * canvas.height;

	const on_off = i%2 == 1 ? 1 : 0;
	//const color = `hsl(${i * 60}, 70%, 60%)`
	const color = `hsl(60, 70%, ${on_off*100}%)`
	//const color = i%2 == 1 ? "`black`" : "`white`" 

	
        ctx.fillStyle = color;
        ctx.fillRect(lineY - lineHeight/2, x1,
		     lineHeight, x2 - x1);
    }

    // Poignées cliquables
    points.forEach((p, index) => {
        const x = p * canvas.height;
        ctx.fillStyle = draggedIndex === index ? '#ff4444' : '#444';
        ctx.beginPath();
        ctx.arc(lineY, x, handleRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    });

    // Labels des positions
    points.forEach((p, index) => {
        const x = p * canvas.height;
        ctx.fillStyle = '#000';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(fractionToTime(p), lineY + 25, x);
    });
}


function draw1() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Ligne principale
    ctx.strokeStyle = '#333';
    ctx.lineWidth = lineHeight;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(0, lineY);
    ctx.lineTo(canvas.width, lineY);
    ctx.stroke();

    // Segments colorés
    const sortedPoints = [0, ...points.sort((a, b) => a - b), 1];
    for (let i = 0; i < sortedPoints.length - 1; i++) {
        const x1 = sortedPoints[i] * canvas.width;
        const x2 = sortedPoints[i + 1] * canvas.width;

	const on_off = i%2 == 1 ? 1 : 0;
	//const color = `hsl(${i * 60}, 70%, 60%)`
	const color = `hsl(60, 70%, ${on_off*100}%)`
	//const color = i%2 == 1 ? "`black`" : "`white`" 

	
        ctx.fillStyle = color;
        ctx.fillRect(x1, lineY - lineHeight/2, x2 - x1, lineHeight);
    }

    // Poignées cliquables
    points.forEach((p, index) => {
        const x = p * canvas.width;
        ctx.fillStyle = draggedIndex === index ? '#ff4444' : '#444';
        ctx.beginPath();
        ctx.arc(x, lineY, handleRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    });

    // Labels des positions
    points.forEach((p, index) => {
        const x = p * canvas.width;
        ctx.fillStyle = '#000';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(fractionToTime(p), x, lineY + 25);
    });
}

function getPointFromEvent(e) {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / canvas.width;
    return Math.max(0, Math.min(1, x));
}

function findClosestPoint(px) {
    let closestIndex = -1;
    const rect = canvas.getBoundingClientRect();
    let minDist = 0.02 ; //canvas.height / 50; //Infinity;
    console.log(points);
    console.log("mindist", minDist);
    const pxs = px; //px / canvas.height;
    console.log("pxs", pxs);
    points.forEach((p, index) => {
        const dist = Math.abs(p - pxs);
	console.log("dist", dist);
        if (dist < minDist) {
            minDist = dist;
            closestIndex = index;
        }
    });
    return closestIndex;
}

function getPosition1(e) {
    const rect = canvas.getBoundingClientRect();
    let x;
    if (e.touches) {
        x = e.touches[0].clientX - rect.left;
    } else {
        x = e.clientX - rect.left;
    }
    return Math.max(0, Math.min(1, x / canvas.width)); // Clamp 0-1
}
function getPosition(e) {
    const rect = canvas.getBoundingClientRect();
    let x;

    if (e.touches) {
        x = e.touches[0].clientY - rect.top;
    } else {
        x = e.clientY - rect.top;
    }
    return Math.max(0, Math.min(1, x / canvas.height)); // Clamp 0-1
}
let lastTap = 0;

function down(e) {

    const curTime = new Date().getTime();
    const tapLen = curTime - lastTap;
    console.log(tapLen, curTime);
    if (tapLen < 500 && tapLen > 0) {
	console.log('Double tapped!');
	doubleclick(e);
    } else {
	simpleclick(e);
    }
    lastTap = curTime;    
}

function simpleclick(e) {
    var px = getPointFromEvent(e);
    e.preventDefault();
    const pos = getPosition(e);
    px = pos;
    draggedIndex = findClosestPoint(px);
    console.log("dragged", draggedIndex);
    if (draggedIndex === -1 && e.offsetX / canvas.width < 0.05) draggedIndex = 0; // Bord gauche
    upload(true);    
    draw();
}

function move(e) {
    //console.log("move");
    //console.log(e)    
    if (draggedIndex !== -1) {
        //points[draggedIndex] = getPointFromEvent(e);
        points[draggedIndex] = getPosition(e);
        // Éviter doublons et tri implicite
        points = points.filter((p, i) => i !== draggedIndex || true).sort((a, b) => a - b);
	//upload();
        draw();
    }
}   
function up() {
    draggedIndex = -1;
    console.log("up");
    draw();    
    upload(true);
    //reload();
}


function upload(doreload) {
    const xhr1 = new XMLHttpRequest();
    xhr1.onreadystatechange = () => {
        if (xhr1.readyState === 4) {
            let ss = xhr1.responseText;
            //console.log(ss)
	    //reload()
        }
    };
    var data_s = encodeURIComponent(JSON.stringify(points));
    try {
        xhr1.open("POST", "set_data?data=" + data_s);
        xhr1.send();
    }
    catch(err) {
        console.log(err);
    }
}

function reload() {
    const xhr1 = new XMLHttpRequest();
    xhr1.open("GET", "get_data");
    xhr1.send();
    xhr1.responseType = "json";
    xhr1.onload = () => {
	//eko("data received")
        let dates = [];
	if (xhr1.readyState == 4 && xhr1.status == 200) {
	    let response = xhr1.response;
	    let buf = response;
            //eko(buf);
            console.log(response);//eko(response);
	    points = response;
	    points = [0.2, 0.4, 0.6, 0.8]; // Segments initiaux

	}
    }
    //draw()
}

function doubleclick(e) {
    var px = getPointFromEvent(e);
    e.preventDefault();
    const pos = getPosition(e);
    console.log(px)
    console.log(pos)
    px = pos;

    const closest = findClosestPoint(px);
    if (closest != -1) {
	console.log("suppress", closest);
	suppress(e)
    } else {
	console.log("add");
	if (!points.includes(px)) {
            points.push(px);
	    upload(true);
            points.sort((a, b) => a - b);
            draw();
	}
    }
}

function suppress(e) {
    e.preventDefault();
    var px = getPointFromEvent(e);
    e.preventDefault();
    const pos = getPosition(e);
    px = pos;
    
    const index = findClosestPoint(px);
    if (index !== -1) {
        points.splice(index, 1);
	upload(true);	
        draw();
    }
}

canvas.addEventListener('mousedown', down)
canvas.addEventListener('mousemove', move);
canvas.addEventListener('mouseup', up);


canvas.addEventListener('touchstart', down, { passive: false });
canvas.addEventListener('touchmove', move, { passive: false });
canvas.addEventListener('touchend', up);


// Ajout de point par double-clic
//canvas.addEventListener('dblclick', doubleclick);


// Suppression par clic droit
canvas.addEventListener('contextmenu', suppress);

function refresh() {
    //reload()
    //draw()
    //timer = setInterval(refresh, 1000 ); // 1 sec    
}
reload()
timer = setInterval(refresh, 1000 ); // 1 sec

draw(); // Dessin initial




