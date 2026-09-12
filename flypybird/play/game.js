const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

const ffvCanvas = document.getElementById('ffv');
const ffvCtx = ffvCanvas.getContext('2d');
const FFV_W = ffvCanvas.width, FFV_H = ffvCanvas.height;
const FFV_FOV_DEG = 100; // the fly's forward vertical field of view -- a modelling choice, not a measured fact

const brainCanvas = document.getElementById('brainviz');
const brainCtx = brainCanvas.getContext('2d');

const GROUND_H = 40;
const GRAVITY = 1400;       // px/s^2 -- back to the original M2 value
const FLAP_VY = -420;       // px/s, set (not added) on flap
const BIRD_X = 120;
const BIRD_R = 14;
const PIPE_W = 18;          // thin pickets, not the original M2 wall width
const PIPE_GAP = 170;
const PIPE_SPEED = 180;     // px/s
const PIPE_SPACING = 260;   // px between pipe pairs -- back to the original M2 value

// Brain-driven flight, as a continuous throttle rather than a keyboard tap:
// BASE_LIFT is a hand-set physics constant (like GRAVITY itself), not
// anything the brain computes -- it's what lets the bird settle near a
// steady altitude in open air the way a hovering insect's sustained
// wingbeat would, rather than free-falling between every pipe.
//
// CLIMB_GAIN converts the brain's real DNp01_R-minus-DNp01_L differential
// (see brain.js -- the reoriented, genuinely directional readout) into
// thrust ABOVE or BELOW that baseline: right-eye-dominant (floor threat)
// pushes thrust up, left-eye-dominant (ceiling threat) pulls it down. This
// is new since the reorientation -- the old pooled-urgency readout could
// only ever add thrust, never subtract it, because it had no sense of
// which way was safe.
// The reoriented threat gating (see EDGE_MARGIN_DEG in brain.js) only
// fires close to an actual edge, so climb sits at 0 for long stretches
// between pipes -- unlike the old wide/loose gate, which fired almost
// continuously and could lean on a low baseline. With infrequent
// corrections, BASE_LIFT has to hold the bird near a real hover by
// itself between them (matching the "a fly sets a sustained altitude,
// not a fall-then-tap rhythm" idea from earlier); a low baseline let it
// sink to the ground before the next correction ever arrived.
const BASE_LIFT = GRAVITY * 0.92;
const CLIMB_GAIN = 200;
// A real wing muscle has a maximum output -- without a cap, climb signal
// and altitude can reinforce each other and run away with no limit.
const MAX_THRUST = GRAVITY * 1.6;
// Plain linear drag, opposing whatever velocity currently exists in either
// direction (a standard physical damping term, not a directional fix) --
// without it, a brief burst of thrust can build up enough climb momentum
// to keep coasting through the wall's silhouette long after the burst
// itself has ended, re-triggering more thrust before it fully clears.
const DRAG = 2.2;

let state; // 'ready' | 'playing' | 'dead'

function reset() {
  state = 'ready';
  bird = { y: H / 2, vy: 0 };
  pipes = [];
  distSinceLastPipe = PIPE_SPACING; // spawn one immediately
  score = 0;
  if (typeof resetBrain === 'function') resetBrain();
}

let bird, pipes, distSinceLastPipe, score;
reset();

function spawnPipe() {
  const margin = 60;
  const gapY = margin + Math.random() * (H - GROUND_H - margin * 2 - PIPE_GAP);
  pipes.push({ x: W, gapY, scored: false });
}

function flap() {
  if (state === 'ready') state = 'playing';
  if (state === 'playing') bird.vy = FLAP_VY;
}

function circleRectOverlap(cx, cy, r, rx, ry, rw, rh) {
  const nearestX = Math.max(rx, Math.min(cx, rx + rw));
  const nearestY = Math.max(ry, Math.min(cy, ry + rh));
  const dx = cx - nearestX, dy = cy - nearestY;
  return dx * dx + dy * dy < r * r;
}

function update(dt) {
  if (state !== 'playing') return;

  bird.vy += (GRAVITY - brainThrust - DRAG * bird.vy) * dt;
  bird.y += bird.vy * dt;

  distSinceLastPipe += PIPE_SPEED * dt;
  if (distSinceLastPipe >= PIPE_SPACING) {
    distSinceLastPipe -= PIPE_SPACING;
    spawnPipe();
  }

  for (const p of pipes) {
    p.x -= PIPE_SPEED * dt;
    if (!p.scored && p.x + PIPE_W < BIRD_X) { p.scored = true; score++; }
  }
  pipes = pipes.filter(p => p.x + PIPE_W > -5);

  if (bird.y - BIRD_R < 0 || bird.y + BIRD_R > H - GROUND_H) { state = 'dead'; return; }
  for (const p of pipes) {
    const topH = p.gapY;
    const botY = p.gapY + PIPE_GAP;
    if (circleRectOverlap(BIRD_X, bird.y, BIRD_R, p.x, 0, PIPE_W, topH) ||
        circleRectOverlap(BIRD_X, bird.y, BIRD_R, p.x, botY, PIPE_W, H - GROUND_H - botY)) {
      state = 'dead';
      return;
    }
  }
}

function draw() {
  ctx.clearRect(0, 0, W, H);

  ctx.fillStyle = '#3fb950';
  for (const p of pipes) {
    ctx.fillRect(p.x, 0, PIPE_W, p.gapY);
    ctx.fillRect(p.x, p.gapY + PIPE_GAP, PIPE_W, H - GROUND_H - (p.gapY + PIPE_GAP));
  }

  ctx.fillStyle = '#21262d';
  ctx.fillRect(0, H - GROUND_H, W, GROUND_H);

  ctx.save();
  ctx.translate(BIRD_X, bird.y);
  ctx.rotate(Math.max(-0.5, Math.min(1.0, bird.vy / 600)));
  ctx.fillStyle = '#f0f6fc';
  ctx.beginPath();
  ctx.arc(0, 0, BIRD_R, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  ctx.fillStyle = '#c9d1d9';
  ctx.font = '28px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(score, W / 2, 60);

  if (state === 'ready') {
    ctx.font = '18px monospace';
    ctx.fillText('space / click to start', W / 2, H / 2 - 40);
  } else if (state === 'dead') {
    ctx.font = '24px monospace';
    ctx.fillText('game over', W / 2, H / 2 - 20);
    ctx.font = '16px monospace';
    ctx.fillText('click to restart', W / 2, H / 2 + 10);
  }
}

// The spectator view shows the pipe as a flat wall at some x-distance. The
// fly doesn't experience "distance" as a number on screen -- it experiences
// an angle. A gap of fixed physical height subtends a small angle far away
// and a huge angle up close: that growth in angle *is* looming. So for each
// edge of the gap we compute its elevation angle from the bird's eye given
// how far away (depth) and how far up/down (relative to the bird) it is,
// then map that angle onto a row of the FFV canvas.
function elevationDeg(relY, depth) {
  return Math.atan2(-relY, depth) * (180 / Math.PI);
}

function elevationToPixelY(elevDeg) {
  const frac = (elevDeg + FFV_FOV_DEG / 2) / FFV_FOV_DEG; // 0 (bottom of FOV) .. 1 (top of FOV)
  return (1 - frac) * FFV_H;
}

function nearestPipeAhead() {
  let nearest = null;
  for (const p of pipes) {
    if (p.x + PIPE_W < BIRD_X) continue; // already passed
    if (!nearest || p.x < nearest.x) nearest = p;
  }
  return nearest;
}

// Shared by drawFFV (what a human sees) and visualDrive in brain.js (what
// the brain is actually fed): whether the top/bottom edges of the gap have
// crept far enough into the forward flight-path cone to count as a real
// ceiling/floor threat. See EDGE_MARGIN_DEG in brain.js for why the sign
// crossing at 0, not a wide unsigned band, is what makes this directional.
function computeThreats(p) {
  if (!p) return { topElev: 0, botElev: 0, ceilingThreat: false, floorThreat: false };
  const depth = Math.max(1, p.x - BIRD_X);
  const topElev = elevationDeg(p.gapY - bird.y, depth);
  const botElev = elevationDeg(p.gapY + PIPE_GAP - bird.y, depth);
  return {
    topElev, botElev,
    ceilingThreat: topElev < EDGE_MARGIN_DEG,
    floorThreat: botElev > -EDGE_MARGIN_DEG,
  };
}

// The wall geometry rendered here (top/bottom bars) is real and honest --
// it's genuinely what the gap looks like from the bird's eye. But since
// the reorientation, that is NOT how the brain actually reads the scene:
// "wall above" drives the LEFT eye's real neurons, "wall below" drives the
// RIGHT eye's, and the climb decision comes from comparing DNp01_L vs
// DNp01_R (see brain.js). The two side strips make that encoding visible
// -- they light up exactly when computeThreats() says that eye is being
// driven, which is the actual input to the brain this frame.
function drawFFV() {
  ffvCtx.clearRect(0, 0, FFV_W, FFV_H);
  ffvCtx.fillStyle = '#0d1117';
  ffvCtx.fillRect(0, 0, FFV_W, FFV_H);

  const p = nearestPipeAhead();
  const { topElev, botElev, ceilingThreat, floorThreat } = computeThreats(p);
  if (p && state !== 'dead') {
    const half = FFV_FOV_DEG / 2;
    const topEdgeY = elevationToPixelY(Math.min(half, Math.max(-half, topElev)));
    const botEdgeY = elevationToPixelY(Math.min(half, Math.max(-half, botElev)));

    ffvCtx.fillStyle = '#3fb950';
    ffvCtx.fillRect(0, 0, FFV_W, topEdgeY);
    ffvCtx.fillRect(0, botEdgeY, FFV_W, FFV_H - botEdgeY);
  }

  ffvCtx.strokeStyle = '#30363d';
  ffvCtx.beginPath();
  ffvCtx.moveTo(0, FFV_H / 2); ffvCtx.lineTo(FFV_W, FFV_H / 2); // horizon line, straight ahead
  ffvCtx.stroke();

  const active = state !== 'dead';
  const stripW = 14;
  ffvCtx.fillStyle = active && ceilingThreat ? '#f0f6fc' : '#21262d';
  ffvCtx.fillRect(0, 0, stripW, FFV_H);
  ffvCtx.fillStyle = active && floorThreat ? '#f0f6fc' : '#21262d';
  ffvCtx.fillRect(FFV_W - stripW, 0, stripW, FFV_H);

  ffvCtx.fillStyle = '#8b949e';
  ffvCtx.font = '10px monospace';
  ffvCtx.textAlign = 'left';
  ffvCtx.save();
  ffvCtx.translate(10, FFV_H / 2 + 20);
  ffvCtx.rotate(-Math.PI / 2);
  ffvCtx.fillText('L eye -> ceiling threat', 0, 0);
  ffvCtx.restore();
  ffvCtx.save();
  ffvCtx.translate(FFV_W - 4, FFV_H / 2 + 20);
  ffvCtx.rotate(-Math.PI / 2);
  ffvCtx.fillText('R eye -> floor threat', 0, 0);
  ffvCtx.restore();
}

let brainControl = true;
let simClockMs = 0;
let brainThrust = 0;

let lastT = performance.now();
function frame(now) {
  const dt = Math.min((now - lastT) / 1000, 1 / 30);
  lastT = now;

  simClockMs += dt * 1000;
  if (brain && state === 'playing') {
    const climb = tickBrain(dt * 1000, simClockMs);
    brainThrust = brainControl ? Math.max(0, Math.min(MAX_THRUST, BASE_LIFT + CLIMB_GAIN * climb)) : 0;
  } else {
    brainThrust = 0;
  }

  update(dt);
  draw();
  drawFFV();
  drawBrainViz(brainCanvas, brainCtx, simClockMs);

  ffvCtx.fillStyle = brainControl ? '#3fb950' : '#8b949e';
  ffvCtx.font = '12px monospace';
  ffvCtx.textAlign = 'left';
  ffvCtx.fillText(brainControl ? 'brain control: ON (b to toggle)' : 'brain control: OFF (b to toggle)', 6, FFV_H - 8);

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
loadBrain();

window.addEventListener('keydown', e => {
  if (e.code === 'KeyB') { brainControl = !brainControl; return; }
  if (e.code !== 'Space') return;
  e.preventDefault();
  if (state === 'dead') reset(); else flap();
});
canvas.addEventListener('mousedown', () => { if (state === 'dead') reset(); else flap(); });
