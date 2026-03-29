---
layout: xdoubledot
title: PPU Design
---

# Power Processing Unit — Design Reference
## 200W Hall Effect Thruster (Krypton, 250V Discharge)
### Aegis RL Platform — Hardware Subsystem

*Status: Preliminary Design*
*Thruster: 200W Kr HET, 250 V / 0.8 A discharge, 12 mN, external hollow cathode*
*Bus: 28 V unregulated (ECSS small-satellite standard)*
*Control: STM32F405RGT6 @ 168 MHz, 1 kHz RL policy loop*

---

## Table of Contents

1. [System Overview and Block Diagram](#1-system-overview-and-block-diagram)
2. [Subsystem 1 — Discharge Supply (HV)](#2-subsystem-1--discharge-supply-hv)
3. [Subsystem 2 — Coil Current Drivers](#3-subsystem-2--coil-current-drivers)
4. [Subsystem 3 — Cathode Heater Supply](#4-subsystem-3--cathode-heater-supply)
5. [Subsystem 4 — Keeper and Ignition Supply](#5-subsystem-4--keeper-and-ignition-supply)
6. [Subsystem 5 — Digital Control and Telemetry](#6-subsystem-5--digital-control-and-telemetry)
7. [Subsystem 6 — Protection Circuits](#7-subsystem-6--protection-circuits)
8. [Power Budget](#8-power-budget)
9. [Mass and Volume Estimate](#9-mass-and-volume-estimate)
10. [Radiation and Environmental Considerations](#10-radiation-and-environmental-considerations)
11. [Bill of Materials Summary](#11-bill-of-materials-summary)
12. [Design Notes and Open Items](#12-design-notes-and-open-items)

---

## 1. System Overview and Block Diagram

The PPU sits between the 28 V spacecraft bus and the thruster assembly. It must simultaneously:

- Sustain a 250 V / 0.8 A discharge plasma (200 W)
- Drive three independent magnetic coils under closed-loop current control
- Start and sustain the hollow cathode (heater, keeper ignition, steady-state keeper)
- Execute the STM32-hosted RL magnetic shielding policy at 1 kHz
- Report telemetry to the satellite OBC and receive commands via CAN

All high-voltage rails are floating with respect to chassis. The discharge cathode potential floats at the plasma potential reference; the digital ground is tied to chassis (structural ground).

```
═══════════════════════════════════════════════════════════════════════════════

  28 V UNREG BUS (6–10 A peak)
  ┌───────────────┐
  │  EMI FILTER   │  Common-mode choke + X/Y caps + TVS
  │  + INRUSH LIM │  NTC + bypass relay
  └───────┬───────┘
          │ 28 V (filtered)
          │
  ┌───────┴────────────────────────────────────────────────────────────┐
  │                      PPU POWER DISTRIBUTION                        │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
  │  │ HV DISCHARGE │  │  COIL SUPPLY │  │ CAT/KEEPER   │            │
  │  │   SUPPLY     │  │  PRE-REG     │  │   SUPPLY     │            │
  │  │  28V→250V    │  │  28V→9V      │  │  28V→LV/HV   │            │
  │  │  ACF Flyback │  │  Sync Buck   │  │  Flyback     │            │
  │  │  200 W       │  │  ~36 W       │  │  ~25 W       │            │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
  │         │                 │                  │                    │
  │  ┌──────┴──────┐  ┌───────┴──────────────────┴──┐                │
  │  │ DISCHARGE   │  │   3× COIL CURRENT DRIVERS    │                │
  │  │ OUTPUT FILT │  │   (Current-mode buck, 9V→Vcoil)               │
  │  │ + ARC DET   │  │   Inner / Outer / Trim        │               │
  │  └──────┬──────┘  └───────┬──────────────────────┘                │
  └─────────┼─────────────────┼──────────────────────────────────────┘
            │                 │
  ══════════╪═════════════════╪══════════ HET CONNECTOR ═════════════
            │ 250V discharge  │ coil currents (3 pairs)
            │                 │
  ┌─────────▼─────────────────▼─────────────────────────────────────┐
  │                    HALL EFFECT THRUSTER                          │
  │  Discharge channel ← 250 V anode                                │
  │  Inner coil  ← 0–3 A                                            │
  │  Outer coil  ← 0–2.5 A                                          │
  │  Trim coil   ← 0–1.5 A  (RL-modulated at 1 kHz)                │
  │                                                                  │
  │  HOLLOW CATHODE (external)                                       │
  │    Heater    ← 5–12 V / ~2 A (isolated buck)                   │
  │    Keeper    ← 300–600 V ignition pulse, then 15 V / 1.5 A     │
  └──────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │                  DIGITAL CONTROL BOARD                           │
  │                                                                  │
  │  STM32F405RGT6 @ 168 MHz                                        │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │  RL POLICY (1 kHz)  ──►  PWM setpoints (TIM1, TIM8)    │    │
  │  │  ADC0–ADC11: Vdis, Idis, I_inner, I_outer, I_trim,     │    │
  │  │              Vheater, Ikeeper, Vbus, T_pcb, ...         │    │
  │  │  SPI: isolated gate driver ICs                           │    │
  │  │  CAN1 (ISO 11898): OBC telemetry / commands             │    │
  │  │  UART3: debug / bootloader                               │    │
  │  │  GPIO: arc detect, safe-mode latch, ignition sequencer   │    │
  │  └─────────────────────────────────────────────────────────┘    │
  │                                                                  │
  │  ISOLATION BARRIER (SiO2 digital isolators, 2.5 kV working)     │
  │  HV side ←──────────────────────────────→ LV/digital side       │
  └──────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │  PROTECTION                                                      │
  │  • Input TVS + fuse (polyfuse + hardwired fuse, 15 A)           │
  │  • Discharge overcurrent: comparator latch, 1.2 A trip           │
  │  • Arc detection: dV/dt > 50 V/µs → disable in < 5 µs           │
  │  • Coil overcurrent: per-channel current limiting                │
  │  • Safe-mode GPIO from OBC → all HV rails off in < 1 ms         │
  └──────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Subsystem 1 — Discharge Supply (HV)

### 2.1 Topology: Active-Clamp Flyback (ACF)

**Justification.**
- Boost: no galvanic isolation — mandatory for the floating discharge rail.
- Half-bridge LLC: excellent efficiency at fixed load but very poor at the 10:1 load range seen during ignition, arc recovery, and throttle-down.
- Push-pull / full-bridge: appropriate above ~300 W; overkill complexity at 200 W.

Active-clamp flyback is the correct choice:
- Galvanic isolation (discharge floats ~5–15 V above cathode potential, which floats at plasma potential — typically +5 to +20 V above chassis)
- Handles 22–36 V input and 200–280 V output during ignition ramp without topology change
- Active clamp recycles leakage inductance energy → efficiency > 88% vs ~82% for RCD-clamp flyback
- Near-zero-voltage switching (ZVS) over most of the operating range
- Fail-safe: active clamp FET failure reverts to dissipative-clamp flyback — degraded efficiency, not catastrophic

### 2.2 Key Parameters

| Parameter                  | Value                     | Notes |
|----------------------------|---------------------------|-------|
| Switching frequency        | 150 kHz                   | Ferrite core loss acceptable; above 200 kHz N87 loss rises steeply |
| Input voltage range        | 22–36 V (nom 28 V)        | ECSS 28 V bus tolerance |
| Output voltage             | 250 V ± 1%                | Discharge anode reference |
| Output current             | 0–0.85 A (nom 0.8 A)      | 6% headroom for plasma impedance variation |
| Output power               | 200 W continuous          | Designed to 220 W for 10% derating |
| Transformer turns ratio    | N = 1:9 (primary:secondary)| See derivation below |
| Duty cycle at nominal      | D ≈ 0.47                  | |
| Magnetising inductance Lm  | 22 µH (primary referred)  | Controls peak flux density |
| Leakage inductance Llk     | < 200 nH                  | Interleaved winding mandatory |
| Output filter capacitor    | 10 µF / 400 V film        | Holdup + arc energy reservoir |
| Output filter ESR          | < 50 mΩ                   | Critical for arc dV/dt detection |
| Clamp capacitor            | 330 nF / 100 V            | Active clamp resonant cap |

### 2.3 Turns Ratio Derivation

In CCM flyback: `V_out = V_in × (N_s/N_p) × D / (1 - D)`

Setting D_max = 0.48 at V_in_min = 22 V, target V_out = 250 V:

```
N_s/N_p = V_out × (1 - D_max) / (V_in_min × D_max)
        = 250 × 0.52 / (22 × 0.48)
        = 130 / 10.56 ≈ 12.3  →  rounds to N = 1:9 (conservative)
```

At N = 1:9 with V_in = 28 V: D = 250 / (250 + 28×9) = 0.498 ≈ 0.47 with losses. Minimum controllable input is ~24 V — within the 22 V lower edge with current-programmed control.

### 2.4 Transformer Design

Core: Ferroxcube ETD32, N87 material, gap tuned for Lm = 22 µH.

- Primary: 9 turns, 5× 0.25 mm Litz wire
- Secondary: 81 turns, 3× 0.1 mm Litz wire
- Winding: interleaved P-S-P-S to minimise leakage and AC resistance
- Estimated core + copper loss: ~1.6 W at 200 W (transformer η = 99.2%)

### 2.5 Key Components

| Function               | Part                          | Rating | Notes |
|------------------------|-------------------------------|--------|-------|
| Controller             | UCC28780PWPR (TI)             | —      | ACF dedicated; adaptive dead-time ZVS |
| Primary FET            | GS61008P (GaN Systems)        | 100 V / 30 A / 7 mΩ | Fast switching for ZVS at 150 kHz |
| Clamp FET              | GS61008P                      | same   | |
| Gate driver (GaN)      | LMG1020 (TI)                  | —      | < 2Ω, < 5 ns rise |
| Secondary rectifier    | SCS220AE2 (Wolfspeed SiC SBD) | 600 V / 20 A | No reverse recovery; SiC TID-resistant |
| Output cap (main)      | WIMA FKP2 10µF / 400 V film   | —      | Vacuum-safe, low ESR |
| Output cap (HF bypass) | 100 nF C0G / 500 V            | —      | |

**Efficiency estimate:** 87–89% at full load.
Dominant losses: primary switch conduction ~2 W, transformer winding ~3.2 W, secondary diode ~2.5 W, control ~1 W.

---

## 3. Subsystem 2 — Coil Current Drivers

### 3.1 Architecture

Three independent current-mode synchronous buck converters, fed from a common **9 V pre-regulated rail** (28 V → 9 V synchronous buck, ~97% efficient at 40 W).

The 9 V pre-reg provides: (1) a clean, well-regulated input to the coil drivers avoiding the full 22–36 V bus range; (2) a natural overcurrent boundary for the coil subsystem as a whole.

Current-mode (not voltage-mode) control is chosen for: first-order dynamic response, natural cycle-by-cycle overcurrent protection, and compatibility with the 1 kHz RL setpoint update rate.

### 3.2 Pre-Regulator (28 V → 9 V)

| Parameter           | Value                                      |
|---------------------|--------------------------------------------|
| Topology            | Synchronous buck (non-isolated)            |
| Output              | 9.0 V ± 1%, 4 A continuous (36 W)         |
| Switching frequency | 400 kHz                                    |
| Inductor            | 10 µH, Isat > 6 A (Bourns SRR1260A-100M)  |
| Output capacitor    | 47 µF / 16 V MLCC X7R (3× parallel)       |
| Controller          | LTC3891 (Analog Devices)                   |
| MOSFETs             | SiR622DP (Vishay) — 60 V / 9.8 mΩ sync pair |
| Efficiency          | ~97%                                       |

### 3.3 Coil Buck Converters (×3)

Three identical LTC3609-based current-mode synchronous bucks with DAC-driven current setpoints from the STM32 via SPI-isolated reference.

| Parameter              | Inner Coil       | Outer Coil       | Trim Coil              |
|------------------------|------------------|------------------|------------------------|
| Turns (N)              | 80               | 60               | 40                     |
| Nominal setpoint       | 3.0 A            | 2.5 A            | 0–1.5 A (RL-controlled)|
| Maximum current        | 4.0 A            | 3.5 A            | 2.0 A                  |
| Estimated coil DCR     | ~0.8 Ω           | ~0.7 Ω           | ~0.5 Ω                 |
| Estimated coil L       | ~500 µH          | ~350 µH          | ~150 µH                |
| Nominal output voltage | ~2.4 V           | ~1.75 V          | ~0.75 V                |
| Switching frequency    | 500 kHz          | 500 kHz          | 500 kHz                |
| External inductor      | 4.7 µH / 6A      | 4.7 µH / 6A      | 4.7 µH / 6A            |
| Output cap             | 22 µF X7R MLCC   | 22 µF X7R MLCC   | 22 µF X7R MLCC         |
| Current sense shunt    | 25 mΩ / 1 W      | 50 mΩ / 1 W      | 50 mΩ / 1 W            |
| Current sense amp      | INA240A2 (TI)    | INA240A2 (TI)    | INA240A2 (TI)          |

**Why 20 kHz current loop bandwidth for a 1 kHz policy rate:** The RL policy issues a new setpoint every 1 ms. A 20 kHz current loop bandwidth gives ~50 µs settling to 2% — well within the 1 ms budget. Higher bandwidth is unnecessary and increases switching losses.

**Inductor ripple check (trim coil, worst case — lowest Vout):**
```
ΔI = Vout × (1 - D) / (L × fsw)
   = 0.75 × (1 - 0.083) / (4.7e-6 × 500e3)
   = 0.29 A peak-to-peak   (19% of 1.5 A max — acceptable)
```

The coil inductance (150–500 µH) dominates output filtering; the 22 µF capacitor provides HF bypass only.

**Controller IC:** LTC3609 (ADI) — current-mode synchronous buck, SYNC input lockable to STM32 timer for frequency synchronisation (prevents beat frequencies between the three switchers), reference input suitable for DAC-driven setpoints.

**MOSFETs:** SiR892DP (Vishay) — 30 V, 9.5 mΩ, 11 A, dual N-channel SO-8. Low Qg (14 nC) suited to 500 kHz.

**Current sense:** INA240A2 (TI) — bidirectional with PWM rejection. Without PWM rejection, switching node transients couple into the sense amp and cause false current readings. Gain = 20 V/V. For inner coil (max 4 A), use 25 mΩ: 4 × 0.025 × 20 = 2.0 V within 3.3 V ADC range.

**Overall coil subsystem efficiency (28 V → coil terminals):** ~87–89%.

---

## 4. Subsystem 3 — Cathode Heater Supply

### 4.1 Function

The hollow cathode insert (typically Ba-impregnated tungsten matrix) must reach ~1000–1100°C before electron emission begins. Heater power: ~20 W at 5–12 V, up to 4 A.

### 4.2 Topology: Isolated Flyback (Primary-Side Regulation)

Isolation is mandatory — the heater element is inside the cathode assembly which floats at cathode potential. A non-isolated supply creates a ground loop that injects noise into plasma diagnostics.

Primary-side regulation (PSR) via UCC28700 avoids an optocoupler feedback path on the secondary, which would add outgassing risk (optocoupler epoxy in vacuum).

| Parameter             | Value                                |
|-----------------------|--------------------------------------|
| Output voltage        | 5–12 V adjustable (DAC-trimmed via SS pin) |
| Output current        | 0–4 A (20 W max)                    |
| Switching frequency   | 200 kHz                              |
| Transformer           | Custom EFD25, N87, N = 1:0.6        |
| Output cap            | 100 µF / 25 V solid tantalum (vacuum-safe) |
| Controller            | UCC28700 (TI)                        |
| Efficiency            | ~85%                                 |

**Current limiting:** 0.1 Ω / 2 W sense resistor on secondary + OPA197 error amplifier caps duty cycle. STM32 adjusts limit setpoint via DAC during the 5-minute thermal ramp (prevents thermal shock to insert).

**Heater sequencing** is STM32 firmware: ramp 0→full power over 300 s, monitor keeper current onset, then reduce to maintenance level (~10 W).

---

## 5. Subsystem 4 — Keeper and Ignition Supply

### 5.1 Two-Stage Architecture

A single supply covering 600 V ignition and 15 V keeper operation is impractical to optimise (40:1 range). Flight heritage approach (Busek BHT-200 class): two stages sharing one transformer.

**Stage A — HV Ignition (tertiary winding)**

| Parameter             | Value                                |
|-----------------------|--------------------------------------|
| Open-circuit voltage  | 300–600 V adjustable (PWM duty)     |
| Peak current limit    | 200 mA (series 2.2 kΩ resistor)     |
| Turns ratio (primary) | 1:22 for 600 V from 28 V            |
| Isolation             | 2.5 kV working, 5 kV hipot          |
| Output cap            | 47 nF / 1 kV C0G ceramic            |
| Series resistor       | 2.2 kΩ / 5 W wire-wound ceramic     |

The 2.2 kΩ limits breakdown current and provides a characteristic dI/dt signature that the comparator uses to detect successful ignition.

**Stage B — LV Keeper (secondary winding)**

| Parameter             | Value                                |
|-----------------------|--------------------------------------|
| Output voltage        | 15 V regulated                      |
| Output current        | 0–1.5 A (22.5 W max)               |
| Output cap            | 100 µF / 25 V solid tantalum        |
| Efficiency            | ~86%                                 |

### 5.2 Ignition Sequencer (STM32 Firmware)

```
1. Enable heater supply; execute thermal ramp profile (5 min)
2. Assert HV_IGNITE GPIO → enables HV winding via series FET
3. Monitor KEEPER_I via ADC at 10 kHz: watch for current step (breakdown)
4. No breakdown after 100 ms → retract HV, wait 2 s, retry (max 10 attempts)
5. Breakdown detected:
   → HARDWARE comparator (< 1 µs) disables HV FET, enables LV keeper FET
   → STM32 firmware monitors keeper current; auto-relight if plasma extinguishes
```

The HV → LV handover **must** be hardware-timed (comparator-triggered, not STM32 ISR) to prevent the 600 V rail being present during keeper plasma operation, which would overdrive keeper current and damage the electrode.

---

## 6. Subsystem 5 — Digital Control and Telemetry

### 6.1 Microcontroller: STM32F405RGT6

168 MHz Cortex-M4F with hardware FPU. Key peripheral utilisation:

| Peripheral | Use |
|---|---|
| TIM1 (advanced) | Gate PWM generation for HV flyback + coil drivers (synchronised, centre-aligned) |
| TIM8 (advanced) | Ignition sequencer timing, keeper supply PWM |
| ADC1, ADC2 | Synchronous sample at 1 kHz DMA, triggered by TIM1 update event |
| SPI1 | Isolated gate drivers (ADuM1201) |
| SPI2 | DAC for coil current setpoints (via isolation) |
| CAN1 | OBC telemetry / commands (ISO 11898, 1 Mbit/s) |
| UART3 | Debug / bootloader |
| I2C1 | TMP100 temperature sensors (×2) |
| IWDG + WWDG | Dual watchdog — SEU protection |

**RL Policy Execution at 1 kHz (per-tick sequence):**
1. DMA completes → ADC values in SRAM (triggered by TIM1 update)
2. Normalise observations to policy training range
3. Forward pass: 2-layer MLP, hidden size TBD from training (64×64 typical; STM32 handles up to 128×128 within 1 ms)
4. De-normalise actions → three current setpoints → DAC via SPI
5. Log 1 Hz telemetry frame to CAN TX FIFO
6. Check all protection flags; update fault state machine

**Estimated STM32 load:** policy inference ~8–50 µs (64×64 to 128×128), ADC processing ~20 µs, CAN framing ~10 µs. Total < 100 µs per 1 ms tick — 10% CPU utilisation maximum.

### 6.2 Isolation Architecture

STM32 runs on chassis-ground (digital) side. All signals crossing the HV barrier use ADuM1201 (Silicon Dioxide, 2.5 kV) isolators:
- 4× ADuM1201 = 8 isolation channels for gate drivers (HV flyback: 2 ch, 3× coil drivers: 6 ch)
- SPI DAC communication: ADuM3471 (quad isolated SPI, 2.5 kV)

### 6.3 ADC Channel Assignment

| Channel  | Signal              | Full Scale | Scaling           |
|----------|---------------------|------------|-------------------|
| ADC1_0   | Discharge voltage   | 300 V      | ÷100 → 3.0 V FSD |
| ADC1_1   | Discharge current   | 1.0 A      | 2Ω shunt ×1.5 amp |
| ADC1_2   | Bus voltage         | 40 V       | ÷13 divider       |
| ADC1_3   | Inner coil current  | 4.0 A      | 25 mΩ, gain 20    |
| ADC1_4   | Outer coil current  | 3.5 A      | 50 mΩ, gain 20    |
| ADC1_5   | Trim coil current   | 2.0 A      | 50 mΩ, gain 20    |
| ADC2_0   | Keeper current      | 2.0 A      | 100 mΩ shunt      |
| ADC2_1   | Keeper voltage      | 25 V       | ÷8.3 divider      |
| ADC2_2   | Heater current      | 4.0 A      | 50 mΩ shunt       |
| ADC2_3   | Heater voltage      | 15 V       | ÷4.5 divider      |

12-bit ADC at 3.3 V full scale → 0.8 mV/LSB = 0.27 mA resolution on a 50 mΩ / gain-20 channel. Adequate.

### 6.4 CAN Telemetry Frame (1 Hz)

```
Bytes  0– 1:  frame counter (uint16)
Bytes  2– 3:  discharge voltage (uint16, mV)
Bytes  4– 5:  discharge current (uint16, mA)
Bytes  6– 7:  inner coil current (uint16, mA)
Bytes  8– 9:  outer coil current (uint16, mA)
Bytes 10–11:  trim coil current  (uint16, mA)
Bytes 12–13:  keeper voltage (uint16, mV)
Bytes 14–15:  keeper current (uint16, mA)
Bytes 16–17:  heater power (uint16, mW)
Bytes 18–19:  bus voltage (uint16, mV)
Bytes 20–21:  PCB temperature (int16, 0.01°C)
Byte  22:     fault flags byte 0
Byte  23:     fault flags byte 1
Bytes 24–27:  policy last action (3× float16 packed)
Bytes 28–63:  reserved
```

### 6.5 Command Frame (OBC → PPU)

```
0x01  ENABLE_DISCHARGE
0x02  DISABLE_DISCHARGE
0x03  IGNITE_CATHODE
0x04  SAFE_MODE (immediate HV shutdown)
0x05  SET_DISCHARGE_VOLTAGE  [bytes 1–2: uint16 mV]
0x06  SET_RL_ENABLED         [byte 1: 0/1]
0x07  SET_COIL_MANUAL        [bytes 1–6: 3× uint16 mA, overrides RL]
0xFE  RESET_FAULTS
0xFF  HARD_RESET
```

---

## 7. Subsystem 6 — Protection Circuits

### 7.1 Input Protection

| Element             | Component                          | Purpose                            |
|---------------------|------------------------------------|------------------------------------|
| Input fuse          | Littelfuse 0297015 (15 A blade)    | Hard fault protection              |
| Inrush limiter      | NTC Ametherm SL32 + bypass relay   | Limits inrush at power-on          |
| Reverse polarity    | Si4435DDY P-ch MOSFET              | Connector mis-mate protection      |
| Input TVS           | SMBJ28A (bidirectional)            | Bus transient suppression          |
| EMI filter          | Bourns SRF2012-900Y (900Ω @100MHz) | Common-mode noise                  |

### 7.2 Discharge Overcurrent (Hardware Latch)

The discharge plasma exhibits **negative incremental resistance** — current rises as voltage falls during an arc. Hardware protection must respond faster than the STM32 (µs vs ms).

**Circuit:** LM2904 comparator monitors discharge current sense. If I > 1.2 A (150% of nominal): output drives SR latch (74HC00 NOR latch) → pulls UCC28780 SS/ENABLE low → converter off within one switching cycle (< 7 µs). STM32 reads latch flag and can re-enable after fault clearance.

### 7.3 Arc Detection (< 5 µs Response)

An arc causes rapid discharge voltage collapse (dV/dt typically > 50 V/µs simultaneously with current spike).

**Circuit:** RC differentiator on voltage sense (R = 10 kΩ, C = 1 nF, τ = 10 µs) → LM2904 comparator (threshold: −0.5 V corresponding to dV/dt < −50 V/µs):

1. Arc comparator fires → SR latch → disables discharge converter (< 5 µs)
2. Output cap (10 µF) absorbs arc current during off-interval
3. Arc energy limit: ½ × 10×10⁻⁶ × 250² = **312 mJ** — far below structural damage threshold
4. After 2 ms blanking (RC-timed), converter auto-restarts
5. Arc rate > 10/s → permanent latch + STM32 fault flag

### 7.4 Coil Overcurrent

Cycle-by-cycle current limiting in LTC3609 (set by REF resistor) provides primary protection. STM32 raises a software fault if any coil channel exceeds 120% of setpoint for > 100 ms.

### 7.5 Safe-Mode

Triggered by:
- CAN command 0x04 (< 10 ms latency via firmware)
- Dedicated SAFE_MODE hardware line: GPIO pulled low by OBC → AND gate on all converter ENABLE pins (< 1 ms, hardware, independent of firmware state)

Safe-mode behaviour:
- All HV rails disabled (discharge, ignition)
- Coil currents ramp to zero over 10 ms (not hard-switched — stored coil energy → controlled freewheel to prevent voltage spikes)
- Keeper supply optionally maintained to keep cathode warm
- STM32 continues reporting telemetry

### 7.6 Thermal Protection

Two TMP100 I2C sensors: one on the discharge transformer, one on the digital board.

| Temperature | Action |
|---|---|
| > 85°C | Reduce discharge power to 50%, send thermal warning CAN frame |
| > 100°C | Full safe-mode |

---

## 8. Power Budget

Full operation: discharge running, cathode active, all coils at nominal.

| Subsystem                       | Output Power | Efficiency | 28 V Bus Input |
|---------------------------------|--------------|------------|----------------|
| HV discharge supply             | 200.0 W      | 88%        | 227.3 W        |
| Coil pre-regulator (28V → 9V)   | 36.0 W       | 97%        | 37.1 W         |
| Coil drivers ×3 (9V → coils)    | 24.0 W       | 89%        | 26.9 W         |
| Cathode heater supply           | 20.0 W       | 85%        | 23.5 W         |
| Keeper steady-state supply      | 22.5 W       | 86%        | 26.2 W         |
| Digital control (STM32 + CAN)   | 1.5 W        | —          | 1.5 W          |
| **TOTAL**                       | **304.0 W**  | **88.8%**  | **342.5 W**    |

**28 V bus current, full load:** 342.5 / 28 = **12.2 A**
**28 V bus current, minimum bus (22 V):** 342.5 / 22 = **15.6 A** — harness and fuse must be rated for this.

**Reduced-power mode** (coils minimal, heater off after ignition): ~255 W input, **9.1 A** at 28 V.

**PPU losses (heat dissipated):** 342.5 − 304.0 = **38.5 W**

---

## 9. Mass and Volume Estimate

### 9.1 PCB Assembly

| Board                           | Dimensions (est.)  | Mass   |
|---------------------------------|--------------------|--------|
| HV discharge + protection       | 100 × 80 mm        | 65 g   |
| Coil drivers ×3 + pre-reg       | 100 × 80 mm        | 55 g   |
| Cathode heater + keeper         | 80 × 60 mm         | 40 g   |
| Digital control (STM32 + CAN)   | 80 × 60 mm         | 30 g   |
| Connectors + wiring harness     | —                  | 45 g   |
| **PCB subtotal**                |                    | **235 g** |

### 9.2 Magnetics

| Component                   | Count | Unit mass | Total  |
|-----------------------------|-------|-----------|--------|
| HV flyback transformer (ETD32) | 1  | 35 g      | 35 g   |
| Coil pre-reg inductor        | 1    | 8 g       | 8 g    |
| Coil buck inductors (4.7 µH) | 3    | 4 g       | 12 g   |
| Heater/keeper transformer (EFD25) | 1 | 25 g   | 25 g   |
| EMI filter choke             | 1    | 12 g      | 12 g   |
| **Magnetics subtotal**       |      |           | **92 g** |

### 9.3 Enclosure

6061-T6 aluminium, 2 mm wall, external 160 × 120 × 50 mm. Spot shields (2 mm Al, per IC): ~30 g. Total enclosure mass: **~180 g**.

### 9.4 Total

| Category        | Mass      |
|-----------------|-----------|
| PCB assembly    | 235 g     |
| Magnetics       | 92 g      |
| Enclosure       | 180 g     |
| Fasteners/misc  | 25 g      |
| **TOTAL**       | **532 g** |

Target: < 600 g. Margin: 11%.

**Volume:** 160 × 120 × 50 mm = **960 cm³ (0.96 litres)**

Comparable to Busek BHT-200 PPU (~900 cm³, ~550 g flight heritage).

---

## 10. Radiation and Environmental Considerations

### 10.1 Orbit and TID

550 km SSO. TID behind 2 mm Al: ~2–5 krad/year. 5-year mission → **10–25 krad total**.

### 10.2 Component Strategy

**Tier 1 — Radiation-hardened** (critical control path):
- STM32F405 is not rad-hard. Options: (a) COTS + 3 mm Al spot shield for prototype; (b) VORAGO VA10820 (Cortex-M4, 300 krad, space-qualified) for flight; (c) STM32F405-RP (ST custom rad-hard variant, quote required).
- ADuM digital isolators: survive ~30–50 krad TID before threshold shift (ADI app note). Acceptable for 5-year mission.

**Tier 2 — COTS with spot shielding** (power conversion ICs):
- UCC28780, LTC3609, LM2904: characterise to 10 krad TID before flight. Apply 2 mm Al spot shields (~5 g each).
- GaN FETs (GS61008P): inherently lower TID sensitivity than Si CMOS (wide bandgap). SEGR not a concern below 100 V bus. No additional shielding required.
- SiC diodes (SCS220AE2): TID-resistant, forward voltage shift < 50 mV at 100 krad.

**Tier 3 — Replace for flight**:
- Capacitors: solid tantalum (hermetically sealed, KEMET T491 / AVX TPS) for bulk; C0G/X7R ceramic for decoupling. Avoid wet tantalum (outgassing), Z5U/Y5V (temperature sensitivity).
- Film capacitors (WIMA FKP2): confirm outgassing < 1% TML per ASTM E595.

### 10.3 Thermal

38.5 W dissipated as heat in vacuum (no convection). Conduction path: PCB thermal vias → enclosure → spacecraft structural panel (bolted, indium foil TIM).

- Spacecraft interface conductance: ~0.7 K/W (typical bolted 6U panel)
- Estimated steady-state ΔT above spacecraft interface: **25–35°C**
- All components rated ≥ 125°C junction temperature; derate to 85°C operating → ≥ 40°C margin

### 10.4 Single Event Effects (SEE)

| Device | SEE Concern | Mitigation |
|---|---|---|
| STM32F405 | SEU in SRAM/registers | IWDG + WWDG watchdog; triplicated safety-critical variables; OBC heartbeat reset |
| Gate drivers (ADuM) | SEU immunity characterised; LET > 60 MeV-cm²/mg | Acceptable |
| GaN FETs | No CMOS latch-up path | None required |
| Si MOSFETs (coil drivers) | SEGR if Vds approaches rated Vds | Derate Vds to 60%: SiR892DP at 30 V rated, max Vds in circuit 9 V (30%) — compliant |

---

## 11. Bill of Materials Summary (Key Parts)

| Ref  | Description                          | Part Number              | Qty | Notes |
|------|--------------------------------------|--------------------------|-----|-------|
| U1   | ACF flyback controller               | UCC28780PWPR (TI)        | 1   | Spot shield |
| Q1,Q2| Primary + clamp GaN FETs             | GS61008P (GaN Systems)   | 2   | 100 V / 30 A |
| U_GD | GaN gate driver                      | LMG1020 (TI)             | 2   | < 2Ω, < 5 ns |
| D1   | HV secondary rectifier (SiC SBD)    | SCS220AE2 (Wolfspeed)    | 1   | 600 V / 20 A |
| T1   | HV flyback transformer               | Custom ETD32, N87         | 1   | Custom wind |
| C1   | HV output capacitor (film)           | WIMA FKP2 10µF/400V      | 1   | Vacuum-safe |
| U2   | 28V→9V pre-reg controller            | LTC3891 (ADI)            | 1   | |
| Q3,Q4| Pre-reg sync buck FETs               | SiR622DP (Vishay)        | 2   | 60 V / 9.8 mΩ |
| U3–5 | Coil current-mode buck controllers   | LTC3609 (ADI)            | 3   | |
| Q5–10| Coil buck FETs (dual N-ch SO-8)      | SiR892DP (Vishay)        | 6   | 30 V / 9.5 mΩ |
| U6–8 | Coil current sense amps              | INA240A2 (TI)            | 3   | PWM rejection |
| U9   | Heater supply controller             | UCC28700 (TI)            | 1   | PSR, no optocoupler |
| T2   | Heater/keeper transformer            | Custom EFD25, N87        | 1   | Multi-winding |
| U10  | Arc detect + overcurrent comparators | LM2904 (TI)              | 1   | Quad |
| U11  | MCU                                  | STM32F405RGT6 (ST)       | 1   | 168 MHz, FPU; spot shield |
| U12–15| Digital isolators (2-ch each)       | ADuM1201BRZ (ADI)        | 4   | 8 channels total |
| U16  | Isolated SPI DAC interface           | ADuM3471 (ADI)           | 1   | Quad SPI |
| U17  | CAN transceiver                      | TCAN1042V (TI)           | 1   | ISO 11898 |
| U18,19| PCB temperature sensors             | TMP100 (TI)              | 2   | I2C |
| F1   | Input fuse                           | Littelfuse 0297015        | 1   | 15 A blade |
| D2   | Input TVS                            | SMBJ28A (Vishay)         | 1   | Bidirectional |
| L_EMI| EMI common-mode choke               | SRF2012-900Y (Bourns)    | 1   | |
| —    | Spot shields                         | 2 mm 6061-T6 Al          | —   | Machined per-IC |

---

## 12. Design Notes and Open Items

### Pre-CDR Open Items

1. **HV transformer winding spec:** Custom-wound ETD32, target leakage Llk < 200 nH and 2.5 kV primary-secondary withstand. Magnetics vendor required (Lintec, Pulse Engineering, or equivalent). First-article measurement of Lm, Llk, Rdc mandatory before layout finalisation.

2. **RL policy network size:** Hidden layer dimensions are determined post-training. Firmware must accommodate up to 128×128 MLP within 1 ms. If larger networks are needed, switch MCU to STM32H7 (480 MHz, pin-compatible) without board redesign.

3. **Coil resistance/inductance measurement:** DCR and L values above are estimates from turn count and assumed wire gauge. Actual thruster coil impedances must be measured before LTC3609 compensation networks are finalised.

4. **Arc detection threshold calibration:** 50 V/µs threshold is typical; actual threshold depends on the specific thruster's plasma impedance. Requires in-vacuum characterisation test (Paschen breakdown in Kr, low-pressure arc simulation) to set comparator threshold without spurious triggering.

5. **Keeper feedback optocoupler:** If optocoupler is used for keeper supply feedback, confirm epoxy outgassing meets < 1.0% TML, < 0.1% CVCM (ASTM E595). Preferred alternative: switch to PSR control on keeper winding (eliminates optocoupler entirely).

6. **Radiation test campaign:** TID functional test of UCC28780, LTC3609, STM32F405 to 10 krad required before PDR.

7. **Thermal model:** FE thermal model of enclosure + PCB stack (Ansys Icepak or equivalent) needed to verify 35°C ΔT estimate and confirm no component exceeds derating limit at 38.5 W dissipation in vacuum.

### PCB Design Rules

- All resistor dividers on HV signals: two series resistors of half total value (if one fails open, divider saturates rather than applying HV to ADC pin)
- HV trace clearance: > 3 mm to all other nets (IPC-2221A Class B, 250 V + 50% margin)
- Creepage for 600 V ignition: > 6.4 mm (IPC-2221A, pollution degree 2; vacuum reduces requirement but retained as margin)
- No electrolytics; only film, X7R/C0G ceramic, or hermetically sealed tantalum
- No solder mask openings under high-current traces; use solid copper pours
- Vds derating: all MOSFETs at ≤ 60% of rated Vds (SEGR mitigation)

---

*Document version: 0.1 — Preliminary Design*
*Next milestone: CDR*
*Companion documents: EXPLAINER.md (system parameters), VALIDATION.md (test programme), explainer.md §18 (STM32 RL inference architecture)*
