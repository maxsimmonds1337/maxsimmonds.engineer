// The M4 brain: the same LIF sim from src/spike_sim.py, ported to run
// live in the browser against the real male-CNS subgraph (data exported
// once by src/export_brain_data.py -- no Python at runtime).
//
// Steering, reoriented: the wing/jump motoneuron pool (read by earlier
// milestones) is real but non-directional -- DNp01, GFC2/3/4 and DNp03 all
// wash out to bilaterally symmetric by the time they reach wing muscle, so
// reading "how much are the wings firing" can only ever say "something is
// looming", never "which way is safe" (measured and written up in M4 /
// M4-revisited). But LC4/LPLC2 -> DNp01, the FIRST hop of the escape
// circuit, is 100% ipsilateral in the real connectome (verified via the
// somaSide annotation: left-eye input drives only left DNp01, right-eye
// input drives only right DNp01, zero cross-talk). So instead of chasing a
// directional pathway all the way to motor output, we read the signal one
// stage earlier, at the descending command neuron itself, before it
// symmetrizes. "Wall above" is rendered as looming in the LEFT eye (real
// somaSide-tagged LC4/LPLC2 neurons), "wall below" as looming in the RIGHT
// eye, and the climb decision is DNp01_R activity minus DNp01_L activity.
// This is a real, verified anatomical asymmetry doing real work -- more
// honest than the old elevation-proxy readout -- but it's still a chosen
// left/right encoding of an up/down game, not the fly's own natural
// steering computation (that lives further upstream, in central-complex
// circuitry -- LAL/PS neurons via AOTU -- that isn't in this subgraph).

const V_REST = -70, V_THRESH = -50, V_RESET = -65, V_SPIKE = 10, V_FLOOR = -95;
const TAU = 15;          // ms, membrane time constant (chosen, not measured)
const SYN_SCALE = 0.3;   // mV per synapse count (chosen, not measured)
// M1 found ~25-30 is the minimum drive for a single LC4/LPLC2 neuron to
// spike at all; well above that (e.g. 160), one driven neuron fires on
// almost every step and can eventually force the cascade through by
// repetition alone, which defeats the point -- the alarm should require
// real convergence (many neurons actually seeing wall at once), not
// persistence from a handful. Staying close to the individual threshold
// keeps that convergence requirement real.
const VISUAL_STIM = 28;

const VISUAL_TYPES = ['LC4', 'LPLC2', 'LPLC1', 'LPLC4', 'LC22', 'LC23'];
const WING_MN_TYPES = [
  'TTMn', 'DLMn c-f', 'DLMn a, b', 'ps1 MN', 'b2 MN',
  'b3 MN', 'hg1 MN', 'hg2 MN', 'i1 MN', 'i2 MN', 'iii1 MN', 'tpn MN',
];
// Widening the visual population (626 neurons vs the original 311) raised
// the circuit's baseline/ambient firing rate enough that a 150ms window
// almost never emptied back out once a first burst triggered it -- the
// rising-edge detector fired exactly once, ever, per game. A shorter
// window that actually reflects "right now" is also what makes this a
// sensible continuous throttle rather than a stale, slow-moving average.
const ALARM_WINDOW_MS = 40;

// topElev/botElev (see elevationDeg() in game.js) are signed by construction:
// topElev is positive while the bird is safely below the gap's top edge and
// crosses toward zero/negative only once the bird has actually drifted up
// toward (or past) the ceiling; botElev is negative while safely above the
// bottom edge and crosses toward zero/positive only when drifting down
// toward the floor. A small positive margin below/above zero gives an early
// warning before the literal collision boundary. This replaced a first
// attempt using a wide, unsigned +-20deg "is a wall anywhere in the fovea"
// gate, which fired almost identically on both sides for any centered,
// even-distant pipe -- swamping the real directional signal with population
// -size noise instead of reflecting the bird's actual position in the gap.
const EDGE_MARGIN_DEG = 20;

let brain = null;

async function loadBrain() {
  const res = await fetch('brain_data.json');
  const data = await res.json();
  const n = data.bodyIds.length;
  brain = {
    n,
    types: data.types,
    W: data.W,                      // n x n, W[i][j] = signed weight i->j
    preferredElevDeg: data.preferredElevDeg,
    side: data.side,                // real somaSide annotation, 'L' | 'R'
    v: new Float64Array(n).fill(V_REST),
    wasSpike: new Uint8Array(n),
    prevSpiked: new Float64Array(n),
    isWingMN: data.types.map(t => WING_MN_TYPES.includes(t)),
    isVisual: data.types.map(t => VISUAL_TYPES.includes(t)),
    isDNp01L: data.types.map((t, i) => t === 'DNp01' && data.side[i] === 'L'),
    isDNp01R: data.types.map((t, i) => t === 'DNp01' && data.side[i] === 'R'),
    dnp01LSpikeTimes: [],
    dnp01RSpikeTimes: [],
    lastSpikeMs: new Float64Array(n).fill(-1e9),
    pos3d: data.pos3d,               // real measured soma [x,y,z] per neuron, or null
    region: data.region,             // 'brain' | 'vnc', from real somaNeuromere
    pos3dNorm: null,                 // centered/scaled once against the population
  };
  prepare3D();
  console.log(`brain loaded: ${n} neurons`);
}

// Real anatomy, not a synthetic layout: centers and scales every neuron's
// actual measured soma position once, so the viz can rotate a genuine 3D
// point cloud shaped like the real brain + VNC rather than an artificial
// left-to-right circuit diagram.
function prepare3D() {
  const valid = brain.pos3d.filter(p => p);
  const n = valid.length;
  const cx = valid.reduce((a, p) => a + p[0], 0) / n;
  const cy = valid.reduce((a, p) => a + p[1], 0) / n;
  const cz = valid.reduce((a, p) => a + p[2], 0) / n;
  const radii = valid.map(p => {
    const dx = p[0] - cx, dy = p[1] - cy, dz = p[2] - cz;
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
  }).sort((a, b) => a - b);
  // A handful of real somas sit far outside the main cluster (true outliers,
  // not a data error) -- normalizing by the true max compresses the other
  // 90%+ of neurons into a tiny central blob. Scaling by the 90th
  // percentile instead fills the canvas with the bulk of the population;
  // the outliers just render past the nominal unit radius, still visible.
  const scaleR = radii[Math.floor(radii.length * 0.9)] || 1;
  brain.pos3dNorm = brain.pos3d.map(p => p ? [(p[0] - cx) / scaleR, (p[1] - cy) / scaleR, (p[2] - cz) / scaleR] : null);
}

// A fixed viewing angle, not a live rotation -- a slow auto-spin looked
// interesting but made it harder to actually read the anatomy at a
// glance. 0 radians is the raw x/z orientation the real soma coordinates
// come in, which already happens to face the point cloud roughly
// head-on: the two optic lobes separate cleanly left/right and the VNC
// cluster sits legibly below, so there was no reason to rotate away from it.
const STATIC_ANGLE_RAD = 0;

// Renders every neuron at its own real, measured soma position (see
// prepare3D), projected with simple weak perspective from a fixed angle.
// Brain neurons cluster near the top of the point cloud, VNC neurons
// (thoracic-neuromere somas -- the real wing motoneurons live here) near
// the bottom, because that's genuinely where their cell bodies sit -- this
// replaced an earlier synthetic left-to-right circuit diagram, which was
// clearer about signal flow but told you nothing about actual anatomy.
function project3D(p, angleRad, canvasW, canvasH) {
  const [x, y, z] = p;
  const cos = Math.cos(angleRad), sin = Math.sin(angleRad);
  const rx = x * cos - z * sin;
  const rz = x * sin + z * cos;
  const focal = 3.2; // world units from camera to origin; bigger = flatter perspective
  const persp = focal / (focal + rz);
  const scale = Math.min(canvasW, canvasH) * 0.34;
  return {
    x: canvasW / 2 + rx * scale * persp,
    y: canvasH / 2 + y * scale * persp + canvasH * 0.06, // nudge down: leaves room for the "brain" label
    depth: rz,
    persp,
  };
}

function drawBrainViz(canvas, ctx, nowMs) {
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  if (!brain || !brain.pos3dNorm) return;

  const order = [];
  for (let i = 0; i < brain.n; i++) {
    const p = brain.pos3dNorm[i];
    if (!p) continue;
    order.push({ i, proj: project3D(p, STATIC_ANGLE_RAD, canvas.width, canvas.height) });
  }
  order.sort((a, b) => b.proj.depth - a.proj.depth); // back-to-front (painter's algorithm)

  ctx.fillStyle = '#8b949e';
  ctx.font = '10px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('brain', canvas.width / 2, 14);
  ctx.fillText('VNC', canvas.width / 2, canvas.height - 6);

  for (const { i, proj } of order) {
    const age = nowMs - brain.lastSpikeMs[i];
    const glow = Math.max(0, 1 - age / 300); // fades over 300ms
    const baseR = (brain.region[i] === 'vnc' ? 1.8 : 1.3) * proj.persp;
    const r = baseR + glow * 2.8 * proj.persp;
    if (glow > 0.02) {
      ctx.fillStyle = brain.isWingMN[i] ? `rgba(240,246,252,${glow})` : `rgba(63,185,80,${glow})`;
    } else {
      // ghosted: quiet neurons fade almost into the background so the ones
      // actually spiking are what draws the eye, rather than the resting
      // population reading as "always lit up" and burying the signal.
      ctx.fillStyle = brain.region[i] === 'vnc' ? 'rgba(224,155,90,0.12)' : 'rgba(90,140,224,0.1)';
    }
    ctx.beginPath();
    ctx.arc(proj.x, proj.y, Math.max(0.6, r), 0, 7);
    ctx.fill();
  }
}

// Given the current nearest pipe (or null), decide per-visual-neuron drive.
// Reoriented steering: rather than assigning drive by each neuron's
// (proxy, uncertain) preferred elevation, we assign it by real, verified
// somaSide -- "wall above" (the ceiling pipe intruding on the forward
// flight-path cone) drives the LEFT eye, "wall below" drives the RIGHT
// eye. Same elevationDeg()/FOVEA_HALF_DEG geometry as before decides
// *whether* each threat is close enough to matter; side decides *which*
// population of real neurons carries that signal.
function visualDrive(p) {
  const drive = new Float64Array(brain.n);
  if (!p) return drive;
  const { ceilingThreat, floorThreat } = computeThreats(p); // shared with drawFFV in game.js
  if (!ceilingThreat && !floorThreat) return drive;
  for (let i = 0; i < brain.n; i++) {
    if (!brain.isVisual[i]) continue;
    if (ceilingThreat && brain.side[i] === 'L') drive[i] = VISUAL_STIM;
    if (floorThreat && brain.side[i] === 'R') drive[i] = VISUAL_STIM;
  }
  return drive;
}

// Advance the brain by one 1ms step. Structurally identical to
// spike_sim.py: continuous leak+injection, then an instantaneous
// synaptic kick (not scaled by dt/tau -- see the M1 writeup for why
// that distinction matters).
function stepBrain(drive) {
  const { n, v, wasSpike, prevSpiked, W } = brain;
  for (let i = 0; i < n; i++) {
    if (wasSpike[i]) { v[i] = V_RESET; wasSpike[i] = 0; }
    v[i] += ((V_REST - v[i]) + drive[i]) * (1 / TAU);
  }
  for (let j = 0; j < n; j++) {
    let syn = 0;
    for (let i = 0; i < n; i++) { if (prevSpiked[i]) syn += prevSpiked[i] * W[i][j]; }
    v[j] += syn * SYN_SCALE;
    if (v[j] < V_FLOOR) v[j] = V_FLOOR;
  }
  for (let i = 0; i < n; i++) {
    if (v[i] >= V_THRESH) { v[i] = V_SPIKE; wasSpike[i] = 1; prevSpiked[i] = 1; }
    else prevSpiked[i] = 0;
  }
}

function resetBrain() {
  if (!brain) return;
  brain.v.fill(V_REST);
  brain.wasSpike.fill(0);
  brain.prevSpiked.fill(0);
  brain.dnp01LSpikeTimes = [];
  brain.dnp01RSpikeTimes = [];
}

// Run the brain forward by dtMs of simulated time (in 1ms substeps,
// matching the FFV/pipe state at the start of this game frame), and
// return a signed climb signal: right DNp01 activity minus left DNp01
// activity, over a short trailing window.
//
// Continuous throttle, not a discrete tap -- a real fly doesn't decide
// once per pipe, it holds a sustained wingbeat and modulates it. Reading
// DNp01_R - DNp01_L (rather than pooled wing-MN spike count, as earlier
// milestones did) is what makes this signed and directional: positive
// means "right eye alarmed -> floor threat -> climb", negative means
// "left eye alarmed -> ceiling threat -> let it sink".
function tickBrain(dtMs, nowMs) {
  if (!brain) return 0;
  const p = nearestPipeAhead();
  const drive = visualDrive(p);
  const steps = Math.max(1, Math.round(dtMs));
  for (let s = 0; s < steps; s++) {
    stepBrain(drive);
    for (let i = 0; i < brain.n; i++) {
      if (brain.wasSpike[i]) {
        brain.lastSpikeMs[i] = nowMs;
        if (brain.isDNp01L[i]) brain.dnp01LSpikeTimes.push(nowMs);
        if (brain.isDNp01R[i]) brain.dnp01RSpikeTimes.push(nowMs);
      }
    }
  }
  brain.dnp01LSpikeTimes = brain.dnp01LSpikeTimes.filter(t => nowMs - t < ALARM_WINDOW_MS);
  brain.dnp01RSpikeTimes = brain.dnp01RSpikeTimes.filter(t => nowMs - t < ALARM_WINDOW_MS);
  return brain.dnp01RSpikeTimes.length - brain.dnp01LSpikeTimes.length;
}
