const top  = document.getElementById('top');
const label  = document.getElementById('label');
const name  = document.getElementById('trace_name');


function refresh() {
    var u = location.protocol + "//" + location.host + "/gps/refresh";
    console.log('refresh', u);
    const xhr1 = new XMLHttpRequest();
    xhr1.onreadystatechange = () => {
        if (xhr1.readyState === 4) {
            let ss = xhr1.responseText;
            console.log('ss', ss);            
            let rep = JSON.parse(ss);
            console.log(rep);
            //console.log(rep.length)
            label.innerText =  ss;
            for (const [key, e] of Object.entries(rep)) {
                console.log(key)
                console.log(e)
                L.circle({ lat : e.latitude, lng : e.longitude}, e.accuracy).addTo(map);
            }
            //EKOX(ss);
        }
    }  
    xhr1.open("GET", u, true)
    xhr1.send();
    //setTimeout(refresh, 1000)    
}

function success(position) {
    console.log("success");    
}

function error() {
    console.log("Error.");
}


setTimeout(refresh, 1000)
