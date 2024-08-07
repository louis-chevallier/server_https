const top  = document.getElementById('top');
const label  = document.getElementById('label');

var map = L.map('map', { zoomControl:false } ).fitWorld();

var openstreet = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})



var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

const scheme = "hybrid.day.mobile"
/*
var here = L.tileLayer.here({
    appId: 'itFu46QqjFn8CY0rfLdB',
    appCode: 'fUSfSpQI48RWqR4PxOu7Kg',
    scheme: scheme})
*/
var layer = googleSat
    
layer.addTo(map);

map.locate({setView: true, maxZoom: 16});

function onLocationFound(e) {
    var radius = e.accuracy;
    console.log(e.latlng)
    console.log(e.accuracy)
    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();
    
    L.circle(e.latlng, radius).addTo(map);

    var u = location.protocol + "//" + location.host + "/gps/position?"
    u = u + "latitude=" + e.latlng.lat;
    u = u + "&longitude=" + e.latlng.lng;
    u = u + "&accuracy=" + e.accuracy;
    console.log(u)
    const xhr1 = new XMLHttpRequest();
    xhr1.onreadystatechange = () => {
        if (xhr1.readyState === 4) {
            let ss = xhr1.responseText;            
            label.innerText =  ss;
            //EKOX(ss);
        }
    }  
    xhr1.open("GET", u, true)
    xhr1.send();
    
}

function refresh() {
    var u = location.protocol + "//" + location.host + "/gps/refresh";
    console.log(u);
    const xhr1 = new XMLHttpRequest();
    xhr1.onreadystatechange = () => {
        if (xhr1.readyState === 4) {
            let ss = xhr1.responseText;            
            label.innerText =  ss;
            //EKOX(ss);
        }
    }  
    xhr1.open("GET", u, true)
    xhr1.send();
    setTimeout(refresh, 1000)    
}


map.on('locationfound', onLocationFound);
setTimeout(refresh, 1000)
