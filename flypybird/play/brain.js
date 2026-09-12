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
    layout: null, // [{x,y}] per neuron, computed once against the brainviz canvas
  };
  console.log(`brain loaded: ${n} neurons`);
}

// Three columns, laid out left-to-right in the same order the real signal
// actually flows: eye -> Giant Fiber circuit -> wing/jump muscles. Neurons
// of the same type are grouped into one box and packed into a square-ish
// grid inside it -- this is a circuit diagram, not an anatomical map (we
// don't have 3D positions for most of these types), so position here means
// "which population this is", not "where in the fly this neuron sits".
const STAGE_TYPES = [
  VISUAL_TYPES,
  ['DNp01', 'DNp03', 'GFC2', 'GFC3', 'GFC4'],
  WING_MN_TYPES,
];

function computeLayout(canvasW, canvasH) {
  const layout = new Array(brain.n);
  const groupLabels = [];
  const colW = canvasW / STAGE_TYPES.length;
  STAGE_TYPES.forEach((typesInStage, col) => {
    const colX0 = col * colW + 10;
    const colW2 = colW - 20;
    const counts = typesInStage.map(t => brain.types.filter(x => x === t).length);
    const totalRows = counts.reduce((a, b) => a + Math.ceil(Math.sqrt(b)), 0) || 1;
    let y0 = 10;
    typesInStage.forEach((t) => {
      const idxs = [];
      brain.types.forEach((x, i) => { if (x === t) idxs.push(i); });
      const count = idxs.length;
      const cols = Math.max(1, Math.min(count, Math.ceil(Math.sqrt(count))));
      const rows = Math.ceil(count / cols);
      const boxH = (canvasH - 20) * (Math.ceil(Math.sqrt(count)) / totalRows);
      const cellW = colW2 / cols;
      const cellH = Math.max(4, boxH / rows);
      groupLabels.push({ text: t, x: colX0, y: y0 });
      idxs.forEach((i, k) => {
        const r = Math.floor(k / cols), c = k % cols;
        layout[i] = { x: colX0 + c * cellW + cellW / 2, y: y0 + 12 + r * cellH + cellH / 2 };
      });
      y0 += boxH + 24;
    });
  });
  brain.layout = layout;
  brain.groupLabels = groupLabels;
}

function drawBrainViz(canvas, ctx, nowMs) {
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  if (!brain) return;
  if (!brain.layout) computeLayout(canvas.width, canvas.height);

  ctx.fillStyle = '#8b949e';
  ctx.font = '10px monospace';
  ctx.textAlign = 'left';
  for (const g of brain.groupLabels) ctx.fillText(g.text, g.x, g.y + 8);

  for (let i = 0; i < brain.n; i++) {
    const pos = brain.layout[i];
    if (!pos) continue;
    const age = nowMs - brain.lastSpikeMs[i];
    const glow = Math.max(0, 1 - age / 300); // fades over 300ms
    const r = 2 + glow * 2.5;
    if (glow > 0.02) {
      ctx.fillStyle = brain.isWingMN[i] ? `rgba(240,246,252,${glow})` : `rgba(63,185,80,${glow})`;
    } else {
      ctx.fillStyle = '#21262d';
    }
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, r, 0, 7);
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
