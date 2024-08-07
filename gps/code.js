const top  = document.getElementById('top');
EKOT("code 1");

var map = L.map('map', { zoomControl:false } ).fitWorld();

openstreet = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})



googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

scheme = "hybrid.day.mobile"
here = L.tileLayer.here({
    appId: 'itFu46QqjFn8CY0rfLdB',
    appCode: 'fUSfSpQI48RWqR4PxOu7Kg',
    scheme: scheme})

layer = googleSat
    
layer.addTo(map);

map.locate({setView: true, maxZoom: 16});

function onLocationFound(e) {
    var radius = e.accuracy;
    console.log(e.latlng)
    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();
    
    L.circle(e.latlng, radius).addTo(map);
}

