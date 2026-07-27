#!/usr/bin/env python3
"""Protect the chassis-core and legacy handbook target boundary."""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CORE_BATCHES = tuple(range(1, 6))
DEVICE_EXAMPLE_BATCHES = (6, 7)
TOPBAR_CORE_OUTPUTS = (
    "topbar/production-batch-01-ironed-interfaces.stl",
    "topbar/production-batch-02-upper-hangers.stl",
    "topbar/production-batch-03-lower-backstays.stl",
    "topbar/production-batch-04-frame-hardware.stl",
    "topbar/production-batch-05-placard-holder.stl",
)


def dry_run(target: str) -> str:
    result = subprocess.run(
        [
            "make",
            "--no-print-directory",
            "--directory",
            str(PROJECT),
            "--dry-run",
            "--always-make",
            target,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.stdout


def output_name(batch: int) -> str:
    names = {
        1: "ironed-interfaces",
        2: "splice-collars",
        3: "movable-mounts",
        4: "frame-hardware",
        5: "placard-holder",
        6: "device-nameplate",
        7: "wire-management",
    }
    return f"production-batch-{batch:02d}-{names[batch]}.stl"


def require(output: str, batches: tuple[int, ...], target: str) -> None:
    missing = [
        output_name(batch)
        for batch in batches
        if output_name(batch) not in output
    ]
    if missing:
        raise SystemExit(f"{target} omits required outputs: {', '.join(missing)}")


def reject(output: str, batches: tuple[int, ...], target: str) -> None:
    unexpected = [
        output_name(batch) for batch in batches if output_name(batch) in output
    ]
    if unexpected:
        raise SystemExit(
            f"{target} includes device-specific outputs: {', '.join(unexpected)}"
        )


def require_names(output: str, names: tuple[str, ...], target: str) -> None:
    missing = [name for name in names if name not in output]
    if missing:
        raise SystemExit(
            f"{target} omits required outputs: {', '.join(missing)}"
        )


def main() -> int:
    core = dry_run("batches")
    topbar = dry_run("topbar-batches")
    handbook = dry_run("handbook-assets")

    require(core, CORE_BATCHES, "batches")
    reject(core, DEVICE_EXAMPLE_BATCHES, "batches")
    if "topbar/production-batch-" in core:
        raise SystemExit("batches includes candidate top-bar outputs")
    require_names(topbar, TOPBAR_CORE_OUTPUTS, "topbar-batches")
    reject(topbar, DEVICE_EXAMPLE_BATCHES, "topbar-batches")
    if "production-batch-02-splice-collars.stl" in topbar:
        raise SystemExit("topbar-batches includes legacy gantry splice collars")
    require(
        handbook,
        CORE_BATCHES + DEVICE_EXAMPLE_BATCHES,
        "handbook-assets",
    )
    print(
        "makefile_target_contract=pass "
        "legacy_core_batches=5 topbar_candidate_core_batches=5 "
        "handbook_device_examples=2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
