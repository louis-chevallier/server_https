const force_on  = document.getElementById('force_on');
const force_off  = document.getElementById('force_off');
const auto  = document.getElementById('auto');

function f(m) {
    console.log( location.protocol)
    console.log( location.host)
    const u = location.protocol + "//" + location.host + "/alarm_mode?mode=" + m;
    console.log(u)
    const xhr1 = new XMLHttpRequest();
    xhr1.open("GET", u, true)
    xhr1.send();
}

force_on.addEventListener('click', function (event) { f("on") ; })
force_off.addEventListener('click', function (event) { f("off") ; })
auto.addEventListener('click', function (event) { f("auto") ; })


