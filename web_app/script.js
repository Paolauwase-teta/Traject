const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');

// Controls
const velocitySlider = document.getElementById('velocity-slider');
const velocityInput = document.getElementById('velocity');
const angleSlider = document.getElementById('angle-slider');
const angleInput = document.getElementById('angle');
const gravitySelect = document.getElementById('gravity');
const launchBtn = document.getElementById('launch-btn');

// Stats
const maxHeightDisplay = document.getElementById('max-height');
const maxRangeDisplay = document.getElementById('max-range');
const flightTimeDisplay = document.getElementById('flight-time');
const currentTimeDisplay = document.getElementById('current-time');

// State
let animationId = null;
let projectile = null;
let trail = [];

// Resize Canvas
function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
    drawScene();
}
window.addEventListener('resize', resize);

// Sync Inputs
function syncInputs(slider, input) {
    slider.addEventListener('input', () => { input.value = slider.value; drawScene(); });
    input.addEventListener('input', () => { slider.value = input.value; drawScene(); });
}
syncInputs(velocitySlider, velocityInput);
syncInputs(angleSlider, angleInput);

// Projectile Class
class Projectile {
    constructor(v0, angleDeg, g) {
        this.v0 = v0;
        this.angleRad = angleDeg * (Math.PI / 180);
        this.g = g;
        this.t = 0;
        this.startTime = null;
        this.active = true;
        
        // Physics constants
        this.vx = this.v0 * Math.cos(this.angleRad);
        this.vy_init = this.v0 * Math.sin(this.angleRad);
        
        // Calculate maxes
        this.totalTime = (2 * this.v0 * Math.sin(this.angleRad)) / this.g;
        this.maxHeight = (Math.pow(this.v0, 2) * Math.pow(Math.sin(this.angleRad), 2)) / (2 * this.g);
        this.maxRange = (Math.pow(this.v0, 2) * Math.sin(2 * this.angleRad)) / this.g;
        
        // Update stats
        maxHeightDisplay.innerHTML = `${this.maxHeight.toFixed(2)} <span class="unit">m</span>`;
        maxRangeDisplay.innerHTML = `${this.maxRange.toFixed(2)} <span class="unit">m</span>`;
        flightTimeDisplay.innerHTML = `${this.totalTime.toFixed(2)} <span class="unit">s</span>`;
    }

    update(dt) {
        if (!this.active) return;
        this.t += dt;

        if (this.t >= this.totalTime) {
            this.t = this.totalTime;
            this.active = false;
        }

        currentTimeDisplay.innerText = this.t.toFixed(2);
    }

    getPosition(time) {
        const x = this.vx * time;
        const y = (this.vy_init * time) - (0.5 * this.g * Math.pow(time, 2));
        return { x, y };
    }
}

// Drawing
function drawGrid(scale) {
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    ctx.beginPath();
    
    // Vertical lines
    for(let x = 0; x < canvas.width; x += 50) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
    }
    // Horizontal lines
    for(let y = 0; y < canvas.height; y += 50) {
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
    }
    ctx.stroke();

    // Ground
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height - 50);
    ctx.lineTo(canvas.width, canvas.height - 50);
    ctx.stroke();
}

function drawScene() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGrid();

    // Transform coordinate system (flip y, origin bottom-left)
    ctx.save();
    ctx.translate(50, canvas.height - 50); // Margin 50px
    ctx.scale(1, -1); // Flip Y

    // Determine scale factor based on max range to fit in view
    let scale = 1;
    // Simple auto-scale
    const v0 = parseFloat(velocityInput.value);
    const ang = parseFloat(angleInput.value) * (Math.PI/180);
    const g = parseFloat(gravitySelect.value);
    const expectedRange = (v0*v0 * Math.sin(2*ang)) / g;
    const expectedHeight = (v0*v0 * Math.sin(ang)**2) / (2*g);
    
    // Fit range in 80% of width, height in 80% of height
    const scaleX = (canvas.width * 0.8) / (expectedRange || 10);
    const scaleY = (canvas.height * 0.8) / (expectedHeight || 10);
    scale = Math.min(scaleX, scaleY, 10); // Limit max zoom
    scale = Math.max(scale, 0.5); // Limit min zoom

    // Draw previous trail if exists
    if (trail.length > 0) {
        ctx.beginPath();
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 3;
        ctx.shadowBlur = 10;
        ctx.shadowColor = '#06b6d4';
        
        trail.forEach((pos, i) => {
            if (i === 0) ctx.moveTo(pos.x * scale, pos.y * scale);
            else ctx.lineTo(pos.x * scale, pos.y * scale);
        });
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    // Draw current projectile
    if (projectile) {
        const pos = projectile.getPosition(projectile.t);
        
        // Draw Projectile
        ctx.fillStyle = '#f472b6';
        ctx.beginPath();
        ctx.arc(pos.x * scale, pos.y * scale, 6, 0, Math.PI * 2);
        ctx.fill();

        // Add glow
        ctx.shadowBlur = 15;
        ctx.shadowColor = '#f472b6';
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    ctx.restore();
}

// Animation Loop
let lastTime = 0;
function loop(timestamp) {
    if (!lastTime) lastTime = timestamp;
    const dt = (timestamp - lastTime) / 1000; // seconds
    lastTime = timestamp;

    if (projectile && projectile.active) {
        projectile.update(dt * 2); // 2x speed for better viewing
        const pos = projectile.getPosition(projectile.t);
        trail.push(pos);
    } else {
        animationId = null;
        return; // Stop animation
    }

    drawScene();
    animationId = requestAnimationFrame(loop);
}

// Launch Handler
launchBtn.addEventListener('click', () => {
    if (animationId) cancelAnimationFrame(animationId);
    
    const v0 = parseFloat(velocityInput.value);
    const angle = parseFloat(angleInput.value);
    const g = parseFloat(gravitySelect.value);

    projectile = new Projectile(v0, angle, g);
    trail = [];
    lastTime = 0;
    
    loop(0);
});

// Initial Draw
resize();
