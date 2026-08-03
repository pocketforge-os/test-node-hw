# PocketForge 2020 chassis cut list — dual-bar variant

- Chassis variant: `dualbar_v1`
- Qualification: **physically_qualified** (`tsp-t1zd.2`; accepted 2026-08-03)
- Join topology: `three_way_cap_flush_side_butt_B08C9Q2TGW_measured_plus_two_adjustable_fixture_bars_printed_indexing_plates`
- External assembled envelope (W × D × H): 346.00 × 358.00 × 368.00 mm
- Clear internal envelope (W × D × H): 306.00 × 318.00 × 328.00 mm
- Stock: 1000.00 mm bars
- Conservative kerf allowance: 3.20 mm per finished piece
- Stock bars required with no reusable offcut: **5**
- Fresh stock required with one qualifying offcut: **5 bars**
- Fresh stock required with two qualifying offcuts: **4 bars**
- Finished extrusion: 4548.00 mm
- Finished-extrusion savings versus legacy gantry: 656.00 mm (12.61%)
- Fixture-support savings: 656.00 mm (51.74%)
- Kerf allowance: 44.80 mm
- Remaining stock/offcuts when starting from five full bars: 407.20 mm

Finished lengths are measured aluminum cuts. This candidate preserves the proven outer frame and uses two continuous fixture bars: one between the lower depth rails and one between the upper depth rails. The matched pair remains movable for camera-distance adjustment. Never splice either fixture bar.

## Scrap-first plan

Each 306.00 mm `fixture_support_bar` needs one straight, undamaged 2020 offcut measuring at least **309.20 mm**. Two qualifying offcuts supply the complete upper/lower pair and reduce fresh stock to the four tightly packed outer-frame sticks.

The known **356.40 mm** retained offcut qualifies for one fixture bar and leaves **47.20 mm**, but it cannot supply both bars. With only that one offcut, a fifth fresh stick is still required for the other fixture bar. Each outer-frame stick yields one 360 mm post, one 318 mm depth rail, and one 306 mm width rail: 993.60 mm kerf-inclusive consumed and 6.40 mm remaining.

## Fifth-stick and batch route

For one chassis, two fixture bars plus two kerfs consume **618.40 mm** of the fifth stick and leave a straight **381.60 mm** offcut. That remainder still qualifies for one future fixture bar; label and retain it.

For batch cutting, three 306.00 mm fixture bars plus three kerfs consume **927.60 mm** and leave **72.40 mm**. Use two now and label the third as the first bar of the next chassis. The known 356.40 mm offcut plus all three bars from one fresh stick supplies the four fixture bars needed by two chassis.

## Finished pieces

| Part | Qty | Length (mm) | Total (mm) | Purpose |
|---|---:|---:|---:|---|
| `outer_vertical_rail` | 4 | 360.00 | 1440.00 | connector stem; measured caps add 4 mm per end |
| `outer_width_rail` | 4 | 306.00 | 1224.00 | butts between vertical-post side faces |
| `outer_depth_rail` | 4 | 318.00 | 1272.00 | butts between vertical-post side faces |
| `fixture_support_bar` | 2 | 306.00 | 612.00 | matched upper/lower depth-adjustable fixture bars |

## 1 m stock assignment — no reusable offcut

- Bar 1: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 2: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 3: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 4: outer_vertical_rail 360.00, outer_depth_rail 318.00, outer_width_rail 306.00; kerf-inclusive consumed 993.60 mm; remainder 6.40 mm
- Bar 5: fixture_support_bar 306.00, fixture_support_bar 306.00; kerf-inclusive consumed 618.40 mm; remainder 381.60 mm

## Qualification boundary

`physically_qualified` records the completed `tsp-t1zd.2` physical gate for the exact locked dual-bar layout. The printed fit, fastener engagement, loaded plate stability, camera alignment, service access, and owner approval were accepted on 2026-08-03. Any geometry or topology change requires a new candidate layout and a fresh physical gate; do not edit this qualified layout in place.
