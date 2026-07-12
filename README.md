# test-node-hw

Open-hardware KiCad sources for the **PocketForge per-device test-node board** (Track D, bead `tsp-bcx.12`).

One PCB, one SKU, one per device under test: an **ESP32-S3** node + an **LTC3649 programmable "virtual
battery"** (2.5–4.4 V, ~3 A, DAC-set) + an **integrated microSD mux** (hands-free host↔device SD swap) +
a **12 V LED-strip switch** + a **FEL/USB-boot strap** + the **standard
Micro-Fit / JST-GH / SD-flex** interface. It permanently replaces the battery in a handheld and gives a
host full remote control, running 24/7 for years across a ~40-node fleet. (Cold-device power-on is done
by cutting/restoring the emulated cell + the device VBUS — a VBUS low→high edge boots the SoC; there is
no power-button actuator, that design is permanently abandoned — `tsp-bcx.24`.)

Design intent: **2-layer, ~60 × 90 mm, JLCPCB-assembled, open hardware** (OSHW gear on the silk; repo goes
public at release).

## → PCB designer: start at [`docs/00-IAN-START-HERE.md`](docs/00-IAN-START-HERE.md)

## Layout
- `docs/` — the full design brief, net list, BOM, the **layout-critical grounding/sense reference**, and
  the safety envelope.
- `kicad/` — the KiCad 9 project. `test-node-placement-template.kicad_sch` is a placement head-start
  (parts placed, power rails attached, signal wiring to be drawn).
- `lib/` — symbols/footprints for the specialized parts.

## Status
Pre-fab. Schematic + placement in progress; **PCB order gated** on the Fri 2026-07-03 EE review + the
`tsp-bcx.9` bench current measurement. Full rationale: PocketForge `mission-control`
`.planning/infra/infra-201-test-node-battery-emulator-board.md`.

## License
TBD (open-hardware — recommend CERN-OHL-S/W or TAPR OHL; to be set before the repo goes public).
