# ACEIRMC ESP32-S3 SuperMini model provenance

## Installed identity

- Seller/brand: ACEIRMC
- Listing: `10pcs Type-C Supermini ESP32-S3 Development Board`
- ASIN: `B0GS1X97DZ`
- PCB reverse marking: `HW-747 V0.0.2`
- SoC marking: `ESP32-S3FH4R2`
- Listing URL: `https://www.amazon.com/dp/B0GS1X97DZ`
- Listing retrieved: 2026-07-26

The listing calls the board 22.52 × 18 mm in prose and 23 × 18 mm in its
dimension image. PocketForge's physical unit was previously measured with
calipers at **23.67 × 18.50 mm overall**, so the physical measurement remains
the model and fixture authority. The listing establishes board population,
component registration, markings, and nominal cross-checks.

## Saved listing references

The owner explicitly asked that the listing images be saved. Original response
assets were preserved outside the distributable Git repository at:

`~/Downloads/pocketforge-reference/amazon/B0GS1X97DZ/`

They remain reference-only Amazon listing artwork and are not licensed or
redistributed as project assets. The committed model contains only original
OpenSCAD geometry reconstructed from observation.

| File | Pixels | SHA-256 |
| --- | ---: | --- |
| `01-main.jpg` | 1600 × 1600 | `71e35b41584fda9bfad5da9fd9d21c9369f75a2d6a522343e97bd4de5327ae1d` |
| `02-board-pair.jpg` | 500 × 500 | `d055c0a9555d41fdb1e3991c02a4f2aa1fa695194dfd6f2b694c33e32f831a04` |
| `03-pinout.jpg` | 500 × 500 | `d3b34fc9af4196a305441624ef9471a723c32ba777146fb29e57753b5d20377f` |
| `04-dimensions.jpg` | 500 × 500 | `83c7af3f095bba54606d207fa7db47dd6e496a2e014671a7a82a59cac34086a5` |
| `05-features.jpg` | 500 × 500 | `b8d14134d6bde2fe4c3cb0a4fe4d23c9f57617a4ce327f0968898def079ff25b` |
| `06-specification.jpg` | 500 × 500 | `78169aedb1c8cb65dc34d0d5d616e967533f362c73969e3abbf281e3cc925ad4` |
| `07-package.jpg` | 500 × 500 | `9e0101a11f93bf4bec831c9c2caca495537ba2a86ecbc3e96b2ba5adfd3c04ad` |

## Cross-checks and limits

- Amazon's photos expose the populated top, reverse PCB artwork, nominal
  dimensions, 18 plated edge holes, USB-C receptacle, dual buttons, red ceramic
  antenna, and identifying package/revision markings.
- Espressif's ESP32-S3 documentation establishes the 7 × 7 mm QFN package
  envelope used for the recognizable central IC.
- Public community KiCad footprints were checked only as independent outline
  and 2.54 mm pad-pitch cross-checks. No footprint geometry is copied.
- Searches of GitHub and the public web did not find an authoritative HW-747
  V0.0.2 board schematic or an exact populated assembly with a suitable license.
  The model therefore makes no claim about hidden copper or electrical
  connectivity.

Reference URLs:

- `https://www.amazon.com/dp/B0GS1X97DZ`
- `https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf`
- `https://github.com/smkent/pcb/blob/main/libraries/module.pretty/ESP32-S3-Super-Mini-Castellated-SMD.kicad_mod`

## Clean-room model policy

`esp32-s3-supermini-hw747-v0.0.2.scad` is an original repository-native
reconstruction. The owner-measured physical envelope is exact; small passive
component envelopes and registration are photo-derived presentation geometry.
No external mesh, EDA artwork, Amazon image, or unlicensed schematic is
embedded in distributable outputs.
