console.log("code 1");
function eko(x) {
    console.log(x)
}

var temps= [33, 44];
var trace1 = {
    y: temps,
    type: 'scatter'
}
var data = [trace1];

eko("start xxx");
function gid(i) {
    return document.getElementById(i);
}

function doplot() {
    const xhr1 = new XMLHttpRequest();
    
    xhr1.open("GET", "data");
    xhr1.send();
    xhr1.responseType = "json";
    const d = new Date();
    
    eko("get linky data...");

    let time = d.getTime();
    xhr1.onload = () => {
	eko("data received")
        let dates = [];
	if (xhr1.readyState == 4 && xhr1.status == 200) {
	    let response = xhr1.response;
	    let buf = response;
	    let date0 = d.getTime();
            eko(buf);
            eko(response);
            eko(response.interval_sec);
            //date0 = buf.date;
            let interval_sec = buf.interval_sec;
            eko(date0);
            function f0(e, i) {
                eko(e[0]);
                return e[0];
            }
            let consos = buf.values.map(f0);
            for (i in consos) {
                let nd = new Date(date0 + i * interval_sec*1000);
                dates.push(nd);
            }
            
            const trace = {
                showlegend: true,
                xaxis: {
                    type: 'date',
                    title: 'consos récentes'
                },
                yaxis: {
                    title: 'Watt',                    
                    rangemode: 'tozero'
                },
                x : dates,
                y : consos,
                //type: 'scatter',
                'line': {'shape': 'spline'} };

            
	    Plotly.newPlot('graph', [trace]);
	    eko("plotted");
	}
	eko("processed");
    }
    setTimeout(doplot, 1000 * 2); // 1 mn
}

setTimeout(doplot, 1000 * 1); // 1 mn
eko("ok");	




