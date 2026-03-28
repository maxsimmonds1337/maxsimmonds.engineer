# Business Plan — ẍ (xdoubledot)
**ESA BIC Estonia Application — Draft v0.1**

*Authors: Max Simmonds, Tiziano Fiore*
*Date: March 2026*
*Reference: BIC-0004 v5.1*

> **Working notes:** Sections marked `[TODO]` need input from both founders before submission. Do not submit with TODOs remaining. Remove all working notes before final version. Target: 15 pages core, max 20 pages + appendices.

---

## Executive Summary

The space sector faces a critical bottleneck: every satellite that needs to maintain or change its orbit depends on electric propulsion — and the dominant technology, the Hall Effect Thruster (HET), has a fundamental lifespan problem. High-energy ions erode the cathode over time, limiting operational life to 10,000–15,000 hours and forcing satellite operators to accept shortened missions, carry redundant hardware, or pay for expensive replacements.

**ẍ (xdoubledot)** is developing the next generation of Hall Effect Thrusters for the Very Low Earth Orbit (VLEO) market, with a core innovation in AI-guided dynamic magnetic shielding that diverts erosive ion bombardment away from critical cathode surfaces. Our target is a 5–10x extension of thruster operational life, enabling the persistent, low-cost VLEO missions that the market demands but current hardware cannot support.

We are a European, ITAR-free propulsion company based in Tallinn, Estonia, targeting the emerging mega-constellation and VLEO satellite market. Our founding team has direct, hands-on experience inside the incumbent European propulsion industry — including time at Safran (the leading European HET manufacturer), Thales Alenia Space, and ESA itself — giving us rare insider knowledge of where current products fall short and where the commercial opportunity lies.

The global Hall thruster market is projected to exceed $1.7T through 2030. We are targeting the European segment, valued at €15.6B by 2030, with an initial focus on VLEO constellation operators and the EU's IRIS2 sovereign connectivity programme. Revenue model: direct hardware unit sales (€50K–€300K per unit) with a software-as-a-service layer for AI-driven orbit control and predictive maintenance.

We are seeking ESA BIC Estonia incubation to fund the proof-of-concept validation phase: demonstrating stable plasma discharge with our AI-optimised magnetic field geometry, and establishing the IP foundation for the platform.

---

## 1. Team & Company Setup

### 1.1 The Team

**Tiziano Fiore — Co-Founder & CEO**

Tiziano is an electric propulsion engineer with hands-on experience designing, building, and testing electric thrusters. He designed and characterised a 1 kW arcjet thruster achieving 130 mN thrust, 600 s specific impulse, and greater than 50% efficiency — building the full test infrastructure including thermal-vacuum test facilities and plasma diagnostic systems (Retarding Potential Analyser ion probes). He holds an MBA from Aalto University and has prior professional experience at ABB.

As CEO, Tiziano leads business development, customer engagement, and technical direction for the thruster hardware programme.

`[TODO: Tiz — add more detail: degree(s), university, graduation year, full ABB role, any publications or conference papers, any space sector network contacts. Also confirm the arcjet work — was this university research, personal project, or company work? This is our strongest technical credential and reviewers will probe it.]`

**Max Simmonds — Co-Founder & CTO**

Max is an electrical and electronic engineer with 9 years of experience spanning space agencies, Tier 1 aerospace primes, and hardware startups. He holds an MEng (Hons) in Electrical and Electronic Engineering from the University of Plymouth (2017), where he received Engineering Excellence and Technical Innovation awards.

*ESA Young Graduate Trainee, ESTEC (2017–2018):* Max joined ESA's competitive Young Graduate Trainee programme at the European Space Research and Technology Centre in Noordwijk, Netherlands. His work focused on discrete-time modelling of high-frequency switch-mode power converters — the power electronics that form the core of Hall thruster Power Processing Units (PPUs). This work was co-authored and published in IEEE COMPEL (2018): *"Discrete-time modelling of pulse-width modulated DC-DC converters."*

*Senior Electronics Engineering Specialist, Safran Electrical & Power (2018–2022):* Max worked in Safran's electrical and power division on next-generation digital Generator Control Units (GCUs) for the Airbus A380. The work involved reverse-engineering existing analogue GCU circuits into validated mathematical models, testing digital implementations against the analogue references, translating to High Side (HS) requirements, implementing in hardware, and verifying in a test cell with an actual aircraft generator. This end-to-end power electronics development cycle — from modelling through hardware verification against a real high-power load — is directly transferable to Hall thruster Power Processing Unit (PPU) development, which faces analogous challenges of controlling a high-power, variable-impedance load.

*Thales Alenia Space:* Max worked on miniature cryogenic coolers for space instruments at Thales Alenia Space. Thales is identified in ẍ's competitive landscape as a potential customer and system integration partner.

*CERN (2016):* Placement on the Antiproton Decelerator facility, contributing to repair and upgrade work. Published a CERN technical report on fiber optic component reverse engineering.

*National Instruments / NASA contractor (2014–2015):* 13-month industrial placement; worked with NASA contractors on computer code for the International Space Station astronaut health monitoring system.

*TEO Robotics Ltd (2022–2025):* Founder and sole director of a profitable UK engineering consultancy (Companies House no. 14261065), delivering hardware and software engineering services across automotive, industrial, and aerospace clients.

*nCode OÜ / Purple Parrot (2024–present):* Co-founder of a Tallinn-based hardware startup developing an AI-powered baby monitor, currently incubated at Tehnopol Startup Incubator — the ESA BIC Estonia Tallinn partner. This venture is being handed to Max's co-founder to allow Max to focus on ẍ.

*Starship Technologies (current):* `[TODO: Max — add role title and brief description of work. Note: Starship Technologies is the autonomous delivery robot company. If this is a different Starship, clarify. Either way, current role in an advanced engineering/robotics environment is relevant context.]`

**Awards:** BrightSparks 2019 (Electronics Weekly / RS Components — UK's top young electronics engineers); The Manufacturer Top 100 (2015); International Space Apps Challenge winner (NASA, 2014).

**Memberships:** IET Member (2013–present); Certified LabVIEW Developer (National Instruments).

---

**Team Summary**

The founding team covers all core competencies for this venture:

| Competency | Coverage |
|---|---|
| Electric propulsion hardware (arcjet, HET) | Tiziano |
| Plasma diagnostics & test infrastructure | Tiziano |
| Power electronics & PPU design | Max (Safran GCU, IEEE-published, ESA) |
| High-power load modelling & hardware verification | Max (Safran — A380 GCU test cell) |
| Embedded systems & AI/ML implementation | Max |
| Space agency processes & standards | Max (ESA YGT) |
| Space instrument systems | Max (Thales Alenia) |
| Business development & MBA | Tiziano (Aalto) |
| Startup operations & company formation | Max (TEO Robotics, nCode) |

**Identified gaps and how we will address them:**
- *Business development / sales:* Tiziano's Aalto MBA and ABB commercial experience covers early-stage BD. We plan to add a business development hire in Year 2.
- *Plasma physics simulation specialist:* We will engage the University of Tartu (Tartu Observatory) and TalTech through the ESA BIC network for simulation support during incubation.
- `[TODO: any advisors, mentors, or supporters to list here? ESA contacts, VC relationships, potential customers who have expressed interest?]`

---

### 1.2 The Company

ẍ (xdoubledot) is not yet incorporated. The founders are based in Tallinn, Estonia and will incorporate a new Estonian OÜ (osaühing — private limited company) prior to signing an incubation contract with ESA BIC Estonia. The legal entity name will be **X Double Dot OÜ** (the typographic ẍ character is not permitted in Estonian Business Register names; "X Double Dot" is the equivalent registered name). `[TODO: confirm name availability with Estonian Business Register — ariregister.rik.ee — before submission. Alternative: "Xdoubledot OÜ"]`

Proposed shareholding: `[TODO: confirm split — e.g. 50/50 Max Simmonds / Tiziano Fiore]`. Both founders are EU residents based in Tallinn.

**Motivation for founding:** Both founders identified the same gap independently — the European space industry is entering an era of mega-constellations and VLEO operations that existing propulsion hardware is not designed for. With collective insider experience at the two largest European HET manufacturers, and direct knowledge of the cathode erosion problem and its cost implications, we are uniquely positioned to build the solution.

**Location:** Tallinn, Estonia. We intend to operate from Tehnopol Science and Business Park, where Max already has an active relationship through nCode OÜ.

**Founders' employment during incubation:** Both founders currently hold full-time positions — Max at Starship Technologies and Tiziano at ABB. During incubation, both will continue in their roles while allocating dedicated time to ẍ development, with the intent to transition full-time as funding milestones are reached. This is a realistic model for an early-stage deep-tech venture and means the team is not financially dependent on the ESA incentive for personal income. Both founders' current roles also provide direct technical relevance: Max at Starship Technologies (advanced propulsion systems context) and Tiziano at ABB (power systems and industrial engineering). `[TODO: specify expected hours per week committed to ẍ during incubation — reviewers will ask. Suggest 20hrs/week each as a minimum credible commitment]`

**Most significant developments planned during incubation:**
- Proof-of-concept plasma discharge demonstration with magnetic field shielding geometry
- First independent validation of AI-optimised B-field configurations (simulation + bench test)
- Patent filing on core magnetic shielding architecture
- First commercial conversations with European satellite OEMs and constellation operators
- `[TODO: any existing LOIs, MoUs, or warm commercial contacts to add?]`

---

## 2. Value Proposition

Satellite operators building constellations for VLEO (below 300 km altitude) face two compounding problems: atmospheric drag requires near-continuous thrust to maintain orbit, and the Hall thrusters that can provide this thrust wear out too quickly and cost too much to run on Xenon propellant.

**ẍ solves both problems:**

1. **Cathode life:** By dynamically shaping the magnetic field around the cathode using AI-optimised coil geometry, we divert erosive ion bombardment away from the cathode surface. Target: 5–10x extension of operational life (50,000+ hours vs. the industry-standard 10,000–15,000 hours), reducing the need for redundant hardware and enabling missions previously considered uneconomical.

2. **Propellant cost:** Our thruster architecture is optimised for Krypton, which costs approximately 3–5x less than Xenon per kilogram and is available through a more resilient European supply chain. Combined with improved efficiency from AI-optimised operating parameters, we target a 10x reduction in total propellant lifecycle cost versus Xenon-based incumbents.

**Unique selling proposition:** No existing European propulsion company combines AI-native control, dynamic magnetic shielding for erosion management, and propellant flexibility in a single platform. Incumbents (Safran, Exotrail) use static magnetic field configurations and accept erosion as a maintenance problem rather than a design problem.

**Example application:** A 70 kg VLEO imaging satellite at 250 km altitude requires approximately 2–3 mN of continuous thrust for drag compensation (moderate solar activity), rising to 20+ mN at solar maximum. No existing European Hall thruster is qualified for this continuous-firing duty cycle at sub-300W power. An ẍ 200W thruster with AI-optimised magnetic shielding, rated for >8,000 hours continuous Kr operation, enables a 5-year VLEO imaging mission without orbit-raising gaps or hardware redundancy.

---

## 3. Product / Service Description

### 3.1 The Space Connection

ẍ is developing hardware and software for direct use in the space sector. The space connection is intrinsic — this is not a downstream or technology transfer application; we are building propulsion hardware for deployment in orbit.

Specifically:
- **Space hardware (upstream):** Hall Effect Thruster units for satellite electric propulsion
- **Space software (upstream):** AI control system for real-time plasma state estimation, magnetic field optimisation, and autonomous orbit management
- **Technology development:** Novel dynamic magnetic shielding architecture, AI-optimised for VLEO drag compensation and extended cathode life

This represents a direct spin-in of advanced control systems technology into the space propulsion sector — combining academic plasma physics with modern embedded AI, power electronics expertise, and lessons learned from operating inside the incumbent supply chain.

---

### 3.2 The Technology

**Background — Hall Effect Thrusters**

A Hall Effect Thruster ionises a propellant gas (typically Xenon or Krypton) using a magnetic-field-trapped electron cloud, then accelerates the resulting ions electrostatically to generate thrust. Exhaust velocities of 15,000–25,000 m/s give specific impulses of 1,500–2,500 s — far higher than chemical propulsion — making HETs the propulsion of choice for long-duration, orbit-maintenance missions.

The core components are: discharge channel (ceramic annulus), anode (propellant distributor, high voltage), magnetic circuit (iron core + electromagnetic coils), hollow cathode (external electron source), and Power Processing Unit (PPU).

**The Cathode Erosion Problem**

The hollow cathode is the single-point failure mode of the modern HET. High-energy ions, accelerated in the discharge plume, are partially redirected back toward the cathode by the magnetic field topology and bombard its surface. Over time, this erodes the cathode emitter material (typically barium oxide on a tungsten matrix), changing its geometry, increasing plasma instabilities, and eventually causing thruster failure.

Current mitigation strategies are passive: use of more erosion-resistant materials, geometric optimisation, and redundant cathode designs. These extend life incrementally but do not solve the fundamental problem.

**The ẍ Approach: Dynamic Magnetic Shielding**

Our approach treats cathode erosion as a control problem rather than a materials problem. By modifying the magnetic field topology in real time — adjusting currents in independently controllable electromagnetic coil arrays — we can shape the plasma sheath boundary and ion trajectory distribution to minimise ion flux at the cathode surface.

The key enabler is an AI control system (neural network + reinforcement learning) that:
1. Estimates plasma state (density, temperature, ion energy distribution) from indirect sensor measurements (discharge current, voltage, optical emission)
2. Predicts the effect of coil current adjustments on cathode ion flux
3. Continuously optimises field geometry to minimise erosion while maintaining target thrust

This is distinct from magnetic shielding techniques used by NASA/JPL (Hofer et al., 2012) on the NSTAR/NEXT thrusters, which use a fixed optimised geometry. Our approach is dynamic and adaptive, enabling continuous re-optimisation as operating conditions change over mission life.

**Technology Roadmap**

| Phase | Timeline | Milestone | TRL |
|---|---|---|---|
| Phase 1 | Now → End of incubation (2028) | Laboratory plasma discharge validation; Kr propellant characterisation; magnetic field geometry modelling & bench test; AI controller proof-of-concept (software-in-loop) | 2–3 → 4–5 |
| Phase 2 | 2028–2029 | Full PPU integration; engineering model (200W nominal, 100–300W throttle range); first customer qualification testing | 5–6 |
| Phase 3 | 2029+ | In-orbit demonstration (IOD); VLEO drag compensation validation at 220–300km; 500W variant development for standard LEO constellation market | 6–7+ |

---

### 3.3 Readiness Level

**Current TRL: 2–3**

The concept is scientifically grounded and technically validated at the level of literature and first-principles analysis. Tiziano has designed and tested a functioning arcjet thruster (different technology, but directly relevant plasma diagnostic skills and test infrastructure experience). The AI magnetic field optimisation approach is designed but not yet implemented in hardware.

**Target TRL at end of incubation: 4–5**

By end of incubation we expect to have:
- A functioning laboratory plasma discharge demonstrating stable HET operation with our magnetic circuit geometry
- A validated simulation model (COMSOL/FEMM) of the magnetic field topology, correlated with bench measurements
- A software-in-the-loop AI controller prototype, validated against simulation
- Initial Krypton propellant flow and ionisation characterisation

This is an honest and achievable target for a 24-month, €60K funded programme. The deliverable is not a flight-ready thruster — it is the validated core technology that de-risks the larger development programme for Series A funding.

---

### 3.4 R&D Strategy

**Key technical challenges:**

1. *Plasma discharge stability with dynamic B-field:* Changing magnetic field geometry during operation risks inducing plasma oscillations (breathing mode instabilities). We will characterise the stability envelope experimentally and define safe operating limits for the AI controller.

2. *AI training data scarcity:* No existing dataset maps dynamic B-field configurations to plasma state outcomes for our specific geometry. We will generate synthetic training data via physics-informed simulation (COMSOL particle tracking + fluid models), validated against bench measurements at key operating points.

3. *PPU design for variable impedance:* Plasma load impedance varies significantly with operating point. Max's IEEE-published work on discrete-time modelling of switch-mode converters provides the methodological foundation for the adaptive PPU control loops needed.

4. *Krypton propellant characterisation:* Krypton has higher ionisation energy than Xenon (14.0 eV vs 12.1 eV), requiring higher electron temperatures and adjusted magnetic field topology for optimal ionisation efficiency. We will characterise this experimentally and use the results to train the AI controller.

**R&D approach:**
- Hardware: in-house (Tiziano, bench test facility to be established at Tehnopol)
- Simulation: combination of in-house (FEMM, open-source) and university lab access (TalTech, University of Tartu — available through ESA BIC network)
- AI development: in-house (Max)
- External procurement: vacuum chamber access (Tartu Observatory or TalTech), specialist plasma diagnostics `[TODO: confirm availability and cost with Sven/ESA BIC team]`

---

### 3.5 Intellectual Property

No patents are currently held. The founding technology — Tiziano's 200W HET design — is currently at TRL 2–3. `[TODO CRITICAL: Establish IP ownership of Tiz's existing design before submission. Was it developed at university (university may own it), independently (Tiz owns it), or during employment (ABB or other employer may have a claim)? Get a one-page IP clearance memo from a patent/IP attorney before filing the application. Budget €1–2K. If ownership is not clean, the ESA BIC contract cannot proceed.]`

Our IP strategy during incubation:

1. **Priority filing:** File a provisional patent application on the core dynamic magnetic shielding architecture and AI control method during the first year of incubation. Budget for IP protection is included in the ESA incentive allocation.
2. **Trade secrets:** Specific AI training methodology and plasma state estimation algorithms will be protected as trade secrets where patent coverage is impractical.
3. **Freedom to operate:** We have reviewed the Hofer et al. (NASA/JPL, 2012) magnetic shielding patents and the relevant Safran/Exotrail patent landscape. Our dynamic, AI-driven approach is distinct from existing filed IP. `[TODO: formal FTO analysis recommended before filing — budget ~€5K with a patent attorney]`
4. **Ownership:** All IP developed during incubation will be owned by ẍ OÜ.

---

## 4. Market Analysis

### 4.1 Context

The satellite industry is undergoing a structural transformation. The era of a few hundred large, expensive GEO satellites is giving way to thousands of small LEO satellites operating in coordinated constellations. This shift is driven by demand for global broadband connectivity, high-revisit Earth observation, and low-latency communications.

Key macro trends affecting ẍ:

- **VLEO opportunity:** Very Low Earth Orbit (180–300 km) offers 10x better imaging resolution and 5x lower communications latency than standard LEO (~550 km), but atmospheric drag at these altitudes is 100–1,000x higher, requiring near-continuous propulsion to maintain orbit. This creates strong demand for efficient, long-life electric propulsion.
- **European strategic autonomy:** Post-2022, European institutions have dramatically accelerated investment in sovereign space infrastructure. The IRIS2 constellation (EU's answer to Starlink — 290 satellites, €11B programme) specifically requires European propulsion solutions that are free of ITAR restrictions.
- **Xenon supply risk:** Xenon is a byproduct of industrial oxygen production. European supply is concentrated and price-volatile. Krypton is 3–5x cheaper and more widely available — operators are actively seeking Krypton-compatible thrusters.
- **Regulatory environment:** ESA's Clean Space initiative and EU Space Law (under development) are pushing satellite operators toward end-of-life deorbiting obligations — increasing demand for capable, long-life propulsion systems.

### 4.2 Market Size

| Market | Value | Source |
|---|---|---|
| EU Space Propulsion Market (2030) | €15.6B | Mordor Intelligence, 2025 |
| Global Electric Propulsion Systems Market (2031) | $17B | Mordor Intelligence, 2025 |
| Hall Thruster Market specifically (2032) | ~$3.8B | DataIntelo, 2025 |
| LEO Satellite Market (2035) | $66B | Roots Analysis, 2025 |
| Planned LEO satellites (2025–2030) | 50,000+ | Multiple sources |

**TAM (Total Addressable Market):** Global electric propulsion systems market, $17B by 2031 (Mordor Intelligence). Hall thruster segment specifically: ~$3.8B by 2032 (DataIntelo).

**SAM (Serviceable Addressable Market):** European market for Hall thrusters and associated software, €15.6B by 2030, specifically:
- IRIS2 and EU institutional satellites
- European commercial constellation operators (Eutelsat OneWeb, etc.)
- International operators seeking ITAR-free European supply chain

**SOM (Serviceable Obtainable Market):** 5% of European market by 2030 = ~€780M. In near-term practical terms (2028–2030): 10–20 engineering model and early production units at €100K–€300K per unit = €1M–€6M initial revenue. `[TODO: refine with bottom-up model — specific constellation programmes, unit volumes, pricing]`

### 4.3 Customer Segments

**Priority Segment 1: VLEO Earth observation operators (primary)**
Operators building small imaging constellations at 220–300km altitude, using 50–120kg satellites. This segment has the highest urgency for cathode life extension — continuous drag compensation at VLEO requires >8,000 hours rated life, which no current European HET provides. No ITAR restrictions, no Safran or Exotrail product qualified for this duty cycle. Estimated per-customer deal: 5–20 thrusters at €60K–€120K each.

**Priority Segment 2: EU institutional programmes (IRIS2 and defence)**
The EU's IRIS2 sovereign connectivity constellation (290 satellites, €11B programme) requires a European, ITAR-free propulsion supply chain. Defence smallsat operators (NATO, EU sovereign surveillance constellations) increasingly require domestic supply. As an Estonian-incorporated, ESA BIC-backed company, ẍ is positioned to qualify. Timeline aligns — IRIS2 procurement extends through the late 2020s.

**Priority Segment 3: Standard LEO constellation operators (Phase 2)**
For the standard 400–600km LEO market (OneWeb-scale, 150–300kg satellites), ẍ's Phase 2 500W variant competes directly with Safran EPS-X00 and Exotrail Mini on price and European supply chain. Lower urgency for our Phase 1 product but the larger long-term revenue opportunity.

`[TODO: identify 2–3 specific named prospects in each segment — even informal conversations count. A named potential customer is far stronger than market analysis.]`

### 4.4 Competition

| Competitor | Strength | Weakness | ẍ differentiation |
|---|---|---|---|
| **Safran** (PPS-series) | Market leader, flight heritage, 1,000+ units | Xenon-only, no AI, no dynamic shielding, high price (€300K+), long lead times | AI-native, Krypton/Argon capable, 10x lower cost target, 5x longer life |
| **Exotrail** (ExoMG) | Software-forward, Krypton capable, startup agility | No VLEO optimisation, no dynamic shielding, no AI-native control | VLEO-optimised, magnetic shielding, AI-integrated platform |
| **Thales Alenia** | Deep institutional relationships, IRIS2 position | System integrator, not a thruster innovator — likely a customer/partner | Complementary, not direct competition |
| **ArianeGroup** | Chemical propulsion heritage, launcher relationships | Limited EP portfolio, chemical-centric, slow to adapt | Not a meaningful HET competitor |
| **US incumbents** (Aerojet, Busek) | Deep flight heritage, NASA relationships | ITAR-restricted — blocked from European institutional programmes | ITAR-free advantage |

**Competitive window:** No company in Europe is currently developing AI-native, dynamically shielded HETs with Krypton optimisation for VLEO. This window is approximately 3–5 years before incumbents or well-funded startups could replicate the approach. Speed of IP filing and first-mover customer relationships are critical.

---

## 5. Business Model

### 5.1 Revenue Streams

**Stream 1: Thruster Unit Sales (primary)**
Direct sale of ẍ HET units to satellite OEMs and constellation operators. Pricing:
- Phase 1 VLEO product (100–300W, nominal 200W): **€50K–€100K per unit**
- Phase 2 standard LEO product (300–600W): **€80K–€150K per unit**

Reference: Busek BHT-350 industry estimates $80K–$250K depending on volume. Safran EPS-X00 expected to price above €150K (legacy pricing culture). ẍ targets below-market pricing enabled by Estonian manufacturing economics and a clean-sheet design.

Gross margin target: 55–65% at scale (hardware margins typical for space-grade components).

**Stream 2: Full Propulsion Subsystem Integration**
Turnkey delivery including PPU, propellant feed system, structural mounting, and software. Premium pricing; simplifies procurement for satellite integrators.
`[TODO: estimate premium over unit price — likely 1.5–2x multiplier]`

**Stream 3: AI Orbit Control Software (SaaS)**
Recurring licence for the AI-driven drag compensation, station-keeping, and predictive maintenance software layer. Delivers ongoing revenue and deepens customer lock-in.
Pricing model: `[TODO — per-satellite per-year licence, e.g. €5K–€20K/year/satellite. Constellation deals potentially €500K+/year for 50+ satellites]`

### 5.2 Pricing Rationale

Current market price for a comparable Safran PPS-series thruster: €250K–€350K. Our target unit price of €100K–€200K for the standard variant represents a 30–50% cost reduction while offering significantly better lifetime and propellant flexibility. We believe this price point is achievable through:
- Lean design-for-manufacture from first principles (no legacy architecture constraints)
- Krypton propellant system (simpler, cheaper than Xenon handling)
- Manufacturing in Estonia (lower labour cost than France/Italy)

### 5.3 Go-to-Market

Phase 1 (During incubation): Technical credibility-building. Publish results, present at IAC and IEPC conferences, engage ESA's Technology Transfer Programme, establish relationships with 5–10 target customers.

Phase 2 (Post-incubation, 2028–2029): Qualification testing with 1–2 anchor customers; first commercial contract for engineering model delivery.

Phase 3 (2029+): Production scale-up; target Series A funding (~€5M) to fund manufacturing capacity and first IOD.

---

## 6. Financial Projections

`[TODO: This section needs a proper financial model. Suggested structure below — fill in with Tiz.]`

### 6.1 Cost Structure During Incubation (24 months)

| Cost Category | Estimated Amount | Source |
|---|---|---|
| Vacuum chamber / lab access (University, Tartu Observatory) | €8,000–€12,000 | External |
| Magnetic circuit components (coils, iron, power supplies) | €10,000–€15,000 | External |
| Propellant feed system (Krypton MFC, valves, fittings) | €5,000–€8,000 | External |
| Electronics / PPU prototype | €6,000–€10,000 | External |
| Patent filing (provisional + PCT) | €8,000–€12,000 | External (attorney) |
| Plasma diagnostics (Langmuir probes, RPA) | €3,000–€5,000 | External / in-house |
| Miscellaneous / contingency (10%) | €5,000 | — |
| **Total external spend** | **~€45,000–€62,000** | — |

This aligns with the €60,000 ESA incentive. Salaries are not covered by the incentive; founders will self-fund through consulting income or co-investment during the incubation period.

`[TODO: confirm whether any salary support is available through Estonian sources — EBIA/KredEx loan facility]`

### 6.2 Revenue Projections (3-Year Outlook)

| Year | Revenue | Source |
|---|---|---|
| 2026 (incubation) | €0 | R&D phase only |
| 2027 (incubation) | €0–€50K | Possible research contract / grant |
| 2028 (post-incubation) | €100K–€300K | 1–2 engineering model deliveries |
| 2029 | €500K–€1.5M | First production units, SaaS revenue beginning |
| 2030 | €2M–€5M | Scale phase, Series A deployment |

`[TODO: build bottom-up model — identify specific programmes and units, not just top-down fractions. Attach P&L table using BIC-0006 Excel template]`

### 6.3 Funding Plan

| Source | Amount | Timing |
|---|---|---|
| ESA BIC incentive | €60,000 | On contract signing |
| EBIA/KredEx loan (optional) | Up to €50,000 | During incubation |
| Founders' own investment | `[TODO]` | Ongoing |
| Estonian R&D grant (EAS, Horizon Europe) | `[TODO — explore]` | 2027 |
| Series A | ~€5M target | 2028–2029 |

---

## 7. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Plasma discharge stability with dynamic B-field — oscillations make AI control impractical | Medium | High | Extensive simulation before hardware; characterise stability envelope early; fixed-geometry fallback option |
| AI training data insufficient for reliable plasma state estimation | Medium | Medium | Physics-informed synthetic data generation; partner with university plasma physics groups |
| Krypton supply disruption or price increase | Low | Medium | Design for propellant flexibility; Argon as secondary option; long-term supply agreements |
| Patent landscape — freedom to operate issue with NASA magnetic shielding IP | Low | High | Commission FTO analysis in Month 1; design around known claims; our dynamic approach is substantively different from Hofer 2012 static geometry |
| Incumbent response — Safran or Exotrail accelerate AI integration | Medium | Medium | Speed of IP filing; first-mover customer relationships; unique VLEO focus narrows the overlap |
| Vacuum test facility access delayed | Medium | Medium | Two options (TalTech, Tartu Observatory); confirm and contract access before incubation start |
| Founders' bandwidth — Max's nCode OÜ transition incomplete | Medium | Medium | Formal handover timeline committed before incubation contract signing |
| Insufficient capital post-incubation to reach Series A readiness | Medium | High | Pursue EAS/Horizon Europe grants in parallel; target 1 paying LOI customer during incubation to de-risk investor case |
| Regulatory / export control complications | Low | Medium | Estonian incorporation + ITAR-free design policy from day one; ESA BIC legal support |

---

## 8. SWOT Analysis

| Strengths | Weaknesses |
|---|---|
| Insider knowledge of incumbent (Max at Safran, Thales) | TRL 2–3 — significant technical work remains |
| ESA YGT background — credibility with ESA/institutional customers | No flight heritage |
| Tiziano's hands-on HET/plasma test experience | Small team — bandwidth constrained |
| ITAR-free, fully European supply chain | No existing customer relationships (yet) |
| Already at Tehnopol (ESA BIC partner) | Self-funded during incubation |
| IEEE-published power electronics (PPU core competency) | |

| Opportunities | Threats |
|---|---|
| IRIS2 — EU sovereign constellation mandating European propulsion | Safran could accelerate AI integration and leverage existing customer relationships |
| VLEO boom — market does not yet have a viable long-life thruster | Exotrail better funded and earlier stage than ẍ currently |
| Krypton demand — all major constellation operators seeking Xe alternatives | Funding gap between incubation end and Series A |
| ESA BIC network — direct access to ESA expertise, data, and contacts | Long sales cycles in space industry — revenue takes time |
| Estonian startup ecosystem — Tehnopol, EAS, EBIA | |

---

## Appendices

- **Annex A:** CVs of Tiziano Fiore and Max Simmonds `[TODO: prepare formal 2-page CVs]`
- **Annex B:** Company registration extract (once ẍ OÜ is incorporated) `[TODO]`
- **Annex C:** IEEE publication — *"Discrete-time modelling of pulse-width modulated DC-DC converters"*, IEEE COMPEL 2018
- **Annex D:** Letters of support / letters of intent `[TODO — even an informal email from a potential customer is worth including]`
- **Annex E:** Key references
  - Hofer, R. et al., *"Magnetically Shielded Hall Thruster"*, NASA/JPL, 2012
  - Mikellides, I. et al., *"Magnetic Shielding of Walls from the Unmagnetized Ion Beam"*, Journal of Applied Physics, 2014
  - Mordor Intelligence, *"Europe Space Propulsion Market Size & Growth to 2030"*, Jan 2025
  - Goldman Sachs, *"The global satellite market is forecast to become seven times bigger"*, Mar 2025

---

*End of draft — v0.1*

*Next: review with Tiz, resolve all TODOs, build P&L table (BIC-0006 Excel), then draft Incubation Proposal (BIC-0005) separately.*
