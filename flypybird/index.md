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
