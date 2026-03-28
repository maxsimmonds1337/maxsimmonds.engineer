# ẍ AI Architecture — Where Does the Intelligence Live?
*Do we need AI in space, or is ground-based AI sufficient?*

---

## The Core Question

The pitch deck says "AI-powered thruster" and "real-time AI control." But there's a fundamental question that needs an honest answer before we design anything:

**Does the intelligence need to be ON the satellite, or can we use AI on the ground to design better controllers that then run deterministically in space?**

Short answer: **Mostly ground. Some lightweight inference on-board. Not deep AI in space.**

---

## What Actually Needs to Happen, and How Fast?

| Event | Timescale | Needs on-board AI? |
|---|---|---|
| Plasma discharge initiation | ms | No — deterministic sequence |
| Plasma oscillation damping (breathing mode) | μs–ms | No — classic PID/control loop |
| Steady-state thrust control | seconds | No — lookup table + PID |
| Magnetic field adjustment for cathode protection | minutes–hours | **Maybe** — but ground-command works too |
| Drag compensation adjustment | minutes | No — atmospheric models are predictable |
| Cathode degradation tracking | days–weeks | No — ground telemetry analysis |
| Collision avoidance manoeuvre | minutes–hours | No — ground-commanded |
| Fleet-wide performance optimisation | weeks | No — ground AI on telemetry |

**Critical insight:** Cathode erosion is a *slow* process. It doesn't need millisecond AI response. It needs good field geometry — which can be designed offline using AI/simulation and implemented as a fixed or slowly-updated setpoint.

---

## The Radiation Problem

Standard AI chips (GPUs, NPUs, TPUs) are not radiation-hardened. In LEO/VLEO:

- **Total Ionising Dose (TID):** 1–10 krad/year at 500km; 10–100 krad/year at 200km (worse — lower altitude means less protection from Earth's magnetic field at high inclinations)
- **Single Event Effects (SEE):** Bit flips, latch-up, processor crashes
- **Radiation-hardened processors available:** LEON3/4 (FPGA-based), BAE RAD750, GR740 — all extremely limited compute by modern standards. The GR740 (state of art in rad-hard) does ~800 DMIPS. A Raspberry Pi 4 does ~25,000 DMIPS.

Running a neural network on radiation-hardened hardware in space is:
- Possible (TensorFlow Lite runs on microcontrollers)
- Severely compute-constrained (small networks only)
- Expensive to qualify
- Adds power draw
- Adds mass and volume

**SpaceX's actual approach on Starlink:** Simple deterministic controllers. Lookup tables. PID loops. Ground monitoring with parameter uplinks. They don't run neural networks on the thruster controller.

---

## What Ground-Based AI Can Do (and This Is Most of the Value)

### 1. Magnetic Field Topology Design (highest value)
- Run COMSOL/FEMM simulation of plasma physics
- AI optimises coil geometry, currents, and positioning to minimise ion flux at cathode
- **Output:** A fixed magnetic field configuration — implemented in hardware as fixed coil geometry and static current setpoints
- **This is a design-time activity, not a runtime activity**
- Tiz builds the thruster with this optimised geometry baked in
- The "AI" value is in the design, not the operation

### 2. Controller Parameter Optimisation
- Use reinforcement learning or Bayesian optimisation on a simulation/digital twin
- Find optimal PID gains, discharge voltage setpoints, flow rates for different operating conditions
- **Output:** Lookup tables (operating_point → {voltage, current, flow_rate, coil_currents})
- Upload to satellite once; update occasionally via ground link
- In-space: thruster reads the table deterministically. No AI inference in space.

### 3. Plasma State Estimation Model Training (ground → small on-board model)
- Plasma state (density, temperature, ion energy) is hard to measure directly without probes that disturb the plasma
- Train a small neural network on ground test data: inputs = {discharge_current, discharge_voltage, optical_emission} → outputs = {plasma_state_estimate}
- **This model can be small enough for a microcontroller** (~10KB, <1ms inference)
- Deploy as firmware, not as an "AI system"
- Radiation tolerance: FPGAs can implement this with triple-redundancy (TMR)

### 4. Ground Telemetry Analysis & Predictive Maintenance
- Satellite sends telemetry: discharge current, voltage, thrust estimate, temperature
- Ground AI analyses trends: cathode degradation rate, efficiency drift, anomaly detection
- Ground operators (or automated system) uploads updated parameters: "cathode shows 12% erosion, shift coil_3 current from 2.1A to 2.3A"
- **This is probably where most of the commercial AI value lives** — not in the thruster, but in the fleet management software (SaaS revenue stream)

### 5. Design Iteration Between Test Campaigns
- Between test cell sessions: feed results to AI → get recommended parameter changes → implement → retest
- Claude-in-the-loop for analysis (as per IDEAS.md)
- Dramatically accelerates development vs. manual analysis

---

## What Minimal On-Board Intelligence Makes Sense

If we do put anything intelligent on-board, it should be:

### Tier 1: Definitely yes (microcontroller-level, radiation-tolerant)
- **Fault detection:** Is discharge current in normal range? Temperature within limits? If not, safe-mode.
- **Plasma ignition sequence:** State machine for startup/shutdown
- **Closed-loop thrust control:** PID on discharge current/voltage to maintain target thrust point
- **Lookup table execution:** Given target thrust + propellant type → set operating point

**Implementation:** STM32 or similar microcontroller. Radiation-tolerant (not rad-hard, but screened). Standard aerospace practice. Not novel. Proven approach.

### Tier 2: Maybe, if compute budget allows (FPGA-based)
- **Plasma state estimation:** Tiny neural network (trained on ground, inferred on FPGA) estimating plasma state from electrical measurements
- **Efficiency tracking:** Detect when thruster is drifting from optimum and adjust setpoint
- **Implementation:** Xilinx/Lattice FPGA with TMR, running a small fixed neural network (no training in space — inference only)

### Tier 3: No — not in space
- Real-time magnetic field topology optimisation
- Large language model or complex reasoning
- Online learning / model updating in space
- Anything that needs a GPU

---

## How This Reframes the "AI" Story

### What we say now (pitch deck):
*"Real-time AI optimization, 1000Hz updates, autonomous orbit control"*

### What's honest and still compelling:
*"AI-designed magnetic shielding geometry, ground-validated via physics simulation and test data, implemented as an optimised fixed configuration — eliminating cathode erosion by design rather than by runtime reaction. On-orbit, lightweight plasma state estimation firmware provides closed-loop efficiency tracking. Ground-side AI analyses fleet telemetry for predictive maintenance and parameter updates."*

This is:
- Honest
- Still technically impressive
- Actually more credible to an ESA reviewer than "AI at 1000Hz"
- Defensible in TEB Q&A
- Easier to build (no exotic space-grade AI hardware)

---

## The Commercial Software Layer (SaaS)

The SaaS revenue stream in the business plan is *ground-based AI software*:

- **Thruster health dashboard:** Real-time telemetry from all satellites, cathode degradation estimates, remaining life predictions
- **Parameter optimisation service:** AI recommends field setpoint updates as thrusters age
- **Mission planning:** AI-assisted ΔV budget planning, propellant lifetime projections
- **Constellation management:** Multi-satellite station-keeping coordination

This is where recurring revenue comes from and where the AI story is most legitimate. A constellation operator with 50+ satellites will pay €5–20K/year/satellite for a service that extends thruster life by 2–3 years. That's €250K–€1M/year for a 50-sat constellation — and the marginal cost of the software is near zero at scale.

---

## Implication for ESA BIC Application

The incubation proposal needs to reflect this architecture honestly:

**During incubation, AI work means:**
1. Build simulation pipeline (COMSOL/FEMM + Python)
2. Train optimisation model on simulation data → output: optimal coil geometry
3. Build and test against that optimised geometry in the lab
4. Train plasma state estimation model on test data
5. Implement as microcontroller firmware
6. Validate: does the firmware estimate match probe measurements?

**Not:**
- Building a space-qualified AI processor
- Real-time ML inference at 1000Hz in a vacuum chamber
- Anything that requires exotic hardware

This is actually *better* for the ESA BIC case — it's achievable within €60K and 24 months.

---

## Summary Decision

| Where | What AI does | Technology |
|---|---|---|
| **Ground — design phase** | Optimise magnetic field topology, channel geometry, operating parameters | COMSOL + Python + RL/Bayesian optimisation |
| **Ground — development** | Analyse test data, suggest parameter changes between test campaigns | LLM-assisted (Claude), ML regression |
| **Ground — operations** | Fleet telemetry analysis, predictive maintenance, parameter uplink | SaaS platform, cloud ML |
| **On-board — firmware** | Fault detection, PID thrust control, lookup table execution | Microcontroller (radiation-tolerant) |
| **On-board — optional** | Plasma state estimation from indirect sensors | Tiny neural net on FPGA (inference only, trained on ground) |
| **On-board — no** | Real-time field topology optimisation, online learning | Not viable in space with current hardware |

---

*See also: DESIGN_TRADESPACE.md, MARKET_ANALYSIS.md, IDEAS.md*
