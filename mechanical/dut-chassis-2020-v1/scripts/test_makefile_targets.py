#!/usr/bin/env python3
"""Protect production batches and the canonical dual-bar handbook scene."""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CORE_BATCHES = tuple(range(1, 6))
DEVICE_EXAMPLE_BATCHES = (6, 7)
DUALBAR_CORE_OUTPUTS = (
    "dualbar/production-batch-01-ironed-interfaces.stl",
    "dualbar/production-batch-02-fixture-links.stl",
    "dualbar/production-batch-04-frame-hardware.stl",
    "dualbar/production-batch-05-placard-holder.stl",
)
GUIDE_LAYER_COUNT = 70
GUIDE_SCENE_DEFINES = (
    """-D 'CHASSIS_VARIANT="dualbar_v1"'""",
    """-D 'EXAMPLE_DEVICE_VARIANT="smart_pro_s"'""",
)
DEVICE_MODEL_COMMIT = "80662c40bd7d878a19127899760bdafb1f149173"
DEVICE_MODEL_SHA256 = (
    "0d5c8153639537d5e70941492ad2cc930f5fb1c93f3694e9a160f5770693224d"
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
    dualbar = dry_run("dualbar-batches")
    handbook = dry_run("handbook-assets")

    require(core, CORE_BATCHES, "batches")
    reject(core, DEVICE_EXAMPLE_BATCHES, "batches")
    if "dualbar/production-batch-" in core:
        raise SystemExit("batches includes candidate dual-bar outputs")
    require_names(dualbar, DUALBAR_CORE_OUTPUTS, "dualbar-batches")
    reject(dualbar, DEVICE_EXAMPLE_BATCHES, "dualbar-batches")
    if "production-batch-02-splice-collars.stl" in dualbar:
        raise SystemExit("dualbar-batches includes legacy gantry splice collars")
    require_names(handbook, DUALBAR_CORE_OUTPUTS, "handbook-assets")
    require(handbook, DEVICE_EXAMPLE_BATCHES, "handbook-assets")
    if "production-batch-02-splice-collars.stl" in handbook:
        raise SystemExit("handbook-assets still builds legacy splice collars")
    guide_layer_lines = [
        line for line in handbook.splitlines() if 'PART="guide_layer_' in line
    ]
    if len(guide_layer_lines) != GUIDE_LAYER_COUNT:
        raise SystemExit(
            "handbook semantic layer count changed: "
            f"{len(guide_layer_lines)} != {GUIDE_LAYER_COUNT}"
        )
    for line in guide_layer_lines:
        missing_defines = [
            define for define in GUIDE_SCENE_DEFINES if define not in line
        ]
        if missing_defines:
            raise SystemExit(
                "handbook layer is not locked to the Smart Pro S dual-bar "
                f"scene: {line}"
            )
    hero_lines = [
        line for line in handbook.splitlines() if "build/handbook/hero.png" in line
    ]
    if len(hero_lines) != 1 or any(
        define not in hero_lines[0] for define in GUIDE_SCENE_DEFINES
    ):
        raise SystemExit(
            "handbook hero is not locked to the Smart Pro S dual-bar scene"
        )
    for required in (
        "device-models/trimui-smart-pro-s/trimui-smart-pro-s.scad",
        DEVICE_MODEL_COMMIT,
        DEVICE_MODEL_SHA256,
        "--device-slug trimui-smart-pro-s",
        "--chassis-variant dualbar_v1",
        "--device-registry ../device-packs/device-layouts.json",
        "--layout-record ../device-packs/layouts/chassis-dualbar-v1.json",
    ):
        if required not in handbook:
            raise SystemExit(
                f"handbook scene omits source/provenance contract: {required}"
            )
    if "device-models/trimui-smart-pro/trimui-smart-pro.scad" in handbook:
        raise SystemExit("handbook scene still fetches the base Smart Pro model")
    print(
        "makefile_target_contract=pass "
        "legacy_core_batches=5 dualbar_candidate_core_batches=4 "
        "handbook_device_examples=2 handbook_scene=smart-pro-s-dualbar "
        f"semantic_layers={GUIDE_LAYER_COUNT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
