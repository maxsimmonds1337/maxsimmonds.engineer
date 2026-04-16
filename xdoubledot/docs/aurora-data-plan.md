---
layout: xdoubledot
title: AURORA Data Capture Plan
---

# AURORA — Data Capture Plan for Neural PPU Control
**AURORA: HET Real-time Management and Execution System**

The goal: a unified neural network controller that replaces the conventional PPU control loop,
taking raw sensor readings and outputting all actuator commands in real time — coil currents,
discharge voltage, mass flow, cathode heater, keeper. This document defines what data must be
captured during hardware testing to train and validate AURORA.

---

## Why data capture matters now

Every firing is irreplaceable. Hardware time is expensive and thruster life is finite.
A firing without proper instrumentation is a missed training opportunity.
The data captured in v1 hardware tests directly determines whether AURORA v2+ can be trained.

---

## Controller versions and their data requirements

| Version | Controls | Needs from data |
|---------|----------|-----------------|
| **v1** (current) | I_inner, I_outer, I_trim | B-field calibration (K-coefficients), coil current response, wall erosion baseline |
| **v2** | + Vd, ṁ | Id(Vd, ṁ, B) mapping, breathing mode vs Vd, throttle curves |
| **v3** | + I_heater, I_keeper | Cathode ignition model, keeper wear, heater thermal time constant |

---

## Sensors required — minimum for v1

### PPU telemetry (must log at ≥ 1 kHz)
| Signal | Symbol | Units | Why |
|--------|--------|-------|-----|
| Discharge voltage | Vd | V | Operating point |
| Discharge current | Id | A | Breathing mode signal, power budget |
| Inner coil current | I_inner | A | K-coefficient calibration |
| Outer coil current | I_outer | A | K-coefficient calibration |
| Trim coil current | I_trim | A | K-coefficient calibration |
| Coil voltages | V_coil | V | Iron saturation check |
| PPU bus voltage | V_bus | V | Power budget |
| PPU input power | P_in | W | Efficiency metric |

### Magnetic field (each firing, static + swept)
| Signal | Symbol | Units | Why |
|--------|--------|-------|-----|
| B at channel exit midpoint | B_exit | T | K_EXIT calibration |
| B at cathode location | B_cath | T | K_CATH calibration |
| B at upstream (z = L_ch/2) | B_upstream | T | K_GRAD calibration |
| B radial profile at exit | B_r(r) | T | Shielding condition verification |

Use a calibrated Hall probe (Lakeshore 475 or similar) swept at 3×3 current combinations
per GEOMETRY_SPEC §10 Q4. This is the single highest-value activity in the first firing campaign.

### Thrust and propulsion
| Signal | Symbol | Units | Why |
|--------|--------|-------|-----|
| Thrust | F | mN | Ground truth for reward model |
| Anode mass flow | ṁ_a | sccm | Propellant efficiency |
| Cathode flow | ṁ_c | sccm | Usually 10% of anode flow |
| Propellant tank pressure | P_tank | bar | Flow calibration |
| MFC set point vs actual | ṁ_set, ṁ_act | sccm | Feed system lag model |

### Thermal
| Signal | Symbol | Units | Why |
|--------|--------|-------|-----|
| BN inner wall temperature | T_BN_in | °C | Sputtering rate depends on T |
| BN outer wall temperature | T_BN_out | °C | Asymmetric erosion indicator |
| Iron pole face temperature | T_pole | °C | Stay below Curie point (770°C) |
| Coil temperature | T_coil | °C | Coil derating check |
| PPU MOSFET temperature | T_FET | °C | Reliability model |

### Additional for v2 (breathing mode control)
| Signal | Symbol | Units | Why |
|--------|--------|-------|-----|
| Id at 10+ kHz | Id_hf | A | Breathing mode frequency, amplitude |
| Plume luminosity | I_optical | a.u. | Independent breathing mode indicator |
| Cathode-to-ground voltage | V_cg | V | Cathode coupling health |
| Keeper current/voltage | I_k, V_k | A, V | Cathode operating point |
| Heater current/voltage | I_h, V_h | A, V | Cathode model |

---

## Data capture protocols

### Protocol 1 — K-coefficient calibration sweep (first firing, 30–60 min)
Run a 3×3×3 grid (inner × outer × trim):
```
I_inner ∈ {1.5, 3.0, 4.5} A
I_outer ∈ {1.25, 2.5, 3.75} A
I_trim  ∈ {-1.0, 0.0, 1.0} A
```
At each point: record B at all 3 probe locations. This calibrates all K-coefficients.
Log at ≥ 100 Hz. Dwell ≥ 30 s per point to reach thermal steady state.

### Protocol 2 — Nominal endurance (steady-state training data)
Run at nominal point (3.0A, 2.5A, 0.0A, 250V, 2.5sccm) for several hours.
Log ALL signals at 1 kHz. This provides:
- Baseline `wall_flux` proxy calibration
- Thermal drift characterisation
- Long-horizon behaviour for RL policy evaluation

### Protocol 3 — Breathing mode mapping (v2 prerequisite)
Sweep Vd from 200–300V at fixed ṁ. Log Id at ≥ 20 kHz.
FFT each steady-state window to map: `f_breathing(Vd, ṁ, B_exit)`.
This is the dataset that trains the breathing mode suppression reward model.

### Protocol 4 — Throttle curves (v2 prerequisite)
Grid over (Vd, ṁ) while holding coils at optimal shielding point.
Measure: thrust, Id, eta_thrust, eta_ion, oscillation amplitude.
Captures the performance surface needed for the v2 surrogate.

---

## Data format and storage

### File format
- **Raw telemetry**: HDF5 (`.h5`), one file per firing session
  - Groups: `/ppu`, `/bfield`, `/thrust`, `/thermal`, `/hf_id`
  - Each dataset: timestamps + values, SI units, metadata in attrs
- **Processed/calibrated**: CSV for quick inspection, `.npy` for NN training

### Metadata to record with every firing
```yaml
firing_id: "AEGIS-001-20260501"
thruster_sn: "AEG-001"
facility: "xdoubledot vacuum chamber"
propellant: "Kr"
background_pressure_mbar: 5e-5
run_hours_on_thruster: 0
operator: ""
notes: ""
```

### Storage and version control
- Raw data: NOT in git (too large). Store in a dedicated S3 bucket or NAS.
- Processed features / calibration results: commit to `Aegis/outputs/calibration/`
- K-coefficient calibration CSV: `outputs/calibration/k_coefficients_measured.csv`

---

## What data enables what capability

| Data captured | Enables |
|---------------|---------|
| K-coefficient sweep (Protocol 1) | Replace hand-tuned K values; accurate `MagneticCircuit.compute()` |
| Steady-state endurance (Protocol 2) | Calibrate `wall_flux → hr` lifetime mapping; validate RL policy |
| Breathing mode sweep (Protocol 3) | Train v2 breathing mode surrogate; enable Vd suppression control |
| Throttle curves (Protocol 4) | Train v2 thrust/efficiency surrogate; enable power management |
| Thermal data (all protocols) | Coil derating model; thermal time constants for PPU protection |

---

## Existing public datasets — landscape (as of 2026)

**The short answer: no public raw-waveform HET dataset exists.**
No agency or university maintains a download-ready repository of HET firing telemetry
analogous to, e.g., NASA's CMAPSS turbofan dataset. The field has not developed that
culture yet — most data lives in PDFs, is export-controlled, or is proprietary.

### What does exist and where to look

| Source | What's available | URL |
|--------|-----------------|-----|
| NASA NTRS | PDF reports with performance tables (not raw waveforms) | ntrs.nasa.gov |
| Zenodo | Best chance of researcher-uploaded supplemental data | zenodo.org → search "Hall thruster" |
| Figshare | Same | figshare.com |
| UM Deep Blue | Michigan PhD dissertations, sometimes include data appendices | deepblue.lib.umich.edu |
| GT SMARTech | Georgia Tech dissertations | smartech.gatech.edu |
| IEPC Proceedings | Conference papers (Electric Rocket Propulsion Society) | electricrocket.org |

### Specific thruster status
- **NASA HERMeS**: Tested at GRC VF-5 and Aerojet EP facility. AIAA/NTRS papers only — no raw telemetry released. Key: Hofer et al. 2016–2020, Kamhawi AIAA 2016-4826.
- **H6 (Michigan PEPL)**: Enormous diagnostic dataset exists internally. Prof. Jorns group has published breathing mode FFTs but not underlying waveforms. Email Jorns or Walker directly for academic ML collaboration.
- **SPT-100**: Performance tables in 1990s–2000s AIAA papers (Garner/Brophy/JPL). No raw telemetry.
- **BHT-200 (Busek)**: Characterised at AFRL Edwards — generally export-controlled or FOUO.
- **Sitael HT100/HT400**: ESA-funded papers with performance tables (IEPC proceedings).

### Best path for synthetic training data
**HallThruster.jl** (MIT / UM-PEPL, open source) — 1D fluid Hall thruster code.
Can generate unlimited discharge current time-series, breathing mode waveforms, and
PPU setpoint response curves. Use this to pre-train AURORA, then fine-tune on real data.
GitHub: github.com/UM-PEPL/HallThruster.jl

**Strategic implication:** xdoubledot's own firing data is genuinely novel.
A well-structured open dataset (with ITAR check) would be a significant community
contribution and a strong publication. Plan the data format accordingly.
A well-structured open dataset (with ITAR check) could be a significant community contribution.

---

## AURORA naming rationale

**AURORA** — Adaptive Unified Real-time Operation and Regulation Algorithm

Named for the Aurora Borealis — the visual signature of charged particles being guided
by a magnetic field. Sits alongside **Aegis** (the hardware/physics codebase) naturally.
- Aegis: the shield + thruster design
- AURORA: the intelligence that operates it

Alternative names considered: HERMES, CORTEX, APEX, IRIS, ATLAS.
AURORA selected: relevant to magnetic field control, striking name, strong backronym.
