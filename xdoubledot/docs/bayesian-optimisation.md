---
layout: xdoubledot
title: Bayesian Optimisation — Geometry Design
---

# Bayesian Optimisation for HET Geometry — What It Is and Why We Use It

## The three optimisation tools in Aegis

Aegis uses three fundamentally different optimisation approaches for three different tasks:

| Task | Approach | Why |
|------|----------|-----|
| Find optimal coil *currents* in real time (runtime control) | Reinforcement Learning (AURORA v1) | Sequential control problem; agent makes many decisions per episode |
| Find optimal pole *geometry* offline (design-time) | **Bayesian Optimisation** | Expensive function, few evaluations, continuous parameters |
| Exhaustive check of a small 2D geometry space | Grid sweep (`pole_geometry_sweep.py`) | 2D is tractable; grid sweep is simple and provably complete |

---

## Why we can't just grid-sweep geometry

Grid search scales as O(n^d), where d = number of design variables and n = grid points per axis.

With the geometry variables we care about:

| Variable | Sensible range | Why it matters |
|----------|---------------|----------------|
| inner_pole_extension | 0–1 (relative units) | Determines whether field lines graze the BN wall ("90-degree lip") |
| outer_pole_taper / flux-matched profile | continuous | Controls outer wall shielding condition |
| Channel length / width ratio | 3–5 × channel_width | Affects ionisation zone depth, wall area |
| BN wall thickness | 0.5–2 mm | Lifetime vs performance trade-off |
| Coil z-position (trim) | varies | Axial gradient range |

Five parameters at 10 grid points each = 10^5 = **100,000 FD solver runs**. Each FD solve takes ~1–2 seconds. That's **27–55 hours** of compute, just for a coarse 10-point grid.

At 20 points per axis: 20^5 = **3.2 million runs** — clearly infeasible.

---

## Why RL doesn't work for geometry

RL is designed for **sequential decision problems** — the agent takes actions over time, observes a reward, and learns a policy. This makes sense for coil current control: the agent adjusts currents 1,000 times per second, observing the plasma state after each step.

Geometry optimisation is **not sequential**. There is no "policy" to learn — it's a single-shot decision: pick geometry parameters, run FD solver, get a scalar score (wall flux, stray field, thrust). There are no intermediate states, no temporal structure, no episode to learn from.

RL would technically work (treat geometry as a bandit problem) but:
- It's sample-inefficient for expensive single-shot functions
- It doesn't model uncertainty, so it can't reason about unexplored regions
- It has no principled way to stop (no convergence criterion)
- Convergence requires many more evaluations than BO for the same result

---

## What Bayesian Optimisation does

BO is the standard approach for optimising expensive black-box functions with few evaluations (Frazier 2018, Snoek et al. 2012). It does two things:

### 1. Builds a Gaussian Process surrogate

After each FD solver evaluation, BO fits a **Gaussian Process (GP)** to all observed (parameter, score) pairs. The GP provides:
- A **mean prediction** μ(x) — best estimate of the objective at any untested point x
- An **uncertainty** σ(x) — how confident we are at each point

The GP is cheap to evaluate (microseconds) once fitted, so we can "pre-explore" the design space without running the FD solver.

### 2. Acquisition function decides where to evaluate next

The acquisition function balances **exploitation** (go to where μ(x) is best) and **exploration** (go to where σ(x) is high — we don't know what's there). Common choices:

- **Expected Improvement (EI):** Expected gain over the current best. Exploits near-optima while exploring promising uncertain regions. Default choice for our geometry problem.
- **Upper Confidence Bound (UCB):** μ(x) + β·σ(x) — tunable exploration parameter β.
- **Thompson Sampling:** Sample a random GP realisation and maximise it — good for parallelism.

We run the FD solver at the acquisition function maximum, add the result to the GP dataset, refit, and repeat.

### Convergence

BO typically finds near-optimal solutions in **10–50 evaluations** for 5D problems, compared to thousands for random search or grid search. At 2s per FD solve, that's **20–100 seconds** of compute — vs. hours for grid sweep.

---

## What we're optimising

**Objective function** (to minimise):

```
score(geometry) = w1 * wall_flux + w2 * (1 - B_exit/B_target) + w3 * B_stray
```

where each term is evaluated by running `solve_het_bfield.py` at the given geometry and reading out the physics quantities.

Alternatively, we can run the AURORA RL agent at nominal currents to get the steady-state wall_flux — this would give a more accurate score but each evaluation takes longer (RL training run per geometry). For the BO outer loop, it's more practical to use the analytical surrogate values from `MagneticCircuit.compute()` at fixed nominal currents.

**Design variables (5D space):**

| Variable | Symbol | Range | Notes |
|----------|--------|-------|-------|
| Inner pole extension | ipe | [0, 1] | 0 = flush, 1 = full lip to exit plane |
| Channel length | Lch | [15, 25] mm | Ionisation zone depth |
| BN wall thickness | t_BN | [0.5, 2.0] mm | Life vs performance |
| Trim coil z-offset | Δz_trim | [0, 3] mm | Axial gradient range |
| Outer pole profile (single param) | k_outer | [0, 1] | Interpolates between rectangular and flux-matched shape |

**Constraints:**
- B_exit at nominal currents ∈ [150, 250] G (operating point maintained)
- Channel width fixed at 5mm (manufacturing constraint)
- Total thruster outer diameter ≤ 65mm

---

## The 90-degree pole face lip — why it exists and what BO will find

The "90-degree bend" is the **inner pole extension** — the inner pole piece has an L-shaped front face where the pole body (running axially alongside the channel) terminates with a short radial flange that extends to the exit plane.

**Without the lip (ipe=0):** The last magnetic field line in the channel terminates on the pole body face. That face is set back from the exit plane. The field lines approaching the BN inner wall plunge into the wall interior — the sheath electric field accelerates ions directly into the ceramic. High erosion.

**With the full lip (ipe=1.0):** The pole face extends flush to the exit plane. The last field line that passes through the channel terminates exactly at the exit plane, parallel to the BN wall surface (the "grazing line" condition of Mikellides et al. 2014). The sheath potential now points *along* the wall, not into it — ions are not accelerated toward the surface. Wall flux falls by 10-20× (shielded vs. unshielded).

This is the defining feature of the H6MS (Hall-6 Magnetically Shielded) design at JPL and was experimentally confirmed to extend thruster life by approximately 20× over an unshielded equivalent.

**Our design already has this.** In `solve_het_bfield.py`: `Z_BODY = 6.80`, `Z_EXIT = 7.00` — the 2mm front cap (`'Inner front cap (Part 2)'` in the legend) is the lip. It IS present in the simulation. The earlier sweep confirmed `ipe = 1.0` is optimal.

**What BO can do further:** BO will confirm the lip should be full length and may find that the lip geometry (currently rectangular cross-section, 2mm long) benefits from being longer (>2mm) or having a chamfered face. It will also reveal whether the BN thickness and channel length interact with the shielding condition — which is harder to see from 1D sweeps.

---

## BO vs RL — summary

| | Grid sweep | RL | **Bayesian Optimisation** |
|---|---|---|---|
| Use case | Small 2D space | Sequential runtime control | Expensive 5–10D design |
| Evaluations needed | n^d (exponential) | Thousands of episodes | 20–50 evaluations |
| Handles uncertainty | No | No (model-free) | **Yes — GP variance** |
| Exploits structure | No | Partial (value function) | **Yes — GP mean** |
| Convergence guarantee | Complete grid | No | Asymptotically Bayes-optimal |
| For HET geometry | OK for 2D only | Wrong tool | **Right tool** |
| Python library | NumPy | Stable-Baselines3 | BoTorch / Optuna / scikit-optimize |

---

## Implementation plan

The BO geometry optimiser will be implemented in `src/physics/bo_geometry_optimise.py`:

```
1. Define the 5D parameter space (bounds, types)
2. Define the objective function: run calibrate_k_coefficients.py → MagneticCircuit.compute()
   → compute wall_flux, B_stray at nominal currents
3. Initialise with 5–10 random evaluations (Latin Hypercube Sampling)
4. Run BO loop (BoTorch GP + Expected Improvement) for 30–50 iterations
5. Output: Pareto front of (wall_flux vs B_stray) and optimal geometry parameters
6. Write optimal geometry to outputs/calibration/optimal_geometry.json
7. Update generate_stl.py with optimal parameters → rebuild CAD
```

**Libraries:** BoTorch (PyTorch-based, state of the art for scientific BO) or Optuna (simpler API, good for getting started fast).

---

*See also: `src/physics/pole_geometry_sweep.py`, `docs/GEOMETRY_SPEC.md`, `src/physics/optimize_outer_pole.py`*
