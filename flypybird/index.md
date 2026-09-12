# FlyPyBird
---

## 12/09/26

**The premise:** take a *real* fruit-fly connectome — an actual, measured wiring
diagram of a fly's nervous system — and wire it into a game of Flappy Bird. Game
on the left, the fly's brain lighting up on the right. Can biology dodge the
pipes?

This is a learning project, so I'm writing down what I get *wrong* as much as
what I get right. Day one already corrected a big misconception of mine.

### Misconception #1: a connectome is not a trainable model

I came in picturing this like the old RL-plays-Mario videos: a neural network you
*train* with rewards until it gets good, dopamine for surviving, punishment for
crashing. But a **connectome isn't a network you train — it's frozen anatomy.**
It tells you "neuron A connects to neuron B, this many synapses, excitatory or
inhibitory," and nothing else. It's a wiring diagram, not a set of weights
waiting for gradient descent.

The important consequence, which took a second to sink in: **if I RL-train the
weights "like Mario," I've thrown the fly brain away.** What's left is a generic
neural net that merely happens to be *shaped* like a fly. The entire point — that
real fruit-fly wiring is flying my game — evaporates the moment I start tuning
the synapses.

So the dopamine/reward idea isn't dead, it's just *demoted*. Real flies do learn
via dopamine, at specific synapses in a structure called the **mushroom body** —
but modelling that plasticity is the hard, final milestone, not the MVP.

### The MVP is a fly that REACTS, not one that LEARNS

Here's the reframe. I don't need learning to get a fly through a pipe. Flies have
**dedicated collision-detector neurons** — lobula cells called `LC4` and `LPLC2`
— that fire when something *looms* (grows) in the visual field and drive an
escape/steering response. So I don't hand-wire "walls are scary." I render the
wall so it **looms** in the fly's view, feed it into the real optic-lobe circuit,
and the avoidance is *the actual neurons firing*.

MVP loop: **wall looms in the fly's view → real circuit fires → read a motor
neuron → fly goes up or down.** No learning anywhere. Get the reflex working
end-to-end first.

### A question I got stuck on: do we *discover* which neurons fire, or is it known?

> If we put the looming wall in, do we then *see* which neurons fire for the
> wings — or is that already known for flies?

Both — and the overlap is the whole project:

- **Known (anatomy + literature):** the cast of characters. The fly escape/flight
  pathway is among the best-studied circuits in neuroscience. The connectome
  hands me the wiring explicitly — the looming detectors (`LC4`, `LPLC2`), the
  **Giant Fiber** (`DNp01`, the famous "escape command" neuron that bridges brain
  to nerve cord), and the ~few dozen **wing motoneurons**. I don't have to guess
  where to look.
- **Observed (run the sim):** the *dynamics*. Given *my* wall, at *my* speed, with
  *my* pixel encoding, which of those neurons fire, how hard, in what order — that
  only emerges when I actually run the simulation. That "watch them light up" step
  doubles as my correctness check: loom a wall, and if `LC4 → LPLC2 → Giant Fiber`
  fire in sequence, I've reproduced textbook biology and know my encoding is right.

So I'm not blindly probing — I'm reproducing a known circuit and then watching it
play my game.

### Which fly? The "male CNS" and why it's the harder-but-better choice

The neurons that flap the wings live in the **VNC** (the fly's "spinal cord"), not
the brain — but vision happens in the brain's optic lobes. So the loop *eyes →
wings* has to cross from brain into VNC, and that crossing is done by **descending
neurons**. I went with the **complete male central nervous system connectome**
([Cell, 2026](https://www.cell.com/cell/fulltext/S0092-8674(26)00942-6), ~166k
neurons) because it's a *single connected graph* covering optic lobes + brain +
VNC — my exact loop exists end to end in one dataset. The male VNC on its own
([MANC](https://www.janelia.org/project-team/flyem/manc-connectome), ~23k neurons)
is on [neuPrint](https://neuprint.janelia.org) and downloadable, with the wing
motoneurons already identified.

The catch: there's no ready-made real-time simulator for it (unlike the FlyWire
brain, which has an in-browser one). So I'll **build my own small
leaky-integrate-and-fire sim over a subset** — the vision→escape→flight pathway,
a few thousand neurons, not all 166k. More work, but it's the most educational
part of the whole thing. Stack: **Python** — neuPrint client for the data,
Brian2/NumPy for the simulation.

### The roadmap (each milestone = a checkpoint here)

- **M0** — repo + this post. ✅
- **M1** — *spike the crux:* pull the escape-circuit subgraph, prove I can inject
  input into one neuron and watch it drive another, at game-loop speed. (This is
  the real risk, so it goes first — before any game polish.)
- **M2** — reactive Flappy Bird: scrolling map, gravity, player-controlled first.
- **M3** — the two views: spectator side-view **+** First-Fly-View (looming
  top/bottom bars with a gap).
- **M4** — wire the circuit in: fly-view → visual neurons; motor neuron → up/down.
- **M5** — split-screen brain viz: neurons light up live.
- **M6** — *later:* learning via mushroom-body/dopamine plasticity.
- **M7** — deploy to a watchable site.

Next up: M1, the spike. Gifs to follow once there's something moving.

---

### A glossary, and a live toy neuron circuit you can poke at

Before the spike, it's worth nailing down the vocabulary I've been throwing
around — and, since this is a learning project, actually *building* one of the
smallest possible pieces of it so it stops being an abstraction.

**[Connectome](https://en.wikipedia.org/wiki/Connectome)** — a complete wiring
diagram of a nervous system: every neuron, and every synapse connecting it to
every other neuron, with a strength (synapse count) and a sign. Nothing about
*time* or *activity* is in it — it's a parts list and a netlist, like a circuit
schematic with no power connected yet.

**[Neuron](https://en.wikipedia.org/wiki/Neuron)** — the basic signalling cell.
It receives input from other neurons at synapses, and if that input pushes its
internal voltage high enough, it fires.

**[Spike / action potential](https://en.wikipedia.org/wiki/Action_potential)**
— the brief, stereotyped electrical pulse a neuron fires once its voltage
crosses a threshold. This is the unit of communication in the brain — neurons
don't send graded voltages to each other, they send spikes (or don't).

**[Chemical synapse](https://en.wikipedia.org/wiki/Chemical_synapse), excitatory
vs. inhibitory** — the connection between two neurons, and its *sign*.
Excitatory synapses push the receiving neuron's voltage **up** (more likely to
spike); inhibitory synapses push it **down** (less likely). The connectome
records which is which for every connection — this is not something we get to
choose, it's measured.

**[Descending neuron (DN)](https://en.wikipedia.org/wiki/Efferent_nerve_fiber)**
— a neuron whose cell body and dendrites sit in the brain, but whose axon runs
*down* into the ventral nerve cord (VNC) — literally the wire carrying a
"decision" made in the brain out to the motor circuits that act on it. It's the
bridge between seeing and doing. The
[Giant Fiber (`DNp01`)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10263144/)
is the most famous example in flies — a single spike in it is enough to trigger
the entire jump-and-flight escape sequence.

**A "stereotyped" brain** — the surprising fact that makes any of this possible:
individual neurons in a fly are *anatomically reproducible* across different
flies of the species. `DNp01` isn't "a Giant-Fiber-like neuron this particular
fly happened to grow" — it's the same identifiable cell, in the same place,
doing the same job, in (almost) every fly. That's precisely how neurons in the
[MANC](https://www.janelia.org/project-team/flyem/manc-connectome) dataset
(imaged from one fly) can be matched by name to neurons in the male CNS dataset
(imaged from a *different* fly) — you're not matching serial numbers, you're
matching recognisable characters.

**The looming detectors** — the actual visual cells this project hinges on:
[`LC4`](https://www.virtualflybrain.org/term/lc4-fbbt_00003874/) and
[`LPLC2`](https://www.virtualflybrain.org/term/lplc2-optic-glomerulus-fbbt_00052656/),
lobula neurons that respond selectively to something expanding in the visual
field — i.e. an object on a collision course — and synapse directly onto the
Giant Fiber.

#### A tiny leaky-integrate-and-fire circuit, running live

Here's the smallest circuit that actually demonstrates the ingredients above:
**leak, integrate, fire, and signed synapses.** Four neurons:

- **N0 (sensory)** — the one you stimulate with the button below.
- **N1 (fast excitatory relay)** — gets excited by N0, quickly.
- **N2 (slow inhibitory relay)** — also gets excited by N0, but reacts more
  sluggishly, and its output is *inhibitory*.
- **N3 (motor)** — our stand-in for "the wing neuron." It gets excited by N1
  and inhibited by N2. Its firing rate is the number I'd eventually read out
  as "how hard to flap."

Watch what happens as you turn the stimulus up: at low strength, nothing
downstream fires at all. Push past a threshold and N1's *fast* excitation
reaches N3 before N2's *slow* inhibition has caught up — so N3 gets a real,
sustained response instead of being cancelled out immediately. This
"fast-excite / slow-inhibit" motif is a real, common one in real nervous
systems for exactly this reason: it lets a circuit respond to changes rather
than just sitting at some cancelled-out steady state — which is the whole game
when the thing you actually care about is a wall that's *looming*, not a wall
that's simply *there*.

To be clear about what this toy is **not**: it is not LC4/LPLC2/the Giant Fiber,
the constants aren't fit to any biological data, and it's simulated with a
plain fixed-step Euler integrator, not anything resembling Brian2. It exists
purely so the words "leak," "integrate," "fire," "excitatory," and "inhibitory"
have a picture attached to them before M1.

<div class="lif-demo">
  <canvas id="lifCanvas" width="700" height="340"></canvas>
  <div class="lif-controls">
    <button id="lifStimBtn">⚡ Stimulate N0</button>
    <label>Strength
      <input type="range" id="lifStrength" min="0" max="60" step="1" value="35">
      <span id="lifStrengthVal">35</span>
    </label>
  </div>
  <div class="lif-readout">
    N3 (motor) firing rate — the "wing neuron" proxy:
    <strong id="lifRate">0.0 Hz</strong>
  </div>
</div>

<style>
.lif-demo { border:1px solid #30363d; border-radius:8px; padding:1rem; margin:1.5rem 0; background:#0d1117; }
.lif-demo canvas { width:100%; max-width:700px; display:block; margin:0 auto; background:#05070a; border-radius:6px; }
.lif-controls { display:flex; gap:1.25rem; align-items:center; justify-content:center; margin-top:0.75rem; flex-wrap:wrap; color:#c9d1d9; font-size:0.9rem; }
.lif-controls button { background:#238636; color:#fff; border:none; padding:0.5rem 1rem; border-radius:6px; cursor:pointer; font-size:0.9rem; }
.lif-controls button:hover { background:#2ea043; }
.lif-readout { text-align:center; margin-top:0.6rem; color:#c9d1d9; font-size:0.95rem; }
.lif-readout strong { color:#58a6ff; }
</style>

<script>
(function(){
  const canvas = document.getElementById('lifCanvas');
  const ctx = canvas.getContext('2d');

  const vRest = -70, vThresh = -50, vReset = -65, vSpike = 10;

  function makeNeuron(name, x, y, tau) {
    return { name, x, y, tau, v: vRest, Iinj: 0, wasSpike: false, spikedThisStep: false, history: [] };
  }

  const N0 = makeNeuron('N0 sensory',   110, 170, 12);
  const N1 = makeNeuron('N1 excitatory', 380, 90,  8);
  const N2 = makeNeuron('N2 inhibitory', 380, 250, 30);
  const N3 = makeNeuron('N3 motor',      620, 170, 12);
  const neurons = [N0, N1, N2, N3];

  // from -> to, weight (mV kick on arrival, sign = excitatory/inhibitory), delay (ms)
  const synapses = [
    { from: N0, to: N1, weight: 22,  delay: 4 },
    { from: N0, to: N2, weight: 12,  delay: 4 },
    { from: N1, to: N3, weight: 20,  delay: 6 },
    { from: N2, to: N3, weight: -22, delay: 6 },
  ];

  let pending = [];   // in-flight synaptic events: { time, synapse }
  let inFlightDots = []; // for drawing: { synapse, tStart, tArrive }
  let simTime = 0;
  let n3SpikeTimes = [];
  let stimUntil = -1;
  let strength = 35;

  function stepSim(dt) {
    simTime += dt;
    N0.Iinj = (simTime <= stimUntil) ? strength : 0;

    // deliver any synaptic events whose arrival time has passed
    pending = pending.filter(ev => {
      if (ev.time <= simTime) { ev.synapse.to.v += ev.synapse.weight; return false; }
      return true;
    });

    for (const n of neurons) {
      if (n.wasSpike) { n.v = vReset; n.wasSpike = false; }
      // the LIF equation: leak back to rest, plus injected current, scaled by dt/tau
      n.v += ((vRest - n.v) + n.Iinj) * (dt / n.tau);
      n.v = Math.max(n.v, -95);
      n.spikedThisStep = false;
      if (n.v >= vThresh) { n.v = vSpike; n.spikedThisStep = true; n.wasSpike = true; }
      n.history.push(n.v);
      if (n.history.length > 260) n.history.shift();
    }

    for (const s of synapses) {
      if (s.from.spikedThisStep) {
        pending.push({ time: simTime + s.delay, synapse: s });
        inFlightDots.push({ synapse: s, tStart: simTime, tArrive: simTime + s.delay });
      }
    }
    inFlightDots = inFlightDots.filter(d => d.tArrive > simTime);

    if (N3.spikedThisStep) n3SpikeTimes.push(simTime);
    n3SpikeTimes = n3SpikeTimes.filter(t => simTime - t < 1000);
  }

  function colourForV(v) {
    const f = Math.max(0, Math.min(1, (v - vRest) / (vThresh - vRest)));
    const r = Math.round(40 + f * 200), g = Math.round(80 + f * 100), b = Math.round(160 - f * 120);
    return `rgb(${r},${g},${b})`;
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const s of synapses) {
      ctx.strokeStyle = s.weight > 0 ? '#3fb950' : '#f85149';
      ctx.lineWidth = Math.max(1, Math.abs(s.weight) / 22 * 3);
      ctx.beginPath();
      ctx.moveTo(s.from.x, s.from.y);
      ctx.lineTo(s.to.x, s.to.y);
      ctx.stroke();
    }
    for (const d of inFlightDots) {
      const f = (simTime - d.tStart) / (d.tArrive - d.tStart);
      const x = d.synapse.from.x + (d.synapse.to.x - d.synapse.from.x) * f;
      const y = d.synapse.from.y + (d.synapse.to.y - d.synapse.from.y) * f;
      ctx.fillStyle = d.synapse.weight > 0 ? '#3fb950' : '#f85149';
      ctx.beginPath(); ctx.arc(x, y, 4, 0, 7); ctx.fill();
    }

    for (const n of neurons) {
      const spiking = n.v === vSpike;
      ctx.beginPath();
      ctx.arc(n.x, n.y, 26, 0, 7);
      ctx.fillStyle = spiking ? '#f0f6fc' : colourForV(n.v);
      if (spiking) { ctx.shadowColor = '#f0f6fc'; ctx.shadowBlur = 20; }
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.strokeStyle = '#30363d'; ctx.lineWidth = 2; ctx.stroke();

      ctx.fillStyle = '#8b949e'; ctx.font = '11px monospace'; ctx.textAlign = 'center';
      ctx.fillText(n.name, n.x, n.y - 36);

      const hw = 42, hh = 24, hx = n.x - hw / 2, hy = n.y + 40;
      ctx.strokeStyle = '#21262d'; ctx.strokeRect(hx, hy, hw, hh);
      ctx.beginPath();
      n.history.forEach((v, i) => {
        const x = hx + (i / 260) * hw;
        const y = hy + hh - ((v - (-95)) / (vSpike - (-95))) * hh;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 1; ctx.stroke();
    }
  }

  let lastT = performance.now();
  function frame(now) {
    let elapsed = Math.min(now - lastT, 50);
    lastT = now;
    while (elapsed > 0) { stepSim(1); elapsed -= 1; }
    draw();
    document.getElementById('lifRate').textContent = n3SpikeTimes.length.toFixed(1) + ' Hz';
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  const slider = document.getElementById('lifStrength');
  const sliderVal = document.getElementById('lifStrengthVal');
  slider.addEventListener('input', () => { strength = +slider.value; sliderVal.textContent = slider.value; });
  document.getElementById('lifStimBtn').addEventListener('click', () => { stimUntil = simTime + 300; });
})();
</script>

<details markdown="1">
<summary>Show the code</summary>

The block above is the entire demo — no libraries, just a canvas and this
loop. The core of it is the LIF update:

```js
// the LIF equation: leak back to rest, plus injected current, scaled by dt/tau
n.v += ((vRest - n.v) + n.Iinj) * (dt / n.tau);

if (n.v >= vThresh) {
  n.v = vSpike;        // fire
  n.spikedThisStep = true;
}
// ...next step: n.v = vReset
```

And synapses are just delayed voltage kicks, positive for excitatory, negative
for inhibitory, queued and delivered after their conduction delay:

```js
if (s.from.spikedThisStep) {
  pending.push({ time: simTime + s.delay, synapse: s });
}
// later, once time has passed:
if (ev.time <= simTime) { ev.synapse.to.v += ev.synapse.weight; }
```

That's it — the whole vocabulary (leak, integrate, fire, excitatory/inhibitory
synapse, conduction delay) in about 40 lines. M1 is the same idea, scaled up
to a few thousand real neurons with real weights instead of four made-up ones.

</details>
