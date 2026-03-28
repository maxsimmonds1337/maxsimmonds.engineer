# ẍ HET Design Trade-Space
*What are the input variables and how do they drive the thruster specification?*

---

## The Full Input Variable Space

Sat size and orbit altitude are the most visible inputs but they're downstream of a longer chain. Here's the complete picture:

```
MISSION INPUTS
    │
    ├── Orbital mechanics
    │       ├── Altitude (km)             → drives drag force
    │       ├── Inclination (°)           → affects drag slightly (polar = marginally more)
    │       └── Solar activity (F10.7)    → multiplies atmospheric density 5–10×
    │
    ├── Satellite design
    │       ├── Mass (kg)                 → affects drag force magnitude
    │       ├── Frontal area (m²)         → affects drag force magnitude
    │       ├── Power budget for EP (W)   → hard ceiling on thruster input power
    │       ├── Mass budget for EP (kg)   → constrains thruster + PPU + propellant
    │       └── Volume budget for EP (L)  → constrains form factor
    │
    └── Mission profile
            ├── Mission lifetime (yrs)    → drives total impulse & lifespan requirement
            ├── Duty cycle                → continuous (VLEO) vs episodic (LEO orbit raise)
            ├── ΔV budget (m/s)          → drives propellant mass
            └── Manoeuvre types:
                    ├── Drag compensation     (continuous, low thrust, VLEO)
                    ├── Orbit raising         (episodic, high thrust, all altitudes)
                    ├── Station-keeping       (episodic, low thrust, LEO)
                    ├── Collision avoidance   (episodic, any thrust)
                    └── End-of-life deorbit   (ESA <5yr reentry rule)

        ↓

THRUSTER DESIGN OUTPUTS
    ├── Required thrust (mN)
    ├── Required Isp (s)         ← derived from propellant mass budget
    ├── Required power (W)
    ├── Required total impulse (kN·s)
    ├── Required lifespan (hrs)
    └── Required duty cycle (%)
```

---

## Variable 1: Orbital Altitude

The single biggest lever. Atmospheric density drops ~3 orders of magnitude between 200km and 600km.

### Density Model (NRLMSIS 2.0, moderate solar activity F10.7~150)

| Altitude (km) | Density (kg/m³) | vs. 500km |
|---|---|---|
| 200 | ~3.0×10⁻¹⁰ | ×500 |
| 250 | ~6.0×10⁻¹¹ | ×100 |
| 300 | ~2.0×10⁻¹¹ | ×33 |
| 350 | ~8.0×10⁻¹² | ×13 |
| 400 | ~2.0×10⁻¹² | ×3.3 |
| 500 | ~6.0×10⁻¹³ | ×1 (baseline) |
| 600 | ~2.0×10⁻¹³ | ×0.33 |

**Solar activity effect:** At solar maximum, density at 200–300km can be **5–10× higher** than moderate solar activity values above. This is mission-critical — a thruster sized for moderate solar activity at 250km will be overwhelmed at solar max. Either:
- Design for solar max (overspec most of the time), or
- Plan to raise orbit during solar max events (operationally complex)

---

## Variable 2: Satellite Mass + Frontal Area

```
F_drag = ½ × ρ × Cd × A × v²

Cd ≈ 2.2–3.7 in free molecular flow (VLEO)
    Use 2.5 as conservative planning figure
v  ≈ 7,800 m/s (circular LEO, barely changes with altitude)
```

**Frontal area is not simply proportional to mass** — it depends on satellite shape and attitude. Typical ratios:

| Form factor | Mass (kg) | Frontal area (m²) | A/m ratio |
|---|---|---|---|
| 6U CubeSat | 8–12 | 0.02–0.04 | ~0.003 |
| 12U CubeSat | 12–24 | 0.03–0.06 | ~0.003 |
| ESPA-class microsat | 50–150 | 0.10–0.25 | ~0.002 |
| Medium smallsat | 150–300 | 0.30–0.60 | ~0.002 |
| Large smallsat | 300–500 | 0.50–1.00 | ~0.002 |

Note: CubeSats have *worse* A/m ratios — drag hits them proportionally harder than larger satellites.

### Drag Force Matrix (mN) — Moderate Solar Activity

|  | 200km | 250km | 300km | 400km | 500km |
|---|---|---|---|---|---|
| **6U CubeSat** (10kg, 0.03m²) | 1.3 | 0.26 | 0.087 | 0.0087 | 0.0026 |
| **50kg microsat** (0.10m²) | 4.3 | 0.86 | 0.29 | 0.029 | 0.0086 |
| **100kg smallsat** (0.25m²) | 10.8 | 2.2 | 0.72 | 0.072 | 0.022 |
| **200kg smallsat** (0.50m²) | 21.6 | 4.3 | 1.4 | 0.14 | 0.043 |
| **300kg smallsat** (0.70m²) | 30.2 | 6.1 | 2.0 | 0.20 | 0.060 |

**Solar max: multiply all values by 5–10.**

---

## Variable 3: Mission ΔV Budget

ΔV drives propellant mass, which constrains Isp choice (higher Isp = less propellant for same ΔV).

**Tsiolkovsky rocket equation:**
```
ΔV = Isp × g₀ × ln(m₀ / m_f)
→ propellant mass fraction = 1 - exp(-ΔV / (Isp × 9.81))
```

### Propellant mass for 100kg satellite by ΔV and Isp

| ΔV (m/s) | Isp 800s | Isp 1,200s | Isp 1,500s | Isp 2,000s |
|---|---|---|---|---|
| 50 | 0.62 kg | 0.42 kg | 0.34 kg | 0.25 kg |
| 150 | 1.84 kg | 1.24 kg | 1.00 kg | 0.75 kg |
| 300 | 3.61 kg | 2.44 kg | 1.97 kg | 1.49 kg |
| 500 | 5.87 kg | 3.99 kg | 3.23 kg | 2.44 kg |
| 1,000 | 11.3 kg | 7.77 kg | 6.31 kg | 4.80 kg |

### Typical ΔV budgets by mission type

| Mission type | Altitude | ΔV estimate | Notes |
|---|---|---|---|
| VLEO drag compensation only | 250km, 3yr | ~450 m/s | Continuous; mostly drag; deorbit is free (natural decay) |
| VLEO drag comp + solar max margin | 250km, 3yr | ~900 m/s | Design for solar max events |
| LEO orbit raising (inject→operational) | 350→550km | ~150–200 m/s | One-time cost |
| LEO station-keeping, 5yr | 550km | ~50–100 m/s | Small but adds up across constellation |
| LEO collision avoidance, 5yr | 550km | ~20–50 m/s | Growing requirement |
| LEO end-of-life deorbit | 550km→decay | ~150–200 m/s | FCC/ESA <5yr rule |
| **Full LEO mission budget (5yr)** | **550km** | **~400–550 m/s** | |
| **Full VLEO mission budget (3yr)** | **250km** | **~900–1,200 m/s** | Dominated by drag comp |

---

## Variable 4: Satellite Power Budget for Propulsion

The thruster cannot draw more power than the satellite bus allocates to it. This is often the **hardest constraint** — it sets the ceiling on thrust.

Typical total satellite power vs. what's available for propulsion:

| Satellite class | Total power (W) | Propulsion allocation (15–25%) | Max thruster input |
|---|---|---|---|
| 6U CubeSat | 20–40 W | 3–10 W | ~5–10 W (ion/FEEP only) |
| 12U CubeSat | 40–80 W | 6–20 W | ~10–20 W |
| 50kg microsat | 100–200 W | 15–50 W | ~30–50 W |
| 100kg smallsat | 300–600 W | 45–150 W | ~80–200 W |
| 200kg smallsat | 600–1,200 W | 90–300 W | ~150–400 W |
| 300kg smallsat | 1,000–2,000 W | 150–500 W | ~250–600 W |

**Important:** The PPU efficiency (typically 88–93%) means the thruster input power ≠ satellite bus power drawn. A 400W thruster at 90% PPU efficiency draws ~445W from the bus.

---

## Variable 5: Propellant Choice

| Propellant | Ionisation energy (eV) | Atomic mass (u) | Isp advantage | Cost/kg | Notes |
|---|---|---|---|---|---|
| Xenon (Xe) | 12.1 | 131.3 | Baseline | $5–12K | Easiest to ionise; highest thrust density; supply risk |
| Krypton (Kr) | 14.0 | 83.8 | +100–190s Isp vs Xe | $2–5K | Lower mass → higher exhaust velocity; harder to ionise |
| Argon (Ar) | 15.8 | 39.9 | +300–500s Isp vs Xe (theoretically) | ~$10 | Very hard to ionise; SpaceX has done it at 4.2kW |
| Iodine (I₂) | 10.5 | 127 | Similar to Xe | ~$200 | Solid storage (no pressure vessel); ThrustMe speciality |
| Nitrogen (N₂) | 15.6 | 28 | Poor thrust density | Near zero | Air-breathing only; very hard |

**Kr vs Xe on same thruster (measured, SPT-100 data):**
- Isp: Kr gives +150s at same discharge voltage ✅
- Thrust: −12% at same power ❌ (lower mass flow)
- Efficiency: −7% ❌
- Erosion: +50–100% on cathode ❌ → **magnetic shielding non-optional for Kr at high duty cycle**

**Design implication:** A thruster *designed* for Kr from scratch (optimised channel length, discharge voltage, magnetic topology for 14.0eV ionisation energy) can recover 3–5% efficiency vs. an adapted Xe thruster run on Kr.

---

## Variable 6: Duty Cycle

Often overlooked. Profoundly affects lifespan requirement.

| Mission type | Duty cycle | Hours/year at duty cycle | 5yr total hours |
|---|---|---|---|
| VLEO drag compensation | ~90–100% | ~7,900 hr/yr | **~39,500 hours** |
| LEO orbit raising (one-time) | 100% during raise (~weeks) | ~500–1,000 hr total | ~1,000 hours |
| LEO station-keeping | ~5–10% | ~440–880 hr/yr | ~2,000–4,400 hours |
| Combined LEO mission | ~15–25% | ~1,300–2,200 hr/yr | ~6,500–11,000 hours |

**Critical finding:** VLEO drag compensation at near-100% duty cycle demands 30,000–40,000+ hour lifespan for a 5-year mission. **No current commercial HET achieves this.** The industry standard is 10,000–15,000 hours. This is the entire reason ẍ's magnetic shielding is necessary — not just nice to have.

---

## The Derived Thruster Spec: Working Backwards

Pick a target mission → derive the thruster requirements:

### Example A: VLEO Imaging Constellation (ẍ Phase 1 target)
```
Satellite:    80kg, 0.20m² frontal area
Altitude:     250km
Solar:        Design for moderate + 3× solar max margin
Mission life: 3 years continuous operation

Step 1 — Drag force:
  Moderate:  F = ½ × 6×10⁻¹¹ × 2.5 × 0.20 × 7800² = 0.91 mN
  Solar max: F ≈ 0.91 × 5 = 4.5 mN
  Design to: 5 mN (includes margin)

Step 2 — ΔV (drag compensation dominated):
  Δv = F × t / m = 5×10⁻³ × (3×365×24×3600) / 80 ≈ 590 m/s (continuous thrust assumption)
  Actual: ~400–600 m/s (some natural decay helps)
  Design to: 600 m/s

Step 3 — Propellant mass (Isp = 1,400s Kr):
  fraction = 1 - exp(-600 / (1400 × 9.81)) = 1 - exp(-0.0437) = 4.3%
  propellant = 80 × 0.043 = 3.4 kg Kr

Step 4 — Power (at 5mN thrust, 1,400s Isp, η=35%):
  Jet power = ½ × F × ve = ½ × 5×10⁻³ × (1400 × 9.81) = 34.3 W
  Input power = 34.3 / 0.35 = 98 W

Step 5 — Lifespan:
  3 years × 365 × 24 × 0.90 duty cycle = 23,652 hours
  → Need >25,000 hour rated life at this power level

RESULT: 5mN, 1,400s Isp, ~100W input, 25,000hr life, 3.4kg Kr
→ This is a ~100W thruster running Kr with magnetic shielding.
→ Well below 200W — this is actually a 100W product for this mission.
```

### Example B: LEO Constellation (IRIS2 / OneWeb-scale)
```
Satellite:    200kg, 0.45m² frontal area
Altitude:     600km (operational), inject at 400km
Mission life: 7 years

Step 1 — Drag at 600km:
  F = ½ × 2×10⁻¹³ × 2.5 × 0.45 × 7800² = 0.0068 mN (negligible)
  Station-keeping: ~5–15 mN episodic

Step 2 — ΔV budget:
  Orbit raising 400→600km:  ~120 m/s
  7yr station-keeping:       ~140 m/s
  Collision avoidance:       ~60 m/s
  Deorbit (600→decay):       ~200 m/s
  Total:                     ~520 m/s

Step 3 — Propellant mass (Isp = 1,500s Kr):
  fraction = 1 - exp(-520 / (1500 × 9.81)) = 3.4%
  propellant = 200 × 0.034 = 6.8 kg Kr

Step 4 — Power for orbit raising (want 25–35mN to raise in reasonable time):
  At 30mN, 1,500s Isp, η=40%:
  Jet power = ½ × 30×10⁻³ × (1500 × 9.81) = 220 W
  Input power = 220 / 0.40 = 550 W

Step 5 — Lifespan:
  Duty cycle ~20% average over 7yr
  = 7 × 365 × 24 × 0.20 = 12,264 hours → need >15,000hr life

RESULT: 30mN, 1,500s Isp, ~550W input, 15,000hr life, 6.8kg Kr
→ This is a 500–600W thruster — the BHT-350 replacement.
```

### Example C: The "throttleable covers both" question
```
Can one thruster do both missions?

Mission A needs: 5mN @ 100W (VLEO, continuous)
Mission B needs: 30mN @ 550W (LEO, episodic orbit raising)

Throttle ratio: 5.5:1 (power), 6:1 (thrust)

Is this feasible?
- Existing products with wide throttle: BHT-350 runs 200–600W (3:1 ratio)
- SpaceX thrusters reportedly run wider ranges
- 5:1 power throttle is aggressive for a HET — plasma can extinguish below a
  minimum discharge current, and efficiency drops sharply at low throttle
- Practical maximum: ~3:1 to 4:1 throttle range before significant efficiency loss

VERDICT: A single thruster cannot optimally serve both missions.
Better approach: Two products sharing as much architecture as possible —
  - Product 1: 50–200W, optimised for VLEO continuous drag compensation
  - Product 2: 300–600W, optimised for LEO orbit raising + constellation use
  Channel diameter, magnetic circuit, and PPU are different.
  Cathode, propellant feed system, and AI controller can be shared.
```

---

## The Decision Matrix: What Power Class Should ẍ Build First?

| Criterion | 100–200W (VLEO) | 300–600W (LEO constellation) |
|---|---|---|
| Market readiness (customers buying now) | Low — emerging | High — OneWeb, IRIS2, defence |
| Competition | Very low (no European qualified) | Medium (Safran EPS-X00, Exotrail Mini) |
| Revenue per unit | €40K–€100K | €80K–€160K |
| Technical risk | Lower (smaller, easier to test) | Moderate |
| Testable on €60K ESA BIC budget | Yes | Yes (marginally) |
| Lifespan requirement | **Extreme (25,000+ hrs)** | Moderate (12,000–15,000 hrs) |
| Magnetic shielding necessity | **Critical** | Important |
| ITAR gap (European opportunity) | Moderate | **Strong** |
| IRIS2 alignment | Indirect | **Direct** |
| Path to IOD in 3 years | Harder (need VLEO-specific customer) | Clearer |

**Recommendation: Build 300–600W first, design the architecture for throttleability down to 100–200W as Phase 2.**

Reason: The LEO constellation market buys now. The VLEO market buys in 3–5 years. Revenue matters for survival. But the VLEO lifespan requirement (25,000+ hours) actually *demands* the magnetic shielding innovation more than the LEO case does — so validating the shielding at lower duty cycle in LEO first is lower risk, then certifying for VLEO high-duty-cycle operation is a credible Phase 2.

---

## Summary: Key Numbers to Know

```
Design a thruster → work backwards from:

1. Thrust needed     = drag force × margin factor (3–5×)
2. Isp choice        = driven by propellant mass budget (higher Isp = less fuel)
3. Input power       = (thrust × exhaust velocity) / (2 × efficiency)
                     = (F × Isp × 9.81) / (2 × η)
4. Propellant mass   = satellite mass × (1 - exp(-ΔV / (Isp × 9.81)))
5. Lifespan          = mission duration × duty cycle × margin (1.5×)

Key efficiency figure: η ≈ 35–45% for a well-designed sub-kW HET on Kr
Key exhaust velocity: ve = Isp × g₀ = 1,400 × 9.81 = 13,734 m/s (at 1,400s Isp)
```

---

*See also: MARKET_ANALYSIS.md for competitive landscape, BUSINESS_PLAN_DRAFT.md for application context*
