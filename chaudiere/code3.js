const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const info = document.getElementById('info');

// Adaptation responsive
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// Positions des séparateurs (normalisées 0 à 1)
let separators = [0.2, 0.5, 0.8];
let draggingIndex = -1; // Index du séparateur déplacé
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


// Obtenir position normalisée (0 à 1) depuis événement touch/mouse
function getPosition(e) {
    const rect = canvas.getBoundingClientRect();
    let x;
    if (e.touches) {
        x = e.touches[0].clientX - rect.left;
    } else {
        x = e.clientX - rect.left;
    }
    return Math.max(0, Math.min(1, x / canvas.width)); // Clamp 0-1
}

// Dessiner la ligne et séparateurs
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const midY = canvas.height / 2;
    const lineH = 8;
    const sepW = 40;
    const sepH = 60;

    // Ligne principale
    ctx.strokeStyle = '#333';
    ctx.lineWidth = lineH;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(0, midY);
    ctx.lineTo(canvas.width, midY);
    ctx.stroke();

    // Séparateurs (visuellement agrandis pour tactile [web:59])
    separators.forEach((pos, i) => {
        const x = pos * canvas.width;
        ctx.fillStyle = draggingIndex === i ? '#ff6b6b' : '#4ecdc4';
        ctx.fillRect(x - sepW/2, midY - sepH/2, sepW, sepH);
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 3;
        ctx.strokeRect(x - sepW/2, midY - sepH/2, sepW, sepH);
    });

    // Labels segments (pourcentages)
    ctx.fillStyle = '#333';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    let prev = 0;
    separators.forEach((pos, i) => {
        const seg = ((pos - prev) * 100).toFixed(0) + '%';
        const midX = (prev + pos) / 2 * canvas.width;
        ctx.fillText(seg, midX, midY - sepH - 10);
        prev = pos;
    });
    const lastSeg = ((1 - prev) * 100).toFixed(0) + '%';
    ctx.fillText(lastSeg, (prev + 1)/2 * canvas.width, midY - sepH - 10);
}

// Début drag : trouver séparateur le plus proche
function startDrag(pos) {
    draggingIndex = -1;
    let minDist = 0.05; // Tolérance tactile ~5%
    separators.forEach((sep, i) => {
        if (Math.abs(sep - pos) < minDist) {
            draggingIndex = i;
            minDist = Math.abs(sep - pos);
        }
    });
    if (draggingIndex === -1) {
        // Ajout nouveau si loin de tous
        separators.push(pos);
        separators.sort((a,b)=>a-b);
        draggingIndex = separators.indexOf(pos);
    }
}

// Déplacement
function drag(pos) {
    if (draggingIndex !== -1) {
        separators[draggingIndex] = pos;
        separators.sort((a,b)=>a-b); // Maintien ordre
        draggingIndex = separators.indexOf(pos); // Update index
    }
    draw();
    info.textContent = `Segments: ${separators.map(p => (p*100).toFixed(0)+'%').join(', ')}`;
}

// Événements unifiés touch/mouse [web:54][web:61]
function handleStart(e) {
    e.preventDefault();
    const pos = getPosition(e);
    startDrag(pos);
    draw();
}
function handleMove(e) {
    e.preventDefault();
    const pos = getPosition(e);
    drag(pos);
}
function handleEnd(e) {
    e.preventDefault();
    draggingIndex = -1;
    draw();
}

// Bind événements
canvas.addEventListener('touchstart', handleStart, { passive: false });
canvas.addEventListener('touchmove', handleMove, { passive: false });
canvas.addEventListener('touchend', handleEnd);
canvas.addEventListener('mousedown', handleStart);
canvas.addEventListener('mousemove', handleMove);
canvas.addEventListener('mouseup', handleEnd);

draw(); // Init
