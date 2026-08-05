#!/usr/bin/env python3
"""Build the PocketForge handbook's semantic glTF model from OpenSCAD layers."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

from handbook_scene_contract import digest, load_scene_contract


LAYER_MATERIALS = {
    "aluminum": ("Aluminum extrusion", "#a8afb8", 0.72, 0.28, 1.0),
    "connectors": ("Metal connectors", "#24282e", 0.78, 0.30, 1.0),
    "printed-hardware": ("Printed chassis hardware", "#e96a0a", 0.02, 0.48, 1.0),
    "fixture-plate": ("Fixture plate", "#d9dbd6", 0.0, 0.58, 1.0),
    "fixture-components": ("Fixture retention ties", "#111418", 0.02, 0.48, 1.0),
    "fixture-labels": ("Fixture labels", "#16794f", 0.0, 0.55, 1.0),
    "fixture-relay-pcb": (
        "ELEGOO relay blue PCB", "#0d6f9f", 0.0, 0.44, 1.0
    ),
    "fixture-relay-blue": (
        "ELEGOO relay cans and terminal bodies",
        "#1688c5",
        0.0,
        0.38,
        1.0,
    ),
    "fixture-relay-dark": (
        "ELEGOO relay optocouplers and drivers",
        "#15191d",
        0.0,
        0.34,
        1.0,
    ),
    "fixture-relay-metal": (
        "ELEGOO relay terminals and pins", "#c5c9cc", 0.76, 0.24, 1.0
    ),
    "fixture-relay-led": (
        "ELEGOO relay status LEDs", "#d72828", 0.0, 0.28, 1.0
    ),
    "fixture-relay-silkscreen": (
        "ELEGOO relay markings", "#eef2ed", 0.0, 0.50, 1.0
    ),
    "fixture-boost-pcb": (
        "HiLetgo XL6009 blue PCB", "#0c559f", 0.0, 0.44, 1.0
    ),
    "fixture-boost-dark": (
        "XL6009 regulator, inductor, and passives",
        "#131820",
        0.0,
        0.34,
        1.0,
    ),
    "fixture-boost-adjuster": (
        "XL6009 blue W103 adjuster", "#176fce", 0.0, 0.38, 1.0
    ),
    "fixture-boost-metal": (
        "XL6009 capacitors, pads, leads, and screw",
        "#c2c8cd",
        0.76,
        0.24,
        1.0,
    ),
    "fixture-boost-silkscreen": (
        "XL6009 polarity and component markings", "#eef1eb", 0.0, 0.50, 1.0
    ),
    "fixture-mosfet-pcb": (
        "Ceksezx MTSD001 blue PCB", "#0d65a7", 0.0, 0.44, 1.0
    ),
    "fixture-mosfet-blue": (
        "MTSD001 terminal bodies", "#177fd0", 0.0, 0.38, 1.0
    ),
    "fixture-mosfet-dark": (
        "MTSD001 dual MOSFETs and passives", "#171a1e", 0.0, 0.34, 1.0
    ),
    "fixture-mosfet-metal": (
        "MTSD001 screws, pads, and leads", "#c4c9cd", 0.76, 0.24, 1.0
    ),
    "fixture-mosfet-led": (
        "MTSD001 indicator LED", "#dce99b", 0.0, 0.28, 1.0
    ),
    "fixture-mosfet-silkscreen": (
        "MTSD001 markings", "#eef2ed", 0.0, 0.50, 1.0
    ),
    "fixture-dp100-shell": (
        "ALIENTEK DP100 enclosure", "#262a2e", 0.0, 0.42, 1.0
    ),
    "fixture-dp100-dark": (
        "DP100 panel, ports, seam, and vents", "#090b0e", 0.0, 0.34, 1.0
    ),
    "fixture-dp100-controls": (
        "DP100 buttons and adjustment wheel", "#3d4248", 0.0, 0.38, 1.0
    ),
    "fixture-dp100-screen": (
        "DP100 0.96-inch IPS display", "#123e51", 0.08, 0.20, 1.0
    ),
    "fixture-dp100-accent": (
        "DP100 positive output and screen accents", "#c9342f", 0.05, 0.34, 1.0
    ),
    "fixture-dp100-metal": (
        "DP100 banana and USB interfaces", "#c89b3c", 0.78, 0.24, 1.0
    ),
    "fixture-dp100-markings": (
        "DP100 display and control markings", "#e8ece7", 0.0, 0.50, 1.0
    ),
    "fixture-bpi-pcb": (
        "Banana Pi blue PCB", "#1769a8", 0.0, 0.44, 1.0
    ),
    "fixture-bpi-dark": (
        "Banana Pi ICs and header", "#171a1e", 0.0, 0.38, 1.0
    ),
    "fixture-bpi-metal": (
        "Banana Pi shields and ports", "#b7bcc2", 0.78, 0.24, 1.0
    ),
    "fixture-bpi-gold": (
        "Banana Pi gold contacts", "#d9aa32", 0.82, 0.22, 1.0
    ),
    "fixture-bpi-silkscreen": (
        "Banana Pi silkscreen", "#e9ece6", 0.0, 0.52, 1.0
    ),
    "fixture-esp32-pcb": (
        "ESP32-S3 SuperMini black PCB", "#15191d", 0.0, 0.42, 1.0
    ),
    "fixture-esp32-dark": (
        "ESP32-S3 ICs and buttons", "#090b0e", 0.0, 0.34, 1.0
    ),
    "fixture-esp32-metal": (
        "ESP32-S3 USB-C and switch metal", "#b9bec4", 0.78, 0.24, 1.0
    ),
    "fixture-esp32-gold": (
        "ESP32-S3 plated contacts", "#d6a83a", 0.82, 0.22, 1.0
    ),
    "fixture-esp32-antenna": (
        "ESP32-S3 red ceramic antenna", "#c62326", 0.05, 0.36, 1.0
    ),
    "fixture-esp32-silkscreen": (
        "ESP32-S3 silkscreen", "#eceee8", 0.0, 0.50, 1.0
    ),
    "fixture-antenna-dark": (
        "Eightwood EWUA0205 antenna and coax", "#15181b", 0.0, 0.42, 1.0
    ),
    "fixture-antenna-metal": (
        "Eightwood MHF4 connector", "#c2a64b", 0.82, 0.22, 1.0
    ),
    "fixture-antenna-markings": (
        "Eightwood antenna markings", "#d7d9d4", 0.0, 0.50, 1.0
    ),
    "fixture-vienon-shell": (
        "VIENON Usb-001 enclosure and cable", "#16191d", 0.0, 0.42, 1.0
    ),
    "fixture-vienon-dark": (
        "VIENON seams and USB 2.0 tongues", "#07090b", 0.0, 0.34, 1.0
    ),
    "fixture-vienon-metal": (
        "VIENON USB interfaces", "#bfc4c8", 0.78, 0.24, 1.0
    ),
    "fixture-vienon-blue": (
        "VIENON USB 3.0 tongue", "#176fc0", 0.0, 0.32, 1.0
    ),
    "fixture-vienon-led": (
        "VIENON status LED", "#3da7e8", 0.0, 0.24, 1.0
    ),
    "fixture-smays-shell": (
        "Smays hub enclosure, leads, and DC cable", "#e7e8e5", 0.0, 0.50, 1.0
    ),
    "fixture-smays-dark": (
        "Smays ports, seams, and strain relief", "#17191c", 0.0, 0.34, 1.0
    ),
    "fixture-smays-metal": (
        "Smays USB, RJ45, and DC interfaces", "#c4c8cb", 0.78, 0.24, 1.0
    ),
    "fixture-smays-led": (
        "Smays Ethernet status LEDs", "#84bb55", 0.0, 0.28, 1.0
    ),
    "fixture-smays-markings": (
        "Smays enclosure markings", "#777b7d", 0.0, 0.48, 1.0
    ),
    "carrier-body": ("DUT carrier", "#e1e2dc", 0.0, 0.58, 1.0),
    "carrier-labels": ("Carrier labels", "#17191c", 0.0, 0.55, 1.0),
    "carrier-hooks": ("Carrier hooks", "#34383e", 0.0, 0.48, 1.0),
    "device-shell": ("DUT shell", "#22262b", 0.05, 0.42, 1.0),
    "device-controls": ("DUT controls", "#0f1114", 0.0, 0.38, 1.0),
    "device-screen": ("DUT screen", "#07161f", 0.08, 0.20, 1.0),
    "webcam-shell": (
        "Logitech C270 shell and articulated clip", "#3b4147", 0.0, 0.40, 1.0
    ),
    "webcam-dark": (
        "Logitech C270 bezel, lens barrel, and cable",
        "#101317",
        0.0,
        0.34,
        1.0,
    ),
    "webcam-glass": (
        "Logitech C270 lens glass", "#101d29", 0.10, 0.18, 1.0
    ),
    "webcam-led": (
        "Logitech C270 activity LED", "#b9d532", 0.0, 0.28, 1.0
    ),
    "webcam-labels": (
        "Logitech C270 markings", "#eceeea", 0.0, 0.52, 1.0
    ),
    "power-strip": ("Power strip", "#ecece7", 0.0, 0.62, 1.0),
    "placard-holder": ("Placard holder", "#17364f", 0.0, 0.48, 1.0),
    "placard-insert": ("White nameplate body", "#f5f5ed", 0.0, 0.48, 1.0),
    "placard-labels": ("Black raised labels", "#050505", 0.0, 0.48, 1.0),
    "camera-frustum": ("Camera field of view", "#51bfd4", 0.0, 0.30, 0.18),
}

# OpenSCAD is right-handed Z-up in millimetres. glTF is right-handed Y-up in
# metres. Map (x, y, z) -> (x, z, -y) while scaling once at the asset boundary.
OPENSCAD_TO_GLTF = np.array(
    [
        [0.001, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.001, 0.0],
        [0.0, -0.001, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--source-repository", required=True)
    parser.add_argument("--device-slug", required=True)
    parser.add_argument("--chassis-variant", required=True)
    parser.add_argument("--device-registry", type=Path, required=True)
    parser.add_argument("--layout-record", type=Path, required=True)
    parser.add_argument("--device-model-source", type=Path, required=True)
    parser.add_argument("--device-model-url", required=True)
    parser.add_argument("--device-model-commit", required=True)
    parser.add_argument("--device-model-sha256", required=True)
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Refuse publication from a dirty source tree.",
    )
    return parser.parse_args()


def git(repository_root: Path, *arguments: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository_root), *arguments],
        text=True,
    ).strip()


def rgba(hex_color: str, alpha: float) -> list[int]:
    color = hex_color.removeprefix("#")
    return [
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:6], 16),
        round(alpha * 255),
    ]


def load_layer(path: Path, layer_name: str) -> trimesh.Trimesh:
    loaded = trimesh.load(path, force="mesh", process=False)
    if not isinstance(loaded, trimesh.Trimesh):
        raise TypeError(f"{path} did not load as one mesh")
    if loaded.is_empty or len(loaded.faces) == 0:
        raise ValueError(f"{path} is empty")
    loaded.metadata["name"] = layer_name
    loaded.apply_transform(OPENSCAD_TO_GLTF)
    return loaded


def main() -> None:
    arguments = parse_args()
    repository_root = arguments.repository_root.resolve()
    revision = git(repository_root, "rev-parse", "HEAD")
    dirty = bool(git(repository_root, "status", "--porcelain"))
    if arguments.require_clean and dirty:
        raise SystemExit("refusing to publish handbook model from a dirty worktree")
    scene_contract = load_scene_contract(arguments, repository_root)

    scene = trimesh.Scene()
    layer_digests: dict[str, str] = {}

    for layer_name, material_fields in LAYER_MATERIALS.items():
        layer_path = arguments.layers / f"{layer_name}.stl"
        if not layer_path.is_file():
            raise FileNotFoundError(layer_path)
        material_name, color, metallic, roughness, alpha = material_fields
        mesh = load_layer(layer_path, layer_name)
        mesh.visual.material = PBRMaterial(
            name=material_name,
            baseColorFactor=rgba(color, alpha),
            metallicFactor=metallic,
            roughnessFactor=roughness,
            alphaMode="BLEND" if alpha < 1.0 else "OPAQUE",
            doubleSided=alpha < 1.0,
        )
        scene.add_geometry(
            mesh,
            node_name=layer_name,
            geom_name=layer_name,
        )
        layer_digests[layer_name] = digest(layer_path)

    extents = scene.extents
    if len(scene.geometry) != len(LAYER_MATERIALS):
        raise ValueError("semantic layer count changed during scene assembly")
    if np.any(extents < 0.05) or np.any(extents > 1.0):
        raise ValueError(f"implausible model extent in metres: {extents}")

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(scene.export(file_type="glb"))
    if arguments.output.read_bytes()[:4] != b"glTF":
        raise ValueError("exported file is not a binary glTF")

    round_trip = trimesh.load(arguments.output, force="scene", process=False)
    if len(round_trip.geometry) != len(LAYER_MATERIALS):
        raise ValueError(
            "round-trip semantic layer count mismatch: "
            f"{len(round_trip.geometry)} != {len(LAYER_MATERIALS)}"
        )
    round_trip_materials = {
        geometry.visual.material.name: list(
            geometry.visual.material.baseColorFactor
        )
        for geometry in round_trip.geometry.values()
    }
    expected_nameplate_materials = {
        "White nameplate body": rgba("#f5f5ed", 1.0),
        "Black raised labels": rgba("#050505", 1.0),
    }
    actual_nameplate_materials = {
        name: round_trip_materials.get(name)
        for name in expected_nameplate_materials
    }
    if actual_nameplate_materials != expected_nameplate_materials:
        raise ValueError(
            "round-trip nameplate material contract changed: "
            f"{actual_nameplate_materials!r}"
        )

    provenance = {
        "schema": 2,
        "source_repository": arguments.source_repository,
        "source_revision": revision,
        "source_dirty": dirty,
        "scene": scene_contract,
        "coordinate_transform": "OpenSCAD mm Z-up -> glTF m Y-up",
        "semantic_layers": list(LAYER_MATERIALS),
        "layer_sha256": layer_digests,
        "model_sha256": digest(arguments.output),
        "model_extents_metres": [round(float(value), 6) for value in extents],
    }
    arguments.provenance.parent.mkdir(parents=True, exist_ok=True)
    arguments.provenance.write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "handbook_model=pass "
        f"layers={len(LAYER_MATERIALS)} "
        f"device={scene_contract['device_slug']} "
        f"layout={scene_contract['layout_id']} "
        f"variant={scene_contract['chassis_variant']} "
        f"nameplate_materials={','.join(sorted(expected_nameplate_materials))!r} "
        f"sha256={provenance['model_sha256']} "
        f"dirty={str(dirty).lower()}"
    )


if __name__ == "__main__":
    main()
