# PocketForge 2020 chassis cut list

- Join topology: `three_way_end_corners_B08C9Q2TGW`
- Stock: 1000.00 mm bars
- Conservative kerf allowance: 3.20 mm per finished piece
- Stock bars required: **8**
- Finished extrusion: 7200.00 mm
- Kerf allowance: 76.80 mm
- Remaining stock/offcuts: 723.20 mm

Do not batch-cut until one physical three-way connector dry-fit confirms the finished rail length. The stock assignment deliberately pairs two 360 mm pieces with one 180 mm gantry-upright half per bar; kerf therefore controls the guaranteed short-piece yield.

## Finished pieces

| Part | Qty | Length (mm) | Total (mm) | Purpose |
|---|---:|---:|---:|---|
| `outer_vertical_rail` | 4 | 360.00 | 1440.00 | between three-way end connectors |
| `outer_width_rail` | 4 | 360.00 | 1440.00 | between three-way end connectors |
| `outer_depth_rail` | 4 | 360.00 | 1440.00 | between three-way end connectors |
| `plate_gantry_upright_half` | 8 | 180.00 | 1440.00 | two offcut halves plus one clamshell form each upright |
| `plate_gantry_crossbar` | 4 | 360.00 | 1440.00 | two height-adjustable crossbars per plate gantry |

## 1 m stock assignment

- Bar 1: outer_depth_rail 360.00, outer_depth_rail 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 2: outer_depth_rail 360.00, outer_depth_rail 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 3: outer_vertical_rail 360.00, outer_vertical_rail 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 4: outer_vertical_rail 360.00, outer_vertical_rail 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 5: outer_width_rail 360.00, outer_width_rail 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 6: outer_width_rail 360.00, outer_width_rail 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 7: plate_gantry_crossbar 360.00, plate_gantry_crossbar 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
- Bar 8: plate_gantry_crossbar 360.00, plate_gantry_crossbar 360.00, plate_gantry_upright_half 180.00; kerf-inclusive consumed 909.60 mm; remainder 90.40 mm
