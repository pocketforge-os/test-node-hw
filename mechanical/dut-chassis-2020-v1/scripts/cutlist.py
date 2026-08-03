#!/usr/bin/env python3
"""Convert OpenSCAD PFCUT echoes into deterministic cut-list artifacts."""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass, field
from pathlib import Path


ECHO_RE = re.compile(
    r'^ECHO:\s+"(?P<payload>PF(?:CUT|STOCK|FRAME|VARIANT)\|.*)"\s*$'
)

VARIANT_STATUS = {
    "legacy_gantry": "physically_proven_frozen_baseline",
    "dualbar_v1": "physically_qualified",
}
LEGACY_FINISHED_TOTAL_MM = 5204.0
LEGACY_FIXTURE_EXTRUSION_MM = 1268.0
FIXTURE_BAR_LENGTH_MM = 306.0
DUALBAR_FIXTURE_EXTRUSION_MM = 2 * FIXTURE_BAR_LENGTH_MM


@dataclass(frozen=True)
class Cut:
    name: str
    length: float
    note: str
    ordinal: int


@dataclass
class StockBar:
    number: int
    stock_length: float
    kerf: float
    cuts: list[Cut] = field(default_factory=list)

    @property
    def consumed(self) -> float:
        return sum(cut.length + self.kerf for cut in self.cuts)

    @property
    def remaining(self) -> float:
        return self.stock_length - self.consumed

    def fits(self, cut: Cut) -> bool:
        return self.consumed + cut.length + self.kerf <= self.stock_length + 1e-9


def parse_echoes(
    path: Path,
) -> tuple[
    list[tuple[str, int, float, str]],
    float,
    float,
    str,
    tuple[float, float, float],
    tuple[float, float, float],
    str,
    str,
]:
    rows: list[tuple[str, int, float, str]] = []
    stock_length = 0.0
    kerf = 0.0
    topology = ""
    frame_outer = (0.0, 0.0, 0.0)
    frame_clear = (0.0, 0.0, 0.0)
    variant = ""
    qualification_status = ""

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = ECHO_RE.match(raw_line.strip())
        if not match:
            continue
        fields = match.group("payload").split("|")
        if fields[0] == "PFCUT" and len(fields) == 5:
            rows.append((fields[1], int(fields[2]), float(fields[3]), fields[4]))
        elif fields[0] == "PFSTOCK" and len(fields) == 4:
            stock_length = float(fields[1])
            kerf = float(fields[2])
            topology = fields[3]
        elif fields[0] == "PFFRAME" and len(fields) == 7:
            frame_outer = tuple(float(value) for value in fields[1:4])
            frame_clear = tuple(float(value) for value in fields[4:7])
        elif fields[0] == "PFVARIANT" and len(fields) == 3:
            variant = fields[1]
            qualification_status = fields[2]

    if not rows:
        raise SystemExit(f"cutlist=fail reason=no_PFCUT_echoes input={path}")
    if stock_length <= 0 or kerf < 0 or not topology:
        raise SystemExit(f"cutlist=fail reason=invalid_PFSTOCK input={path}")
    if min(frame_outer) <= 0 or min(frame_clear) <= 0:
        raise SystemExit(f"cutlist=fail reason=invalid_PFFRAME input={path}")
    if variant not in VARIANT_STATUS:
        raise SystemExit(
            f"cutlist=fail reason=invalid_PFVARIANT variant={variant!r} input={path}"
        )
    if qualification_status != VARIANT_STATUS[variant]:
        raise SystemExit(
            "cutlist=fail reason=variant_status_mismatch "
            f"variant={variant} status={qualification_status!r} input={path}"
        )
    return (
        rows,
        stock_length,
        kerf,
        topology,
        frame_outer,
        frame_clear,
        variant,
        qualification_status,
    )


def _first_fit_decreasing(
    cuts: list[Cut], stock_length: float, kerf: float
) -> list[StockBar]:
    """Return a fast, deterministic upper bound for exact packing."""
    bars: list[StockBar] = []
    for cut in cuts:
        destination = next((bar for bar in bars if bar.fits(cut)), None)
        if destination is None:
            destination = StockBar(len(bars) + 1, stock_length, kerf)
            bars.append(destination)
        destination.cuts.append(cut)
    return bars


def _pack_into_count(
    cuts: list[Cut], stock_length: float, kerf: float, count: int
) -> list[StockBar] | None:
    """Find an exact packing into ``count`` bars with symmetry pruning."""
    bars = [StockBar(number + 1, stock_length, kerf) for number in range(count)]
    consumed = [0.0] * count
    item_sizes = [cut.length + kerf for cut in cuts]
    remaining_sizes = [0.0] * (len(cuts) + 1)
    for index in range(len(cuts) - 1, -1, -1):
        remaining_sizes[index] = remaining_sizes[index + 1] + item_sizes[index]

    failed_states: set[tuple[int, tuple[float, ...]]] = set()

    def search(index: int) -> bool:
        if index == len(cuts):
            return True
        remaining_capacity = sum(stock_length - value for value in consumed)
        if remaining_sizes[index] > remaining_capacity + 1e-9:
            return False

        canonical_fill = tuple(
            sorted((round(value, 6) for value in consumed), reverse=True)
        )
        state = (index, canonical_fill)
        if state in failed_states:
            return False

        cut = cuts[index]
        item_size = item_sizes[index]
        seen_consumed: set[float] = set()
        for bar_index in range(count):
            current = round(consumed[bar_index], 6)
            if current in seen_consumed:
                continue
            seen_consumed.add(current)
            if consumed[bar_index] + item_size > stock_length + 1e-9:
                continue

            bars[bar_index].cuts.append(cut)
            consumed[bar_index] += item_size
            if search(index + 1):
                return True
            consumed[bar_index] -= item_size
            bars[bar_index].cuts.pop()

            # Every empty bar is equivalent; trying a second one only repeats
            # the same state under another stock-bar number.
            if current == 0.0:
                break

        failed_states.add(state)
        return False

    return bars if search(0) else None


def pack(rows: list[tuple[str, int, float, str]], stock_length: float, kerf: float) -> list[StockBar]:
    cuts = [
        Cut(name, length, note, ordinal)
        for name, quantity, length, note in rows
        for ordinal in range(1, quantity + 1)
    ]
    cuts.sort(key=lambda cut: (-cut.length, cut.name, cut.ordinal))

    for cut in cuts:
        if cut.length + kerf > stock_length + 1e-9:
            raise SystemExit(
                f"cutlist=fail reason=piece_exceeds_stock piece={cut.name} "
                f"length={cut.length:.2f} stock={stock_length:.2f}"
            )

    # First-fit is only an upper bound. Search from the volume lower bound
    # upward so the checked-in cut list proves the stock minimum instead of
    # depending on heuristic order.
    upper = _first_fit_decreasing(cuts, stock_length, kerf)
    lower_count = math.ceil(
        sum(cut.length + kerf for cut in cuts) / stock_length - 1e-12
    )
    for count in range(lower_count, len(upper) + 1):
        exact = _pack_into_count(cuts, stock_length, kerf, count)
        if exact is not None:
            return exact
    return upper


def pack_dualbar_for_reusable_offcut(
    rows: list[tuple[str, int, float, str]],
    stock_length: float,
    kerf: float,
) -> list[StockBar]:
    """Keep the fifth-stick remainder as one useful fixture-bar offcut.

    Many five-stick packings consume the same aluminum.  Four identical outer
    frame groups plus a two-fixture-bar fifth stick leave one 381.6 mm
    remainder that can still yield a third fixture bar. Fail closed if the
    variant's cut contract changes rather than silently emitting a less
    reusable assignment.
    """

    expected = {
        "outer_vertical_rail": (4, 360.0),
        "outer_depth_rail": (4, 318.0),
        "outer_width_rail": (4, 306.0),
        "fixture_support_bar": (2, FIXTURE_BAR_LENGTH_MM),
    }
    actual = {name: (quantity, length) for name, quantity, length, _ in rows}
    if actual != expected:
        raise SystemExit(
            "cutlist=fail reason=dualbar_reuse_contract_changed "
            f"expected={expected!r} actual={actual!r}"
        )

    notes = {name: note for name, _, _, note in rows}
    # Four outer-frame repetitions plus one fixture-bar-only stick.
    bars = [StockBar(number, stock_length, kerf) for number in range(1, 6)]
    for index in range(4):
        for name in (
            "outer_vertical_rail",
            "outer_depth_rail",
            "outer_width_rail",
        ):
            bars[index].cuts.append(
                Cut(name, expected[name][1], notes[name], index + 1)
            )
    for ordinal in (1, 2):
        bars[4].cuts.append(
            Cut(
                "fixture_support_bar",
                expected["fixture_support_bar"][1],
                notes["fixture_support_bar"],
                ordinal,
            )
        )

    if any(bar.remaining < -1e-9 for bar in bars):
        raise SystemExit(
            "cutlist=fail reason=dualbar_reuse_assignment_exceeds_stock"
        )
    lower_bound = math.ceil(
        sum(
            quantity * (length + kerf)
            for _, quantity, length, _ in rows
        )
        / stock_length
        - 1e-12
    )
    if lower_bound != len(bars):
        raise SystemExit(
            "cutlist=fail reason=dualbar_reuse_assignment_not_minimal "
            f"lower_bound={lower_bound} assigned={len(bars)}"
        )
    return bars


def write_csv(path: Path, rows: list[tuple[str, int, float, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["part", "quantity", "finished_length_mm", "total_mm", "note"])
        for name, quantity, length, note in rows:
            writer.writerow([name, quantity, f"{length:.2f}", f"{quantity * length:.2f}", note])


def write_markdown(
    path: Path,
    rows: list[tuple[str, int, float, str]],
    bars: list[StockBar],
    stock_length: float,
    kerf: float,
    topology: str,
    frame_outer: tuple[float, float, float],
    frame_clear: tuple[float, float, float],
    variant: str,
    qualification_status: str,
) -> None:
    finished_total = sum(quantity * length for _, quantity, length, _ in rows)
    stock_total = len(bars) * stock_length
    kerf_total = sum(len(bar.cuts) for bar in bars) * kerf
    waste_total = stock_total - finished_total - kerf_total

    if variant == "dualbar_v1":
        fixture_savings = (
            LEGACY_FIXTURE_EXTRUSION_MM - DUALBAR_FIXTURE_EXTRUSION_MM
        )
        whole_chassis_savings = LEGACY_FINISHED_TOTAL_MM - finished_total
        offcut_minimum = FIXTURE_BAR_LENGTH_MM + kerf
        known_offcut = 356.4
        known_offcut_remainder = known_offcut - offcut_minimum
        outer_bar_consumed = 360.0 + 318.0 + 306.0 + 3 * kerf
        outer_bar_remainder = stock_length - outer_bar_consumed
        exact_pair_consumed = 2 * offcut_minimum
        exact_pair_remainder = stock_length - exact_pair_consumed
        batch_consumed = 3 * offcut_minimum
        batch_remainder = stock_length - batch_consumed
        lines = [
            "# PocketForge 2020 chassis cut list — dual-bar variant",
            "",
            f"- Chassis variant: `{variant}`",
            f"- Qualification: **{qualification_status}** (`tsp-t1zd.2`; accepted 2026-08-03)",
            f"- Join topology: `{topology}`",
            f"- External assembled envelope (W × D × H): {frame_outer[0]:.2f} × {frame_outer[1]:.2f} × {frame_outer[2]:.2f} mm",
            f"- Clear internal envelope (W × D × H): {frame_clear[0]:.2f} × {frame_clear[1]:.2f} × {frame_clear[2]:.2f} mm",
            f"- Stock: {stock_length:.2f} mm bars",
            f"- Conservative kerf allowance: {kerf:.2f} mm per finished piece",
            f"- Stock bars required with no reusable offcut: **{len(bars)}**",
            "- Fresh stock required with one qualifying offcut: **5 bars**",
            "- Fresh stock required with two qualifying offcuts: **4 bars**",
            f"- Finished extrusion: {finished_total:.2f} mm",
            f"- Finished-extrusion savings versus legacy gantry: {whole_chassis_savings:.2f} mm ({whole_chassis_savings / LEGACY_FINISHED_TOTAL_MM * 100:.2f}%)",
            f"- Fixture-support savings: {fixture_savings:.2f} mm ({fixture_savings / LEGACY_FIXTURE_EXTRUSION_MM * 100:.2f}%)",
            f"- Kerf allowance: {kerf_total:.2f} mm",
            f"- Remaining stock/offcuts when starting from five full bars: {waste_total:.2f} mm",
            "",
            "Finished lengths are measured aluminum cuts. This candidate preserves the proven outer frame and uses two continuous fixture bars: one between the lower depth rails and one between the upper depth rails. The matched pair remains movable for camera-distance adjustment. Never splice either fixture bar.",
            "",
            "## Scrap-first plan",
            "",
            f"Each 306.00 mm `fixture_support_bar` needs one straight, undamaged 2020 offcut measuring at least **{offcut_minimum:.2f} mm**. Two qualifying offcuts supply the complete upper/lower pair and reduce fresh stock to the four tightly packed outer-frame sticks.",
            "",
            f"The known **{known_offcut:.2f} mm** retained offcut qualifies for one fixture bar and leaves **{known_offcut_remainder:.2f} mm**, but it cannot supply both bars. With only that one offcut, a fifth fresh stick is still required for the other fixture bar. Each outer-frame stick yields one 360 mm post, one 318 mm depth rail, and one 306 mm width rail: {outer_bar_consumed:.2f} mm kerf-inclusive consumed and {outer_bar_remainder:.2f} mm remaining.",
            "",
            "## Fifth-stick and batch route",
            "",
            f"For one chassis, two fixture bars plus two kerfs consume **{exact_pair_consumed:.2f} mm** of the fifth stick and leave a straight **{exact_pair_remainder:.2f} mm** offcut. That remainder still qualifies for one future fixture bar; label and retain it.",
            "",
            f"For batch cutting, three 306.00 mm fixture bars plus three kerfs consume **{batch_consumed:.2f} mm** and leave **{batch_remainder:.2f} mm**. Use two now and label the third as the first bar of the next chassis. The known 356.40 mm offcut plus all three bars from one fresh stick supplies the four fixture bars needed by two chassis.",
            "",
            "## Finished pieces",
            "",
            "| Part | Qty | Length (mm) | Total (mm) | Purpose |",
            "|---|---:|---:|---:|---|",
        ]
    else:
        lines = [
        "# PocketForge 2020 chassis cut list",
        "",
        f"- Join topology: `{topology}`",
        f"- External assembled envelope (W × D × H): {frame_outer[0]:.2f} × {frame_outer[1]:.2f} × {frame_outer[2]:.2f} mm",
        f"- Clear internal envelope (W × D × H): {frame_clear[0]:.2f} × {frame_clear[1]:.2f} × {frame_clear[2]:.2f} mm",
        f"- Stock: {stock_length:.2f} mm bars",
        f"- Conservative kerf allowance: {kerf:.2f} mm per finished piece",
        f"- Stock bars required: **{len(bars)}**",
        f"- Finished extrusion: {finished_total:.2f} mm",
        f"- Kerf allowance: {kerf_total:.2f} mm",
        f"- Remaining stock/offcuts: {waste_total:.2f} mm",
        "",
        "Finished lengths are measured aluminum cuts. The delivered three-way connector was physically checked: horizontal rails butt flush to adjacent faces of each vertical post, their top/bottom outer faces are flush with the connector-cap planes, and a 360.00 mm post with caps at both ends measures approximately 368 mm outside-to-outside. "
        "The assignment below is an exact bounded packing, not first-fit order; retain the listed kerf reserve, measure every stock stick, mark every finished cut before sawing, and witness one saw cut before batch cutting.",
        "",
        "## Node 1 already-cut reuse",
        "",
        "Node 1 predates the width/depth axis swap and reuses every finished piece:",
        "",
        "- install four existing 318 mm rails as the outer depth rails;",
        "- install four existing 306 mm rails as the outer width rails;",
        "- retain all four 360 mm posts and all four 164 mm upright halves unchanged;",
        "- trim only the remaining two 318 mm rails to a 306 mm finished length for the fixture crossbars (12 mm shorter each; remove kerf from the waste side).",
        "",
        "## Finished pieces",
        "",
        "| Part | Qty | Length (mm) | Total (mm) | Purpose |",
        "|---|---:|---:|---:|---|",
        ]
    lines.extend(
        f"| `{name}` | {quantity} | {length:.2f} | {quantity * length:.2f} | {note} |"
        for name, quantity, length, note in rows
    )
    assignment_heading = (
        "## 1 m stock assignment — no reusable offcut"
        if variant == "dualbar_v1"
        else "## 1 m stock assignment"
    )
    lines.extend(["", assignment_heading, ""])
    for bar in bars:
        pieces = ", ".join(f"{cut.name} {cut.length:.2f}" for cut in bar.cuts)
        lines.append(
            f"- Bar {bar.number}: {pieces}; kerf-inclusive consumed "
            f"{bar.consumed:.2f} mm; remainder {bar.remaining:.2f} mm"
        )
    if variant == "dualbar_v1":
        qualification_boundary = (
            f"`{qualification_status}` records the completed `tsp-t1zd.2` "
            "physical gate for the exact locked dual-bar layout. The printed "
            "fit, fastener engagement, loaded plate stability, camera "
            "alignment, service access, and owner approval were accepted on "
            "2026-08-03. Any geometry or topology change requires a new "
            "candidate layout and a fresh physical gate; do not edit this "
            "qualified layout in place."
        )
        lines.extend(
            [
                "",
                "## Qualification boundary",
                "",
                qualification_boundary,
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--markdown", required=True, type=Path)
    args = parser.parse_args()

    (
        rows,
        stock_length,
        kerf,
        topology,
        frame_outer,
        frame_clear,
        variant,
        qualification_status,
    ) = parse_echoes(args.input)
    bars = (
        pack_dualbar_for_reusable_offcut(rows, stock_length, kerf)
        if variant == "dualbar_v1"
        else pack(rows, stock_length, kerf)
    )
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.csv, rows)
    write_markdown(
        args.markdown,
        rows,
        bars,
        stock_length,
        kerf,
        topology,
        frame_outer,
        frame_clear,
        variant,
        qualification_status,
    )
    print(
        f"cutlist=pass parts={sum(row[1] for row in rows)} "
        f"stock_bars={len(bars)} stock_length_mm={stock_length:.2f} "
        f"variant={variant} qualification={qualification_status}"
    )


if __name__ == "__main__":
    main()
