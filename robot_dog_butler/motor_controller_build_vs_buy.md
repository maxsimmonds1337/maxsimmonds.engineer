---
---

# Motor Controller: Build vs Buy

Comparison of VESC 6, ODrive v3.6, and moteus r4.11 — component costs from LCSC/Mouser, PCB+assembly from JLCPCB, vs buying finished boards. Delivery to Estonia, VAT 24%.

---

## TL;DR

| Board | DIY landed | Buy landed | Verdict |
|-------|-----------|------------|---------|
| **VESC 6** | ~$95–105 | ~$130–145 | **Build — save ~$35** |
| **ODrive v3.6** | ~$145–165 | ~$115–155 | **Buy clone** |
| **moteus r4.11** | ~$95–100 | ~$148–158 | **Build — save ~$55** |

---

## Shipping & VAT assumptions

| Route | Cost |
|-------|------|
| LCSC → Estonia (DHL Express) | ~$15–22 |
| JLCPCB → Estonia (DHL, PCBA parcel) | ~$20–30 |
| AliExpress/Makerbase → Estonia (DHL) | ~$18–25 |
| mjbots US → Estonia (DHL) | ~$25–35 |
| Estonia VAT (from Jul 2025) | **24%** |
| EU customs duty threshold | €150 (VAT still applies from €0) |

---

## 1. VESC 6

**Repo:** [vedderb/bldc-hardware](https://github.com/vedderb/bldc-hardware)  
**Board:** 4-layer, ~70×70mm, single motor

### Key components (LCSC, qty 10)

| Component | Part | LCSC # | Qty | @10 each | Line total |
|-----------|------|--------|-----|----------|------------|
| MCU | STM32F405RGT6 | [C15742](https://www.lcsc.com/product-detail/C15742.html) | 1 | $3.44 | $3.44 |
| Gate driver + shunt amp | DRV8301DCAR | [C98969](https://www.lcsc.com/product-detail/C98969.html) | 1 | $2.86 | $2.86 |
| Power FETs 60V 240A | IRFS7530TRL7PP | [C445669](https://www.lcsc.com/product-detail/C445669.html) | 6 | $1.54 | $9.24 |
| CAN transceiver | SN65HVD232DR | [C30530](https://www.lcsc.com/product-detail/C30530.html) | 1 | $0.66 | $0.66 |
| Bulk caps 120µF 50V | EEH-ZC1H121P | Mouser | 4 | $1.20 | $4.80 |
| Current shunt 2mΩ | Various | LCSC | 2 | $0.08 | $0.16 |
| Crystal 8MHz | ABM3B-8.000MHz | LCSC | 1 | $0.25 | $0.25 |
| Passives (caps, Rs, inductors) | Various | LCSC | ~60 | — | ~$4.00 |
| Connectors | Various | LCSC | ~10 | — | ~$3.00 |
| **Component total** | | | | | **~$28–32** |

### JLCPCB (5-board run, per board share)

| Item | Cost |
|------|------|
| 4-layer PCB 70×70mm × 5 | ~$20 |
| PCBA setup + stencil | ~$10 |
| Assembly (~350 joints) | ~$1 |
| Extended part fees (~8 types × $1.50) | ~$12 |
| **Total / 5 boards → per board** | **~$9** |

### DIY total (1 board)

| Item | Cost |
|------|------|
| Components | ~$30 |
| PCB + assembly share | ~$9 |
| LCSC shipping | ~$18 |
| JLCPCB shipping | ~$25 |
| VAT 24% on ~$50 goods | ~$12 |
| **Total landed** | **~$95–105** |

### Buy price

| Source | Board price | Ship | VAT | Landed |
|--------|------------|------|-----|--------|
| [Makerbase VESC Mini 6.7](https://www.aliexpress.com/item/1005004275900738.html) | $92 | $20 | $27 | **~$139** |
| [Flipsky FSESC 6.7 Pro](https://flipsky.net) | $94 | $20 | $27 | **~$141** |

**Verdict: Build saves ~$35–40. All main ICs on LCSC and in JLCPCB library. Straightforward 4-layer design.**

---

## 2. ODrive v3.6

**Repo:** [odriverobotics/ODriveHardware](https://github.com/odriverobotics/ODriveHardware) (v3.4 public, v3.6 closed source — same architecture)  
**Board:** 4-layer, ~140×68mm, **dual motor**

### Key components (LCSC, qty 10)

| Component | Part | LCSC # | Qty | @10 each | Line total |
|-----------|------|--------|-----|----------|------------|
| MCU | STM32F405RGT6 | [C15742](https://www.lcsc.com/product-detail/C15742.html) | 1 | $3.44 | $3.44 |
| Gate driver (×2 channels) | DRV8301DCAR | [C98969](https://www.lcsc.com/product-detail/C98969.html) | 2 | $2.86 | $5.72 |
| Power FETs 30V 93A (×14/channel) | NTMFS5C628NLT1G | [C145537](https://www.lcsc.com/product-detail/C145537.html) | 28 | $0.47 | $13.16 |
| CAN transceiver | SN65HVD232D | [C1544356](https://www.lcsc.com/product-detail/C1544356.html) | 1 | $0.57 | $0.57 |
| Bulk caps 120µF 50V (×8) | EEH-ZC1H121P | Mouser | 8 | $1.20 | $9.60 |
| Current sense amp | AD8418WBRZ | **Mouser** ~$3.50 | 1 | $3.50 | $3.50 |
| Crystal 8MHz | ABM3B-8.000MHz | LCSC | 1 | $0.25 | $0.25 |
| Passives | Various | LCSC | ~70 | — | ~$5.00 |
| Connectors | Various | LCSC | ~15 | — | ~$4.00 |
| **Component total** | | | | | **~$47–55** |

> ⚠️ NTMFS4935NT1G (original ODrive FET) is out of stock on LCSC — NTMFS5C628NLT1G is the current in-stock alternative.  
> ⚠️ AD8418WBRZ not on LCSC — order from Mouser separately.

### JLCPCB (5-board run, per board share)

| Item | Cost |
|------|------|
| 4-layer PCB 140×68mm × 5 | ~$40 |
| PCBA setup + stencil | ~$10 |
| Assembly (~600 joints) | ~$1 |
| Extended part fees (~12 types × $1.50) | ~$18 |
| **Total / 5 boards → per board** | **~$14** |

### DIY total (1 board)

| Item | Cost |
|------|------|
| Components (LCSC + Mouser) | ~$52 |
| PCB + assembly share | ~$14 |
| LCSC shipping | ~$18 |
| Mouser shipping (separate order) | ~$15 |
| JLCPCB shipping | ~$28 |
| VAT 24% on ~$80 goods | ~$19 |
| **Total landed** | **~$145–165** |

### Buy price

| Source | Board price | Ship | VAT | Landed |
|--------|------------|------|-----|--------|
| [Makerbase ODrive 3.6 clone](https://www.aliexpress.com/item/1005002349959313.html) | $90 | $20 | $26 | **~$136** |
| Official ODrive v3.6 | $259 | — | — | **NRND / sold out** |

**Verdict: Buy the clone. Lands ~$136 vs ~$155 DIY. Three separate shipments (LCSC, Mouser, JLCPCB) and 28 FETs make this painful to build. Clone is basically the same board.**

---

## 3. moteus r4.11

**Repo:** [mjbots/moteus](https://github.com/mjbots/moteus) — hardware in `/hw/controller/r4.11/`  
**Board:** 4-layer, 46×53mm, single motor, **encoder on board**

### Key components (LCSC, qty 10)

| Component | Part | LCSC # | Qty | @10 each | Line total |
|-----------|------|--------|-----|----------|------------|
| MCU | STM32G474RET6 | [C521608](https://www.lcsc.com/product-detail/C521608.html) | 1 | $4.66 | $4.66 |
| Gate driver 3-phase smart | DRV8353RSRGZR | [C506246](https://www.lcsc.com/product-detail/C506246.html) | 1 | $4.18 | $4.18 |
| Power FETs (see note) | BSC016N06NS or equiv | LCSC | 6 | ~$1.00–1.80 | ~$7–11 |
| Magnetic encoder | AS5047P-ATSM | [C962063](https://www.lcsc.com/product-detail/C962063.html) | 1 | $3.25 | $3.25 |
| CAN-FD transceiver | TCAN1042VDRQ1 | [C485806](https://www.lcsc.com/product-detail/C485806.html) | 1 | $0.57 | $0.57 |
| Current shunt ~5mΩ | Various | LCSC | 2 | $0.20 | $0.40 |
| Bulk caps (polymer, 44V) | Various | LCSC | 4 | $0.50 | $2.00 |
| Passives | Various | LCSC | ~50 | — | ~$3.50 |
| Connectors (XT30PW, JST-PH3) | Various | LCSC | 4 | $0.60 | $2.40 |
| Diametric magnet 6mm | — | AliExpress | 1 | ~$0.50 | $0.50 |
| **Component total** | | | | | **~$24–30** |

> ⚠️ Exact MOSFET part number not in public BOM — open `hw/controller/r4.11/controller.brd` in Eagle to confirm. Likely Infineon BSC016N06NS or similar 60V 100A SO-8FL device.

### JLCPCB (5-board run, per board share)

| Item | Cost |
|------|------|
| 4-layer PCB 46×53mm × 5 | ~$18 |
| PCBA setup + stencil | ~$10 |
| Assembly (~280 joints) | ~$0.50 |
| Extended part fees (~10 types × $1.50) | ~$15 |
| **Total / 5 boards → per board** | **~$9** |

> Note: DRV8353RSRGZR is WQFN-40 0.5mm pitch — within JLCPCB capability but verify placement accuracy before ordering.

### DIY total (1 board)

| Item | Cost |
|------|------|
| Components | ~$28 |
| PCB + assembly share | ~$9 |
| LCSC shipping | ~$18 |
| JLCPCB shipping | ~$25 |
| VAT 24% on ~$50 goods | ~$12 |
| **Total landed** | **~$92–100** |

### Buy price

| Source | Board price | Ship | VAT | Landed |
|--------|------------|------|-----|--------|
| [mjbots.com r4.11](https://mjbots.com/products/moteus-r4-11) | $94 | $30 | $30 | **~$154** |

> Ships from USA — DHL to Estonia is $25–35. No cheap clone equivalent exists.

**Verdict: Build saves ~$55. Smallest board, cheapest fab, all ICs on LCSC. Biggest win if you can identify the MOSFET from the Eagle file.**

---

## LCSC part numbers — quick reference

| Part | LCSC # | @1 / @10 |
|------|--------|----------|
| STM32F405RGT6 | [C15742](https://www.lcsc.com/product-detail/C15742.html) | $3.97 / $3.44 |
| STM32G474RET6 | [C521608](https://www.lcsc.com/product-detail/C521608.html) | $5.39 / $4.66 |
| DRV8301DCAR | [C98969](https://www.lcsc.com/product-detail/C98969.html) | $3.35 / $2.86 |
| DRV8353RSRGZR | [C506246](https://www.lcsc.com/product-detail/C506246.html) | $4.82 / $4.18 |
| IRFS7530TRL7PP | [C445669](https://www.lcsc.com/product-detail/C445669.html) | $1.82 / $1.54 |
| NTMFS5C628NLT1G | [C145537](https://www.lcsc.com/product-detail/C145537.html) | $0.58 / $0.47 |
| AS5047P-ATSM | [C962063](https://www.lcsc.com/product-detail/C962063.html) | $3.68 / $3.25 |
| TCAN1042VDRQ1 | [C485806](https://www.lcsc.com/product-detail/C485806.html) | $0.71 / $0.57 |
| SN65HVD232DR | [C30530](https://www.lcsc.com/product-detail/C30530.html) | $0.78 / $0.66 |

**Not on LCSC — order from Mouser:**
- AD8418WBRZ (ODrive current sense amp) — ~$3.50
- EEH-ZC1H121P (120µF 50V Al-poly, ODrive bulk cap) — ~$1.20 @10

---

## Build risk notes

- JLCPCB minimum is 5 boards — you pay for 5 even if you need 1
- Extended parts fees (~$1.50/unique part type) add up fast — 10 extended types = $15 just in loading fees
- A first spin of a 4-layer power electronics board almost always needs at least one rework
- Debugging requires oscilloscope + current probe + safe motor test rig
- If you're building 5+ boards (robot has 12 joints), DIY savings multiply significantly

---

*Prices as of May 2026. LCSC/Mouser prices fluctuate with stock. VAT 24% is Estonia's standard rate from July 2025.*
