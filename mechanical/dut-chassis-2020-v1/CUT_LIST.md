# PocketForge 2020 chassis cut list

- Join topology: `three_way_cap_flush_side_butt_B08C9Q2TGW_measured`
- External assembled envelope (W × D × H): 358.00 × 346.00 × 368.00 mm
- Clear internal envelope (W × D × H): 318.00 × 306.00 × 328.00 mm
- Stock: 1000.00 mm bars
- Conservative kerf allowance: 3.20 mm per finished piece
- Stock bars required: **6**
- Finished extrusion: 5228.00 mm
- Kerf allowance: 57.60 mm
- Remaining stock/offcuts: 714.40 mm

Finished lengths are measured aluminum cuts. The delivered three-way connector was physically checked: horizontal rails butt flush to adjacent faces of each vertical post, their top/bottom outer faces are flush with the connector-cap planes, and a 360.00 mm post with caps at both ends measures approximately 368 mm outside-to-outside. The assignment below is an exact bounded packing, not first-fit order; retain the listed kerf reserve, measure every stock stick, mark every finished cut before sawing, and witness one saw cut before batch cutting.

## Finished pieces

| Part | Qty | Length (mm) | Total (mm) | Purpose |
|---|---:|---:|---:|---|
| `outer_vertical_rail` | 4 | 360.00 | 1440.00 | connector stem; measured caps add 4 mm per end |
| `outer_width_rail` | 4 | 318.00 | 1272.00 | butts between vertical-post side faces |
| `outer_depth_rail` | 4 | 306.00 | 1224.00 | butts between vertical-post side faces |
| `fixture_gantry_upright_half` | 4 | 164.00 | 656.00 | two halves plus reinforced splice form each fixture upright |
| `fixture_gantry_crossbar` | 2 | 318.00 | 636.00 | two height-adjustable fixture crossbars |

## 1 m stock assignment

- Bar 1: outer_vertical_rail 360.00, outer_vertical_rail 360.00, fixture_gantry_upright_half 164.00; kerf-inclusive consumed 893.60 mm; remainder 106.40 mm
- Bar 2: outer_vertical_rail 360.00, outer_vertical_rail 360.00, fixture_gantry_upright_half 164.00; kerf-inclusive consumed 893.60 mm; remainder 106.40 mm
- Bar 3: fixture_gantry_crossbar 318.00, fixture_gantry_crossbar 318.00, outer_width_rail 318.00; kerf-inclusive consumed 963.60 mm; remainder 36.40 mm
- Bar 4: outer_width_rail 318.00, outer_width_rail 318.00, outer_width_rail 318.00; kerf-inclusive consumed 963.60 mm; remainder 36.40 mm
- Bar 5: outer_depth_rail 306.00, outer_depth_rail 306.00, outer_depth_rail 306.00; kerf-inclusive consumed 927.60 mm; remainder 72.40 mm
- Bar 6: outer_depth_rail 306.00, fixture_gantry_upright_half 164.00, fixture_gantry_upright_half 164.00; kerf-inclusive consumed 643.60 mm; remainder 356.40 mm
