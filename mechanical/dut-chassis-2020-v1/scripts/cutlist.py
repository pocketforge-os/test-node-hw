#!/usr/bin/env python3
"""Convert OpenSCAD PFCUT echoes into deterministic cut-list artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path


ECHO_RE = re.compile(r'^ECHO:\s+"(?P<payload>PF(?:CUT|STOCK)\|.*)"\s*$')


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


def parse_echoes(path: Path) -> tuple[list[tuple[str, int, float, str]], float, float, str]:
    rows: list[tuple[str, int, float, str]] = []
    stock_length = 0.0
    kerf = 0.0
    topology = ""

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

    if not rows:
        raise SystemExit(f"cutlist=fail reason=no_PFCUT_echoes input={path}")
    if stock_length <= 0 or kerf < 0 or not topology:
        raise SystemExit(f"cutlist=fail reason=invalid_PFSTOCK input={path}")
    return rows, stock_length, kerf, topology


def pack(rows: list[tuple[str, int, float, str]], stock_length: float, kerf: float) -> list[StockBar]:
    cuts = [
        Cut(name, length, note, ordinal)
        for name, quantity, length, note in rows
        for ordinal in range(1, quantity + 1)
    ]
    cuts.sort(key=lambda cut: (-cut.length, cut.name, cut.ordinal))

    bars: list[StockBar] = []
    for cut in cuts:
        if cut.length + kerf > stock_length + 1e-9:
            raise SystemExit(
                f"cutlist=fail reason=piece_exceeds_stock piece={cut.name} "
                f"length={cut.length:.2f} stock={stock_length:.2f}"
            )
        destination = next((bar for bar in bars if bar.fits(cut)), None)
        if destination is None:
            destination = StockBar(len(bars) + 1, stock_length, kerf)
            bars.append(destination)
        destination.cuts.append(cut)
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
) -> None:
    finished_total = sum(quantity * length for _, quantity, length, _ in rows)
    stock_total = len(bars) * stock_length
    kerf_total = sum(len(bar.cuts) for bar in bars) * kerf
    waste_total = stock_total - finished_total - kerf_total

    lines = [
        "# PocketForge 2020 chassis cut list",
        "",
        f"- Join topology: `{topology}`",
        f"- Stock: {stock_length:.2f} mm bars",
        f"- Conservative kerf allowance: {kerf:.2f} mm per finished piece",
        f"- Stock bars required: **{len(bars)}**",
        f"- Finished extrusion: {finished_total:.2f} mm",
        f"- Kerf allowance: {kerf_total:.2f} mm",
        f"- Remaining stock/offcuts: {waste_total:.2f} mm",
        "",
        "Do not batch-cut until one physical three-way connector dry-fit confirms the finished rail length. "
        "The stock assignment deliberately pairs two 360 mm pieces with one 180 mm gantry-upright half per bar; kerf therefore controls the guaranteed short-piece yield.",
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
    lines.extend(["", "## 1 m stock assignment", ""])
    for bar in bars:
        pieces = ", ".join(f"{cut.name} {cut.length:.2f}" for cut in bar.cuts)
        lines.append(
            f"- Bar {bar.number}: {pieces}; kerf-inclusive consumed "
            f"{bar.consumed:.2f} mm; remainder {bar.remaining:.2f} mm"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--markdown", required=True, type=Path)
    args = parser.parse_args()

    rows, stock_length, kerf, topology = parse_echoes(args.input)
    bars = pack(rows, stock_length, kerf)
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.csv, rows)
    write_markdown(args.markdown, rows, bars, stock_length, kerf, topology)
    print(
        f"cutlist=pass parts={sum(row[1] for row in rows)} "
        f"stock_bars={len(bars)} stock_length_mm={stock_length:.2f}"
    )


if __name__ == "__main__":
    main()
