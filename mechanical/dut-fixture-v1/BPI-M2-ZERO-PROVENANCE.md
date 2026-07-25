# Banana Pi BPI-M2 Zero V1.0 model provenance

The presentation model in `bpi-m2-zero-v1.scad` is an original PocketForge
reconstruction of the populated board installed on `pf-node-01`. It embeds no
third-party mesh, DXF, image, or PCB artwork.

## Runtime identity

A read-only, fail-fast SSH query against the fixture node on 2026-07-25
reported:

```text
hostname=pf-node-01
device_tree_model=Banana Pi BPI-M2-Zero
architecture=armv7l
BOARD=bananapim2zero
BOARD_NAME="Banana Pi M2 Zero"
```

The physical revision is cross-checked against the manufacturer's V1.0 artwork
and the `BPi-M2-ZERO-V1.0` silkscreen documented by linux-sunxi. Runtime
firmware cannot expose the PCB's printed revision, so the model does not claim
that SSH supplied a serial number or board revision.

## Measurement and population evidence

- Owner fixture photograph: `/home/matt/Downloads/20260718_233317.jpg`,
  captured 2026-07-18. It establishes the installed top-side population:
  blue PCB, Allwinner H2+, K016 radio shield, populated 2x20 header, u.FL,
  mini-HDMI, two micro-USB receptacles, and CSI connector.
- Owner caliper-note photographs:
  `/home/matt/Downloads/20260718_233626.jpg` and
  `/home/matt/Downloads/20260718_233729.jpg`.
- Measured board interface: 29.90 x 65.00 mm, 2.60 mm mounting holes,
  and 23.00 x 58.36 mm hole-centre spacing.

The local photo paths document the controlled measurement input; the images are
not redistributed by this repository.

## Manufacturer reference

Sinovoip's official BPI forum publishes the exact BPI-M2 Zero V1.0 top/bottom
DXF archive:

`https://forum.banana-pi.org/t/bpi-m2-zero-dxf-file-public/4110`

Downloaded Google Drive archive:

```text
sha256  5d1a7181bb9c930ae39b7f6583a45479cd10171ace241bc1fdf8f8139e985ff0
bytes   38522
```

Extracted references:

```text
7adbb58ab77addc91a5fc2ee84df689e5db62e7ed2b9b2b12b166684b1632833  bpi-m2-zero-v1_0_DXF_top.dxf
9d0815fd9bdb3cb5dd790d8dda1eb132a36802b586dc5eab696c79cea3dc592a  bpi-m2-zero-v1_0_DXF_bot.dxf
```

The DXFs were used only to cross-check factual dimensions, connector
registration, and V1.0 labels. The archive contains no explicit redistribution
license, so it is deliberately not committed or converted into repository
geometry.

Additional identity/dimension references:

- `https://docs.banana-pi.org/en/BPI-M2_Zero/BananaPi_BPI-M2_Zero`
- `https://linux-sunxi.org/Sinovoip_Banana_Pi_M2_Zero`

## Online 3D-model search

The 2026-07-25 search covered the manufacturer's documentation/forum, GitHub
code and repositories, GrabCAD, Sketchfab, Printables, Thingiverse, Thangs,
and Cults. Results contained cases and mounting accessories, but no exact
BPI-M2 Zero V1.0 populated-board model with a license suitable for
redistribution. Consequently this source-native reconstruction is preferred
over importing a look-alike Raspberry Pi Zero model or an unlicensed mesh.
