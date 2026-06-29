# KiCad with Claude — A Practical Workflow

---

## What this is

I've been using Claude Code to do hardware design — schematic review, component selection, LCSC part number population, design calculations — and over the course of building [SBS_hw](https://github.com/maxsimmonds1337/SBS_hw) (a custom BLDC motor controller for my [DIY Onewheel](../DIY_One_Wheel/) and [Robot Dog Butler](../robot_dog_butler/)) I built up a set of patterns that work really well.

This page documents that workflow and points to the [kicad-template-master](https://github.com/maxsimmonds1337/kicad-template-master) repo, which packages it all up for reuse on new boards.

---

## The Core Idea: CLAUDE.md

Claude Code automatically reads a file called `CLAUDE.md` from the root of any project it's opened in. That's the entry point for the whole workflow.

A `CLAUDE.md` for a hardware project contains:

- **What the board is**: platforms, motor, battery chemistry, max voltage, key ICs
- **The critical sizing case**: e.g. "14S Onewheel = 58.8V nominal — all component voltage ratings are sized for this"
- **File map**: where schematics, manufacturing docs, and design calcs live
- **Ground rules**: e.g. "always check `pgrep -fil kicad` before editing `.kicad_sch` files" (KiCad corrupts files if you edit them while it's open)
- **Current state**: what's done, what's blocked, what's pending
- **End-of-design checklist**: things that must be true before sending to fab

When a fresh Claude session opens, it reads this and is immediately oriented — it knows the board topology, voltage constraints, open issues, and house rules without you re-briefing it.

---

## LCSC Part Numbers

JLCPCB requires an LCSC `Cxxxxxx` property on every component for assembly quoting. Doing this by hand in KiCad is tedious. The workflow instead:

1. Build a UUID→LCSC dict (KiCad UUIDs are in the `.kicad_sch` text files)
2. Run `scripts/add_lcsc.py` — it patches each schematic in-place, skipping anything already populated
3. Commit the sheets

The script handles all 6 sheets of SBS_hw (136 components) in about 2 seconds.

For standard 0603 passives, JLCPCB "Basic Parts" have no per-component assembly fee. The `jlcpcb-basic-parts.md` file in the template has the C-numbers for the full standard value range — so you don't look them up every session.

---

## Manufacturing Folder Structure

Each non-trivial component gets its own folder:

```
manufacturing/
  parts/
    Infineon/
      IRFS4115TRLPBF/
        IRFS4115TRLPBF.md   ← thermal calcs, switching loss, snubber sizing
        IRFS4115TRLPBF.pdf  ← datasheet (linked in KiCad Datasheet property)
    Texas_Instruments/
      DRV8301DCAR/
        DRV8301DCAR.md
  motor_controller/
    ISSUES.md               ← board-level issue tracker (MC-001, MC-002, ...)
  BOM.md
```

The individual `.md` files are the working design documents. At the end of the design they're collated into a single `design_calcs.md` — but not before. Premature collation just creates a doc that immediately goes stale.

The two-tier issue tracking (component issues in `parts/`, board-level issues in `ISSUES.md`) keeps things findable: you don't wade through a 500-line issue list to find the decoupling cap calculation.

---

## The KiCad Library Submodule

The template includes a personal KiCad library (`design/Kicad_Library/`) as a git submodule. This means:

- Custom symbols and footprints are versioned independently
- All projects share the same library and get updates when you do `git submodule update --remote`
- The library can contain datasheets, 3D models, and application notes alongside the KiCad files

The trade-off: GitHub's "Use this template" button doesn't clone submodules. You have to use the mirror method instead (documented in the [template README](https://github.com/maxsimmonds1337/kicad-template-master)).

---

## Creating a New Project from the Template

GitHub's built-in template system silently drops the submodule, so use the mirror method:

```bash
# 1. Create a blank repo at github.com/new

# 2. Bare-clone the template
git clone --bare https://github.com/maxsimmonds1337/kicad-template-master.git TEMP

# 3. Mirror-push to your new repo
cd TEMP
git push --mirror https://github.com/maxsimmonds1337/YOURPROJECT.git

# 4. Clean up
cd ..
rm -rf TEMP

# 5. Clone your new project normally (--recurse-submodules gets the library)
git clone --recurse-submodules https://github.com/maxsimmonds1337/YOURPROJECT.git
```

Then:
- Rename the `TEOXXXX_boardname.*` files in `design/` to match your project
- Fill in the bracketed sections in `CLAUDE.md`
- Open the project in Claude Code — it'll read `CLAUDE.md` and be oriented immediately

---

## Stock Checking

Before BOM lock, check LCSC stock for every part. The `lcsc` and `bom` Claude skills can sweep the whole BOM automatically. The rule: any part with stock < 10× required quantity gets flagged, and an alternative C-number is documented in the component's `.md` file. LCSC stock drops fast on popular parts — stale stock numbers have caused problems.

---

## The Workflow in Practice

For SBS_hw (VESC 6 MK5 derivative, 14S BLDC driver, ~155 unique components):

- Session 1: schematic review vs VESC 6 MK5, flagged 15 issues including MOSFET voltage rating violation (40V part on a 58.8V bus)
- Session 2: replaced MOSFETs, bootstrap diodes, fixed footprints, wrote design calcs for all major ICs
- Session 3: bulk LCSC population (136 components in one script run), wrote this template

The `CLAUDE.md` at each session start meant no time spent re-orienting — the second session picked up the exact list of open issues from the first.

---

## Links

- [kicad-template-master](https://github.com/maxsimmonds1337/kicad-template-master) — the template repo
- [Kicad_Library](https://github.com/maxsimmonds1337/Kicad_Library) — the library submodule
- [SBS_hw](https://github.com/maxsimmonds1337/SBS_hw) — the project this workflow was developed on
