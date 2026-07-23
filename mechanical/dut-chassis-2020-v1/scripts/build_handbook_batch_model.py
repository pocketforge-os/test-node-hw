#!/usr/bin/env python3
"""Convert one canonical OpenSCAD print-bed STL into an interactive GLB."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial


# OpenSCAD is right-handed Z-up in millimetres. glTF is right-handed Y-up in
# metres. Keep the print bed horizontal after mapping (x, y, z) -> (x, z, -y).
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
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", required=True)
    return parser.parse_args()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    arguments = parse_args()
    source = arguments.input.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    mesh = trimesh.load(source, force="mesh", process=True)
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError(f"{source} did not load as one mesh")
    if mesh.is_empty or len(mesh.faces) == 0:
        raise ValueError(f"{source} is empty")
    if np.any(mesh.extents <= 0.0) or np.any(mesh.extents > 247.1):
        raise ValueError(f"implausible canonical-bed extent in millimetres: {mesh.extents}")

    mesh.apply_transform(OPENSCAD_TO_GLTF)
    mesh.metadata["name"] = arguments.name
    mesh.visual.material = PBRMaterial(
        name="PocketForge printed ABS",
        baseColorFactor=[233, 106, 10, 255],
        metallicFactor=0.0,
        roughnessFactor=0.48,
    )

    scene = trimesh.Scene()
    scene.add_geometry(
        mesh,
        node_name=arguments.name,
        geom_name=arguments.name,
    )

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(scene.export(file_type="glb"))
    if arguments.output.read_bytes()[:4] != b"glTF":
        raise ValueError("exported file is not a binary glTF")

    round_trip = trimesh.load(arguments.output, force="scene", process=False)
    if len(round_trip.geometry) != 1:
        raise ValueError(
            f"round-trip geometry count changed: {len(round_trip.geometry)} != 1"
        )

    print(
        "handbook_batch_model=pass "
        f"name={arguments.name!r} "
        f"source_sha256={digest(source)} "
        f"glb_sha256={digest(arguments.output)}"
    )


if __name__ == "__main__":
    main()
