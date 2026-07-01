# Start here — PocketForge test-node board (for the PCB designer)

Welcome Ian. This repo holds the KiCad sources for **one open-hardware board** — a per-device automated
test fixture that replaces the battery in a handheld game console and gives a host full remote control of
it (programmable "virtual battery" voltage, hands-free microSD swap, power-button press, 12 V light-strip,
and USB-boot recovery). One PCB, one SKU, meant to run **24/7 for years** across a ~40-node fleet, so
protection + thermal reliability are first-class. Target: **~2-layer, ~60 × 90 mm, JLCPCB-assembled.**

## What to read, in order
1. **`01-design-brief.md`** — the complete spec: power tree, the LTC3649 virtual-battery buck, the ESP32-S3
   node + GPIO map, the integrated microSD mux, the 12 V LED switch, the power-button PhotoMOS, the FEL
   strap, and all connectors. **This is the master reference.**
2. **`02-netlist-wiring-guide.md`** — every net → pin (the connectivity source-of-truth for the schematic).
3. **`03-BOM.md`** — the parts + MPNs. The buck is decided (**LTC3649**); the protection/aux MPNs are being
   finalized (see the note in that file).
4. **`04-grounding-and-sense-reference.md`** — ⚠ **LAYOUT-CRITICAL.** Read before you route the analog
   section (star ground, Kelvin sense, SD-mux SI). This is the #1 thing that decides whether the board works.
5. **`05-abs-max-and-safety-spice.md`** — the safety envelope (PMIC BAT abs-max ~7 V; the OVP crowbar +
   TVS + fuse coordination; the SPICE fault analysis behind the protection values).

## Starting point in `kicad/`
- **`test-node-placement-template.kicad_sch`** — a KiCad 9 schematic with the ~25 core parts already placed
  in functional groups with the power rails (GND/+12V) pre-attached as power symbols. **The signal wiring
  is intentionally left for you to draw** (from `02-netlist-wiring-guide.md`). It's a head start on
  placement, not a finished schematic — treat it as a scaffold; move/replace freely.
- Symbols/footprints for the specialized parts (LTC3649, the SD-mux chips, ESP32-S3, etc.) are being
  collected under **`lib/`** (see `lib/README.md`) so you're not hunting parts.

## Workflow / conventions
- **KiCad 9** (9.0.9 is what's here). Hand-draw the schematic in eeschema; commit the `.kicad_sch` /
  `.kicad_pcb` as the source of truth. Use **labels only for power/global/cross-sheet nets; draw wires for
  local analog topology** (a net-label-everything schematic is hard to review).
- One editor at a time on a given `.kicad_*` file (KiCad files don't text-merge cleanly — UUID churn).
- **Design rules:** JLCPCB 2-layer capabilities; we'll add a `.kicad_dru` + a JLCPCB stackup.
- **Do NOT order a PCB yet.** The order is gated on the Fri 2026-07-03 EE review + a bench-current
  measurement (it sizes the buck inductor/FET/thermals). Schematic + placement can proceed now; hold final
  layout of the analog section until the grounding-ref (doc 04) is applied and the bench current is known.
- Put the **OSHW gear logo** on the silk at layout (KiCad ships `Symbol:OSHW-Logo_*_SilkScreen`).

## The load-bearing gotchas (so you don't rediscover them the hard way)
- **Buck output setting:** the MCP4728 DAC drives the **LTC3649 ISET pin at unity gain (Vout = V(ISET))** —
  **no feedback divider.** Float MODE/SYNC for forced-continuous so it can sink. (This was chosen after a
  long part hunt; the "DAC into a feedback divider" approach amplifies noise ~5× and is rejected.)
- **The OVP crowbar (TL431→SCR→fuse) must be independent** of the buck/DAC reference.
- **SD-mux only works to ≤50 MHz** — series-terminate CLK/CMD/DAT, keep the flex short, force High-Speed.
- **No aluminium electrolytics** on stressed nodes; everything default-safe at power-on (buck off, LED off,
  normal boot, mux defined).

Questions on intent → the full design rationale lives in the PocketForge `mission-control` repo,
`.planning/infra/infra-201-test-node-battery-emulator-board.md` (§J power stage, §K connectors).
