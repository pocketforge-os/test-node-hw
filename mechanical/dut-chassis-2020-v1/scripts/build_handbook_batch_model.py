#!/usr/bin/env python3
"""Convert canonical OpenSCAD print-bed meshes into an interactive GLB."""

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
    parser.add_argument("--input", type=Path)
    parser.add_argument(
        "--layer",
        action="append",
        default=[],
        metavar="PATH::NAME::HEX",
        help="add a named, colored mesh layer (repeat for multi-material beds)",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", required=True)
    arguments = parser.parse_args()
    if bool(arguments.input) == bool(arguments.layer):
        parser.error("provide exactly one of --input or one or more --layer values")
    return arguments


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rgba(hex_color: str) -> list[int]:
    color = hex_color.removeprefix("#")
    if len(color) != 6:
        raise ValueError(f"expected a six-digit RGB color, got {hex_color!r}")
    return [
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:6], 16),
        255,
    ]


def parse_layers(arguments: argparse.Namespace) -> list[tuple[Path, str, str]]:
    if arguments.input:
        return [
            (
                arguments.input,
                arguments.name,
                "#e96a0a",
            )
        ]

    layers: list[tuple[Path, str, str]] = []
    for specification in arguments.layer:
        fields = specification.rsplit("::", 2)
        if len(fields) != 3 or not all(fields):
            raise ValueError(
                f"invalid --layer {specification!r}; expected PATH::NAME::HEX"
            )
        layers.append((Path(fields[0]), fields[1], fields[2]))
    return layers


def main() -> None:
    arguments = parse_args()
    layers = parse_layers(arguments)
    scene = trimesh.Scene()
    source_digests = []
    for source_path, layer_name, color in layers:
        source = source_path.resolve()
        if not source.is_file():
            raise FileNotFoundError(source)

        mesh = trimesh.load(source, force="mesh", process=True)
        if not isinstance(mesh, trimesh.Trimesh):
            raise TypeError(f"{source} did not load as one mesh")
        if mesh.is_empty or len(mesh.faces) == 0:
            raise ValueError(f"{source} is empty")
        if np.any(mesh.extents <= 0.0) or np.any(mesh.extents > 247.1):
            raise ValueError(
                f"implausible canonical-bed extent in millimetres: {mesh.extents}"
            )

        mesh.apply_transform(OPENSCAD_TO_GLTF)
        mesh.metadata["name"] = layer_name
        mesh.visual.material = PBRMaterial(
            name=layer_name,
            baseColorFactor=rgba(color),
            metallicFactor=0.0,
            roughnessFactor=0.48,
        )
        scene.add_geometry(
            mesh,
            node_name=layer_name,
            geom_name=layer_name,
        )
        source_digests.append(f"{source.name}:{digest(source)}")

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(scene.export(file_type="glb"))
    if arguments.output.read_bytes()[:4] != b"glTF":
        raise ValueError("exported file is not a binary glTF")

    round_trip = trimesh.load(arguments.output, force="scene", process=False)
    if len(round_trip.geometry) != len(layers):
        raise ValueError(
            "round-trip geometry count changed: "
            f"{len(round_trip.geometry)} != {len(layers)}"
        )
    material_names = {
        geometry.visual.material.name for geometry in round_trip.geometry.values()
    }
    if len(material_names) != len(layers):
        raise ValueError(
            "round-trip material count changed: "
            f"{len(material_names)} != {len(layers)}"
        )

    print(
        "handbook_batch_model=pass "
        f"name={arguments.name!r} "
        f"layers={len(layers)} "
        f"materials={','.join(sorted(material_names))!r} "
        f"source_sha256={','.join(source_digests)!r} "
        f"glb_sha256={digest(arguments.output)}"
    )


if __name__ == "__main__":
    main()
