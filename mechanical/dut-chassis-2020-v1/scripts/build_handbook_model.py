#!/usr/bin/env python3
"""Build the PocketForge handbook's semantic glTF model from OpenSCAD layers."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial


LAYER_MATERIALS = {
    "aluminum": ("Aluminum extrusion", "#a8afb8", 0.72, 0.28, 1.0),
    "connectors": ("Metal connectors", "#24282e", 0.78, 0.30, 1.0),
    "printed-hardware": ("Printed chassis hardware", "#e96a0a", 0.02, 0.48, 1.0),
    "fixture-plate": ("Fixture plate", "#d9dbd6", 0.0, 0.58, 1.0),
    "fixture-components": ("Fixture components", "#20384b", 0.02, 0.52, 1.0),
    "fixture-labels": ("Fixture labels", "#16794f", 0.0, 0.55, 1.0),
    "carrier-body": ("DUT carrier", "#e1e2dc", 0.0, 0.58, 1.0),
    "carrier-labels": ("Carrier labels", "#17191c", 0.0, 0.55, 1.0),
    "carrier-hooks": ("Carrier hooks", "#34383e", 0.0, 0.48, 1.0),
    "device-shell": ("DUT shell", "#22262b", 0.05, 0.42, 1.0),
    "device-controls": ("DUT controls", "#0f1114", 0.0, 0.38, 1.0),
    "device-screen": ("DUT screen", "#07161f", 0.08, 0.20, 1.0),
    "webcam": ("Webcam", "#1f394d", 0.0, 0.48, 1.0),
    "power-strip": ("Power strip", "#ecece7", 0.0, 0.62, 1.0),
    "placard-holder": ("Placard holder", "#17364f", 0.0, 0.48, 1.0),
    "placard-insert": ("Placard insert", "#d7a40b", 0.05, 0.42, 1.0),
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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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

    provenance = {
        "schema": 1,
        "source_repository": arguments.source_repository,
        "source_revision": revision,
        "source_dirty": dirty,
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
        f"sha256={provenance['model_sha256']} "
        f"dirty={str(dirty).lower()}"
    )


if __name__ == "__main__":
    main()
