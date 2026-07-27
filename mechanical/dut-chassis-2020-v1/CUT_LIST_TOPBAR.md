# PocketForge 2020 chassis cut list — top-bar variant

- Chassis variant: `topbar_v1`
- Qualification: **candidate; physical print, fit, loaded-sag, and camera checks are still required**
- Join topology: `three_way_cap_flush_side_butt_B08C9Q2TGW_measured_plus_single_adjustable_topbar_B08D6T9CGN`
- External assembled envelope (W × D × H): 346.00 × 358.00 × 368.00 mm
- Clear internal envelope (W × D × H): 306.00 × 318.00 × 328.00 mm
- Stock: 1000.00 mm bars
- Conservative kerf allowance: 3.20 mm per finished piece
- Stock bars required with no reusable offcut: **5**
- Fresh stock required with the retained 356.40 mm offcut: **4 bars**
- Finished extrusion: 4242.00 mm
- Finished-extrusion savings versus legacy gantry: 962.00 mm (18.49%)
- Fixture-support savings: 962.00 mm (75.87%)
- Kerf allowance: 41.60 mm
- Remaining stock/offcuts when starting from five full bars: 716.40 mm

Finished lengths are measured aluminum cuts. This candidate preserves the proven outer frame and replaces the complete two-upright/two-crossbar fixture gantry with one continuous top bar. The bar remains movable on the upper depth rails. Never splice the top bar, and do not cut the legacy upright halves or second crossbar for this variant.

## Scrap-first plan

Cut the 306.00 mm `fixture_topbar` from any straight, undamaged 2020 offcut measuring at least **309.20 mm** before buying another stick. The retained **356.40 mm** offcut from the proven legacy six-stick assignment qualifies and leaves **47.20 mm** after one finished cut plus kerf.

With that offcut, buy only four fresh 1 m sticks. Each fresh stick yields one 360 mm post, one 318 mm depth rail, and one 306 mm width rail: 993.60 mm kerf-inclusive consumed and 6.40 mm remaining. If no qualifying offcut exists, the exact bounded assignment below proves that five full sticks suffice.

## Batch top-bar route

If the fifth stick must be new, cut **three** 306.00 mm top bars together rather than stranding its large single-build remainder. Three finished bars plus three kerfs consume 927.60 mm and leave **72.40 mm**. Use one now and label the other two for the next two chassis; each later chassis then needs only its four tightly packed outer-frame sticks.

## Finished pieces

| Part | Qty | Length (mm) | Total (mm) | Purpose |
|---|---:|---:|---:|---|
| `outer_vertical_rail` | 4 | 360.00 | 1440.00 | connector stem; measured caps add 4 mm per end |
| `outer_width_rail` | 4 | 306.00 | 1224.00 | butts between vertical-post side faces |
| `outer_depth_rail` | 4 | 318.00 | 1272.00 | butts between vertical-post side faces |
| `fixture_topbar` | 1 | 306.00 | 306.00 | single depth-adjustable fixture suspension bar |

## 1 m stock assignment — no reusable offcut

- Bar 1: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 2: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 3: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 4: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 5: fixture_topbar 306.00; kerf-inclusive consumed 309.20 mm; remainder 690.80 mm

## Qualification boundary

`candidate_requires_physical_qualification` is deliberate. These dimensions and print beds may be generated for a prototype, but this cut list does not make the topology production-qualified. Promote it only after the tracked physical acceptance gate records print fit, fastener engagement, loaded plate stability, camera alignment, and owner approval.
