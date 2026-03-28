# ẍ Market & Technical Analysis
**HET Product Strategy — Where to Play**
*March 2026*

---

## 1. Where the Market Is Going

The constellation race has converged on **300–600W** as the standard power class for 100–300kg satellites at 400–1,200km LEO:
- **OneWeb** (1,200km): Busek BHT-350, 300W nominal, Kr/Xe, 17mN
- **Starlink V2** (550km): In-house argon HET, 4.2kW, 170mN, 2.1kg — sets the performance benchmark but not for sale
- **Amazon Kuiper** (590–630km): In-house Kr HET, specs undisclosed

This standard LEO/MEO constellation segment is getting crowded:
- Busek BHT-350 (US, ITAR) — only flight-proven sub-kW HET at constellation scale (250+ units on OneWeb)
- Safran EPS-X00 (FR) — Kr-compatible, first deliveries H1 2025, targets >200kg sats, high price culture
- Exotrail Spaceware Mini (FR) — 300–600W, Xe+Kr, strong commercial traction, flight heritage TBD

**The underserved market is VLEO (200–350km)** — where no European supplier has a qualified thruster designed for *continuous drag compensation*. This is ẍ's strategic opening.

---

## 2. VLEO Drag Physics — 200km Imaging Constellation

### Drag Force Formula
```
F_drag = ½ × ρ × Cd × A × v²

Constants:
  Cd ≈ 2.5 (free molecular flow regime)
  v  ≈ 7,800 m/s (circular orbit)
```

### Atmospheric Density by Altitude
| Altitude | Density (kg/m³) | Notes |
|---|---|---|
| 200 km | ~3×10⁻¹⁰ | Highly variable; solar max can be 10× this |
| 250 km | ~6×10⁻¹¹ | |
| 300 km | ~2×10⁻¹¹ | |
| 400 km | ~2×10⁻¹² | ISS altitude |
| 550 km | ~6×10⁻¹³ | Starlink altitude |

### Required Drag Compensation Thrust at 200km
| Satellite | Mass | Frontal Area | Moderate Solar | High Solar (10×) |
|---|---|---|---|---|
| Small imaging sat | 50 kg | 0.10 m² | **2.3 mN** | 23 mN |
| Medium imaging sat | 100 kg | 0.25 m² | **5.7 mN** | 57 mN |
| Large imaging sat | 200 kg | 0.50 m² | **11.4 mN** | 114 mN |

**Key finding:** At 200km, only **≤80kg satellites** are practical for sustained operations with a ~200W thruster. High solar activity events are the limiting case — a 200W thruster producing 10–15mN has ~5× margin for a 50kg satellite at moderate solar activity, but that margin collapses at solar maximum. Mission planning must account for this with operational altitude adjustments during solar maximum.

### Power Required for Drag Compensation
For a 50kg sat at 250km needing ~1mN continuous thrust:
- At 1,400s Isp, η=35%: **~60–80W** — very achievable
- For a 100kg sat at 250km needing ~2.2mN: **~130–180W**

At 200km the power demand roughly doubles — a 200W thruster is well-matched to a 50–100kg satellite at 220–280km altitude.

---

## 3. Current HET Product Landscape

### Key Products (sub-2kW class)

| Product | Supplier | Country | Power (W) | Thrust (mN) | Isp (s) | Propellant | Status |
|---|---|---|---|---|---|---|---|
| BHT-100 | Busek | US (ITAR) | 100 | 7 | 1,000 | Xe/Kr/I₂ | Flight heritage |
| BHT-200 | Busek | US (ITAR) | 200 | 13 | 1,390 | Xe/Kr/I₂ | Flight heritage |
| BHT-350 | Busek | US (ITAR) | 300 nom. | 17 | 1,244 | Xe/Kr/I₂ | **250+ units, OneWeb** |
| BHT-600 | Busek | US (ITAR) | 600 nom. | 39 | 1,300–1,500 | Xe/Kr/I₂ | Flight heritage |
| EPS-X00 | Safran | FR | 200–1,000 | 15–75 | 1,300–1,800 | Xe/Kr | First deliveries H1 2025 |
| Spaceware Mini | Exotrail | FR | 300–600 | 12–32 | 1,300–1,600 | Xe/Kr | Flight heritage TBD |
| Spaceware Micro | Exotrail | FR | 150 | 7 | ~1,000 | Xe | In development |
| HT-100 | Sitael | IT | 100–250 | 4–13 | 900–1,400 | Xe/Kr | Ground-tested, Kr record |
| HT-400 | Sitael | IT | 350–750 | 20–45 | 1,300–1,700 | Xe | Ground-tested |
| MUSIC | Aliena | SG | 10–100 | 3.6 @ 84W | 658 | Xe | **ELITE VLEO 2025 launch** |
| NPT30-I2 | ThrustMe | FR | 35–65 | 1.1 | 2,450 | I₂ (solid) | Flight heritage (not HET) |

### SpaceX Performance Benchmark (not for sale)
- **Starlink V1/V1.5:** Kr HET, ~60mN, ~1,500s Isp, ~300–400W estimated
- **Starlink V2 Mini:** Ar HET, **170mN, 2,500s Isp, 4.2kW, 2.1kg** — extraordinary mass-to-power ratio

---

## 4. Propellant Economics

### Cost per kg (2025)
| Propellant | Cost/kg | Availability | Notes |
|---|---|---|---|
| Xenon | $5,000–$12,000 | Constrained | 0.09 ppm in atmosphere; air separation byproduct |
| Krypton | $2,100–$4,800 | Moderate | 1 ppm in atmosphere |
| Kr/Xe blend | $300–$800 | Good | Byproduct of LOX production — cheapest noble gas option |
| Argon | $7–$15 | Abundant | 0.93% of atmosphere — essentially free |

### 5-Year Mission Propellant Cost (300kg satellite, 250m/s ΔV, 1,400s Isp, ~54kg propellant)
| Propellant | Total Cost |
|---|---|
| Xenon | $270K–$648K |
| Krypton | $113K–$259K |
| Blend | $16K–$43K |
| Argon | ~$400 |

For a 648-satellite constellation: **Krypton vs. Xenon saves $100M–$400M over constellation lifetime.** This is why every new constellation has moved to Kr or cheaper.

### Krypton vs. Xenon Performance Trade-off (same thruster)
- **Isp:** Kr gives +100–190s higher Isp (lower atomic mass → higher exhaust velocity) ✅
- **Thrust:** ~10–15% lower on Kr ❌ (manageable for LEO)
- **Efficiency:** ~7–8% lower on Kr ❌
- **Wall erosion:** 1.5–2× higher on Kr ❌ → **magnetic shielding is essential for Kr operation >5,000hrs**

---

## 5. Market Gaps — Where ẍ Can Win

### Gap 1: VLEO-Optimised European HET (Primary Target)
**200–350km sustained operation, 100–300W, Kr-native, magnetically shielded**

No European supplier has a flight-qualified VLEO-optimised HET. Only player with any VLEO HET heritage: Aliena (Singapore, ELITE 2025). The DARPA TALOS programme and ESA AETHER project confirm institutional demand.

Requirements for sustained VLEO operation that current products don't address:
- High duty cycle capability (>8,000 hours continuous)
- Magnetic shielding specifically tuned for Kr at high-duty-cycle (not adapted from Xe designs)
- Solar activity tolerance — thruster must handle 3–5× thrust demand variability
- Thermal management for continuous firing

### Gap 2: 300–600W, Kr-Native, ITAR-Free, European
The BHT-350 is ITAR-restricted. Safran EPS-X00 just entering market with GEO-pricing culture. Exotrail Mini's flight heritage TBD. **A European, ITAR-free, flight-qualified 300–500W Kr-primary thruster does not exist today.**

### Gap 3: Dual-Propellant Krypton + Argon Capable
SpaceX proved argon at scale. No commercial supplier offers a flight-qualified Ar-capable HET. If a new entrant can demonstrate Kr+Ar operation, this is 3–5 years ahead of the market.

---

## 6. Assessment of Tiz's 200W Design

**Verdict: Well-positioned for the VLEO smallsat niche. Right power class for the right reasons.**

### What 200W gets you (estimated Kr performance)
- Thrust: **10–15 mN**
- Isp: **1,300–1,500s on Kr**
- Efficiency: ~30–40%

### Target satellite at 200W
| Altitude | Max satellite mass | Continuous thrust margin |
|---|---|---|
| 200km (moderate solar) | ~50–80kg | 2–5× |
| 250km | ~100–150kg | 3–6× |
| 300km | ~200kg+ | comfortable |

### Strategic fit
- VLEO 220–300km smallsat constellation (50–120kg) — **best fit**
- Drag compensation for small imaging satellites — **strong fit**
- Station-keeping at standard LEO (400–600km) for 50–150kg sats — **works but overkill**
- Standard LEO constellation (OneWeb-scale, 200kg+) — **underpowered; would need 300–500W variant**

### Recommended evolution path
Start at 200W → validate → throttle range 100–300W → position as VLEO-specialist product, then develop 500W variant for standard LEO constellation market as Phase 2.

---

## 7. Critical IP Question

Tiz's 200W design IP ownership must be resolved before ESA BIC submission. The business plan requires a clear IP ownership statement.

**Possibilities:**
- University research → IP likely owned by university; need licence or assignment agreement
- Personal/independent project → Tiz owns it; needs to be assigned to ẍ OÜ on incorporation
- Developed while employed (ABB or elsewhere) → employer may have claim; needs legal review

**Action:** Get a one-page IP clearance memo from an IP/tech lawyer before submission. Budget ~€1–2K. If the IP isn't cleanly owned by the company at time of application, the ESA BIC contract cannot be signed.

---

## 8. Recommended Target Specification for ẍ Phase 1 Product

| Parameter | Target | Rationale |
|---|---|---|
| Power class | 100–300W (nominal 200W) | Tiz's existing design; VLEO smallsat sweet spot |
| Thrust | 5–15 mN | Drag compensation for 50–150kg at 220–300km |
| Isp (Kr) | 1,300–1,500s | Competitive; Kr-native design bonus |
| Propellant | Krypton primary | Cost, supply chain, performance |
| Lifespan | >8,000 hours | 5-year VLEO mission with continuous firing |
| System mass | <3 kg (thruster + PPU) | CubeSat/smallsat bus compatible |
| Duty cycle | Continuous | VLEO drag compensation requirement |
| ITAR status | ITAR-free | Mandatory for European institutional customers |
| Target market | 50–120kg VLEO smallsats, 220–300km | Underserved; no qualified European product |
| Phase 2 | 300–500W variant | Standard LEO constellation market |

---

## 9. Key References
- Hofer, R. et al., "Magnetically Shielded Hall Thruster", NASA/JPL, 2012
- Mikellides, I. et al., "Magnetic Shielding of Walls from the Unmagnetized Ion Beam", J. Applied Physics, 2014
- Busek BHT series specs: busek.com/hall-thrusters
- Safran EPS-X00 qualification status: ResearchGate, IEPC 2024
- Aliena MUSIC / ELITE VLEO mission: CEAS Space Journal, 2025
- SPT-100 Kr vs Xe comparison: IEPC-2011-003
- DARPA TALOS programme: darpa.mil
- MarketsandMarkets satellite propulsion ($5.19B by 2030)
- Mordor Intelligence electric propulsion systems ($17B by 2031)
- DataIntelo Hall thruster market (~$3.8B by 2032)
