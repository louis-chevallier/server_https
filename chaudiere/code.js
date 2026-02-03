
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const info = document.getElementById('info');

// Points de division (normalisés 0 à 1, multipliés par largeur)
let points = [0.2, 0.4, 0.6, 0.8]; // Segments initiaux
let draggedIndex = -1;
const lineY = 100;
const lineHeight = 10;
const handleRadius = 8;

function draw() {
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
        ctx.fillStyle = `hsl(${i * 60}, 70%, 60%)`;
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
        ctx.fillText(p.toFixed(2), x, lineY + 25);
    });
}

function getPointFromEvent(e) {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / canvas.width;
    return Math.max(0, Math.min(1, x));
}

function findClosestPoint(px) {
    let closestIndex = -1;
    let minDist = Infinity;
    points.forEach((p, index) => {
        const dist = Math.abs(p - px);
        if (dist < minDist) {
            minDist = dist;
            closestIndex = index;
        }
    });
    return closestIndex;
}

canvas.addEventListener('mousedown', (e) => {
    const px = getPointFromEvent(e);
    draggedIndex = findClosestPoint(px);
    if (draggedIndex === -1 && e.offsetX / canvas.width < 0.05) draggedIndex = 0; // Bord gauche
    draw();
});

canvas.addEventListener('mousemove', (e) => {
    if (draggedIndex !== -1) {
        points[draggedIndex] = getPointFromEvent(e);
        // Éviter doublons et tri implicite
        points = points.filter((p, i) => i !== draggedIndex || true).sort((a, b) => a - b);
        draw();
    }
});

canvas.addEventListener('mouseup', () => {
    draggedIndex = -1;
    draw();
});

// Ajout de point par double-clic
canvas.addEventListener('dblclick', (e) => {
    const px = getPointFromEvent(e);
    if (!points.includes(px)) {
        points.push(px);
        points.sort((a, b) => a - b);
        draw();
    }
});

// Suppression par clic droit
canvas.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    const px = getPointFromEvent(e);
    const index = findClosestPoint(px);
    if (index !== -1) {
        points.splice(index, 1);
        draw();
    }
});

draw(); // Dessin initial




