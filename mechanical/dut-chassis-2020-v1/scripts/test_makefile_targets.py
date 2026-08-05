#!/usr/bin/env python3
"""Protect production batches and the canonical dual-bar handbook scene."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from handbook_scene_contract import (
    digest,
    load_scene_contract,
    validate_layout_binding,
)

PROJECT = Path(__file__).resolve().parents[1]
CORE_BATCHES = tuple(range(1, 6))
DEVICE_EXAMPLE_BATCHES = (6, 7)
DUALBAR_CORE_OUTPUTS = (
    "dualbar/production-batch-01-ironed-interfaces.stl",
    "dualbar/production-batch-02-fixture-links.stl",
    "dualbar/production-batch-04-frame-hardware.stl",
    "dualbar/production-batch-05-placard-holder.stl",
)
BRICK_DUALBAR_REVIEW = (
    "build/dualbar-brick/layout-assembly.png",
    "build/dualbar-brick/layout-front.png",
    "build/dualbar-brick/layout-device-side.png",
)
GUIDE_LAYER_COUNT = 70
GUIDE_SCENE_DEFINES = (
    """-D 'CHASSIS_VARIANT="dualbar_v1"'""",
    """-D 'CARRIER_LINK_REVISION="stack_clear_v2"'""",
    """-D 'EXAMPLE_DEVICE_VARIANT="smart_pro_s"'""",
)
GUIDE_DUALBAR_ASSEMBLY = (
    (
        "build/handbook/assembly-01-channel-bar.png",
        "guide_dualbar_assembly_01_channel_bar",
    ),
    (
        "build/handbook/assembly-02-width-rails.png",
        "guide_dualbar_assembly_02_width_rails",
    ),
    (
        "build/handbook/assembly-03-depth-rails.png",
        "guide_dualbar_assembly_03_depth_rails",
    ),
    (
        "build/handbook/assembly-04-fixture-bars.png",
        "guide_dualbar_assembly_04_fixture_bars",
    ),
    (
        "build/handbook/assembly-05-lower-frame.png",
        "guide_dualbar_assembly_05_lower_frame",
    ),
    (
        "build/handbook/assembly-06-lower-fixture-bar.png",
        "guide_dualbar_assembly_06_lower_fixture_bar",
    ),
    (
        "build/handbook/assembly-07-posts.png",
        "guide_dualbar_assembly_07_posts",
    ),
    (
        "build/handbook/assembly-08-upper-ring.png",
        "guide_dualbar_assembly_08_upper_ring",
    ),
    (
        "build/handbook/assembly-09-upper-fixture-bar.png",
        "guide_dualbar_assembly_09_upper_fixture_bar",
    ),
    (
        "build/handbook/assembly-10-close-frame.png",
        "guide_dualbar_assembly_10_close_frame",
    ),
    (
        "build/handbook/assembly-11-square-frame.png",
        "guide_dualbar_assembly_11_square_frame",
    ),
    (
        "build/handbook/assembly-12-dut-holder.png",
        "guide_dualbar_assembly_12_dut_holder",
    ),
    (
        "build/handbook/assembly-13-fixture-board.png",
        "guide_dualbar_assembly_13_fixture_board",
    ),
    (
        "build/handbook/assembly-14-placard.png",
        "guide_dualbar_assembly_14_placard",
    ),
    (
        "build/handbook/assembly-15-power-strip.png",
        "guide_dualbar_assembly_15_power_strip",
    ),
    (
        "build/handbook/assembly-16-stacking-tabs.png",
        "guide_dualbar_assembly_16_stacking_tabs",
    ),
    (
        "build/handbook/assembly-17-final.png",
        "guide_dualbar_assembly_17_final",
    ),
)
RETIRED_ASSEMBLY_PART_TOKENS = (
    "guide_step_",
    "gantry",
    "splice",
    "fixture_spacer",
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


def require_handbook_layout_binding_contract() -> None:
    with TemporaryDirectory() as temporary_directory:
        repository_root = Path(temporary_directory)
        layouts = repository_root / "device-packs" / "layouts"
        layouts.mkdir(parents=True)
        registry_path = repository_root / "device-packs" / "device-layouts.json"
        model_path = repository_root / "device-model.scad"
        model_path.write_text("cube([1, 1, 1]);\n", encoding="utf-8")

        active_relative = "device-packs/layouts/active-candidate.json"
        historical_relative = "device-packs/layouts/historical-qualified.json"
        active = {
            "layout_id": "active-candidate",
            "qualification": {
                "status": "candidate",
                "acceptance_ref": "tsp-active-candidate",
                "device_slugs": ["trimui-smart-pro-s"],
            },
            "artifacts": [
                {"parameters": {"CHASSIS_VARIANT": "dualbar_v1"}}
            ],
        }
        historical = {
            "layout_id": "historical-qualified",
            "qualification": {
                "status": "physically_qualified",
                "acceptance_ref": "tsp-historical-qualified",
                "device_slugs": ["trimui-smart-pro-s"],
            },
            "artifacts": [
                {"parameters": {"CHASSIS_VARIANT": "dualbar_v1"}}
            ],
        }
        registry_path.write_text(
            json.dumps(
                {
                    "devices": {
                        "trimui-smart-pro-s": {"layout": active_relative}
                    }
                }
            ),
            encoding="utf-8",
        )
        active_path = repository_root / active_relative
        historical_path = repository_root / historical_relative
        active_path.write_text(json.dumps(active), encoding="utf-8")
        historical_path.write_text(json.dumps(historical), encoding="utf-8")

        common = {
            "device_slug": "trimui-smart-pro-s",
            "chassis_variant": "dualbar_v1",
            "device_registry": registry_path,
            "device_model_source": model_path,
            "device_model_url": "https://example.invalid/device-models.git",
            "device_model_commit": "0123456789abcdef",
            "device_model_sha256": digest(model_path),
        }
        active_contract = load_scene_contract(
            SimpleNamespace(**common, layout_record=active_path), repository_root
        )
        historical_contract = load_scene_contract(
            SimpleNamespace(**common, layout_record=historical_path),
            repository_root,
        )

        expected_provenance = {
            "active-candidate": {
                "record": active_relative,
                "status": "candidate",
                "acceptance_ref": "tsp-active-candidate",
            },
            "historical-qualified": {
                "record": historical_relative,
                "status": "physically_qualified",
                "acceptance_ref": "tsp-historical-qualified",
            },
        }
        for contract in (active_contract, historical_contract):
            expected = expected_provenance[contract["layout_id"]]
            actual = {
                "record": contract["layout_record"],
                **contract["qualification"],
            }
            if actual != expected:
                raise SystemExit(
                    "handbook scene provenance used the wrong layout record: "
                    f"{actual!r} != {expected!r}"
                )

    qualified = {
        "layout_id": "chassis-dualbar-v1",
        "qualification": {
            "status": "physically_qualified",
            "device_slugs": ["trimui-smart-pro-s"],
        },
    }
    historical_qualification = validate_layout_binding(
        device_slug="trimui-smart-pro-s",
        registered_layout="layouts/chassis-dualbar-v2.json",
        layout_relative="layouts/chassis-dualbar-v1.json",
        layout=qualified,
    )
    active_qualification = validate_layout_binding(
        device_slug="trimui-smart-pro-s",
        registered_layout="layouts/chassis-dualbar-v1.json",
        layout_relative="layouts/chassis-dualbar-v1.json",
        layout=qualified,
    )
    if historical_qualification is not qualified["qualification"]:
        raise SystemExit(
            "historical handbook binding lost its qualification provenance"
        )
    if active_qualification is not qualified["qualification"]:
        raise SystemExit(
            "active handbook binding lost its qualification provenance"
        )
    if historical_qualification.get("status") != "physically_qualified":
        raise SystemExit(
            "historical handbook provenance did not retain qualification status"
        )

    invalid_cases = (
        (
            None,
            qualified,
            "has no active registered layout",
        ),
        (
            "layouts/chassis-dualbar-v2.json",
            {
                **qualified,
                "qualification": {
                    **qualified["qualification"],
                    "status": "candidate",
                },
            },
            "is not physically qualified",
        ),
        (
            "layouts/chassis-dualbar-v2.json",
            qualified,
            "outside chassis-dualbar-v1 qualification scope",
        ),
    )
    for index, (registered, layout, expected) in enumerate(invalid_cases):
        device_slug = (
            "trimui-smart-pro" if index == len(invalid_cases) - 1
            else "trimui-smart-pro-s"
        )
        try:
            validate_layout_binding(
                device_slug=device_slug,
                registered_layout=registered,
                layout_relative="layouts/chassis-dualbar-v1.json",
                layout=layout,
            )
        except ValueError as error:
            if expected not in str(error):
                raise SystemExit(
                    "handbook layout binding failed with the wrong reason: "
                    f"{error}"
                ) from error
        else:
            raise SystemExit(
                "unsafe handbook layout binding was unexpectedly accepted"
            )


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


def require_dualbar_assembly_contract(output: str) -> None:
    logical_output = output.replace("\\\n\t", " ")
    commands = [
        line for line in logical_output.splitlines() if line.startswith("openscad ")
    ]
    expected_outputs = tuple(item[0] for item in GUIDE_DUALBAR_ASSEMBLY)
    rendered_outputs: list[str] = []

    for command in commands:
        matches = [name for name in expected_outputs if name in command]
        if len(matches) > 1:
            raise SystemExit(
                f"one assembly render command owns multiple outputs: {command}"
            )
        rendered_outputs.extend(matches)

    if tuple(rendered_outputs) != expected_outputs:
        raise SystemExit(
            "dual-bar assembly output order changed: "
            f"{rendered_outputs!r} != {expected_outputs!r}"
        )

    for output_name, part_name in GUIDE_DUALBAR_ASSEMBLY:
        matching = [command for command in commands if output_name in command]
        if len(matching) != 1:
            raise SystemExit(
                f"{output_name} has {len(matching)} render commands instead of 1"
            )
        command = matching[0]
        for define in GUIDE_SCENE_DEFINES:
            if define not in command:
                raise SystemExit(
                    f"{output_name} is not locked to the Smart Pro S dual-bar scene"
                )
        if f'PART="{part_name}"' not in command:
            raise SystemExit(
                f"{output_name} does not render its ordered source scene: {command}"
            )
        retired = [
            token for token in RETIRED_ASSEMBLY_PART_TOKENS if token in command
        ]
        if retired:
            raise SystemExit(
                f"{output_name} references retired assembly parts: {retired!r}"
            )


def main() -> int:
    require_handbook_layout_binding_contract()
    core = dry_run("batches")
    dualbar = dry_run("dualbar-batches")
    handbook = dry_run("handbook-assets")
    assembly = dry_run("guide-dualbar-assembly-steps")
    brick_preview = dry_run("brick-dualbar-preview")

    require(core, CORE_BATCHES, "batches")
    reject(core, DEVICE_EXAMPLE_BATCHES, "batches")
    if "dualbar/production-batch-" in core:
        raise SystemExit("legacy batch target includes dual-bar outputs")
    require_names(dualbar, DUALBAR_CORE_OUTPUTS, "dualbar-batches")
    reject(dualbar, DEVICE_EXAMPLE_BATCHES, "dualbar-batches")
    if "production-batch-02-splice-collars.stl" in dualbar:
        raise SystemExit("dualbar-batches includes legacy gantry splice collars")
    require_names(
        brick_preview, BRICK_DUALBAR_REVIEW, "brick-dualbar-preview"
    )
    if brick_preview.count('EXAMPLE_DEVICE_VARIANT="trimui_brick"') != 3:
        raise SystemExit(
            "Brick dual-bar evidence is not locked to all three review views"
        )
    require_names(handbook, DUALBAR_CORE_OUTPUTS, "handbook-assets")
    require(handbook, DEVICE_EXAMPLE_BATCHES, "handbook-assets")
    if "production-batch-02-splice-collars.stl" in handbook:
        raise SystemExit("handbook-assets still builds legacy splice collars")
    require_names(
        handbook,
        tuple(item[0] for item in GUIDE_DUALBAR_ASSEMBLY),
        "handbook-assets",
    )
    require_dualbar_assembly_contract(assembly)
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
        "legacy_core_batches=5 dualbar_qualified_core_batches=4 "
        "handbook_device_examples=2 handbook_scene=smart-pro-s-dualbar "
        f"semantic_layers={GUIDE_LAYER_COUNT} assembly_steps=17"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
