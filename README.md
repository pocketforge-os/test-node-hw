# test-node-hw

Open-hardware mechanical sources for the **PocketForge per-device test-node fixtures** — the
3D-printable chassis, DUT cradles, and fixture plates that hold a handheld device under test at a
repeatable optical datum in front of a per-node camera + electronics harness. Each fixture supports
the BPI-per-DUT test-node topology (one node per device under test), running 24/7 across the lab
fleet.

> **Scope note (2026-07-23):** this repo now holds **mechanical CAD only**. The earlier custom
> test-node PCB effort (the `tsp-bcx.12` / infra-201 battery-emulator board — LTC3649 virtual
> battery, ESP32-S3, integrated SD mux) has been retired in favor of the DUT-based approach, so the
> KiCad project, part libraries, and electronics design docs were removed. They remain recoverable
> in git history if ever needed.

## Layout

- `mechanical/dut-chassis-2020-v1/` — the stackable 20 × 20 mm aluminum-extrusion **standard rack**
  around one test node (movable camera/electronics fixture + fixed rear DUT carrier on a shared
  optical axis).
- `mechanical/dut-cradle-v1/` — the parametric **DUT cradle** (camera-facing device carrier) that
  fixes a handheld at a repeatable optical datum without loading its controls or display. Supports
  the TrimUI Smart Pro and Smart Pro S.
- `mechanical/dut-fixture-v1/` — the parametric **DUT fixture plate** (electronics mounting tray)
  sized for a Prusa i3 MK3S, carrying the current harness.
- `scripts/` — OpenSCAD lint/CI helpers.

Each `mechanical/*` project carries its own README with print instructions, parameters, and a
`Makefile` to render STLs.

## Building

OpenSCAD renders and meshes are generated from source (`mechanical/**/*.stl` is gitignored); run the
per-project `Makefile`. CI lints every `.scad` and publishes rendered artifacts on PRs.

## License

TBD (open-hardware — recommend CERN-OHL-S/W or TAPR OHL).
