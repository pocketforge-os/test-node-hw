# Ceksezx MTSD001 MOSFET-module model provenance

## Identity and dimensional contract

This source-native model represents the exact **Ceksezx MTSD001 dual
high-power MOSFET trigger switch drive module** supplied by the owner:

- Amazon listing: <https://www.amazon.com/dp/B0FMJH3DML>
- ASIN: `B0FMJH3DML`
- listing model and part number: `MTSD001`
- manufacturer/brand: `Ceksezx`
- retrieval date: **2026-07-26**

The listing specifies **1.34 × 0.67 × 0.47 in**, or approximately
**34 × 17 × 12 mm**. The actual module is also visible in the owner's
2026-07-18 fixture photograph. The annotated fixture sketch establishes two
**Ø2.2 mm** mounting holes with **15.58 mm far-edge spacing**, which converts
to **13.38 mm centre spacing**.

The original fixture used a deliberately provisional 35 × 18 mm analytical
envelope. The exact 34 × 17 mm PCB is centred within that envelope and rotated
180 degrees, preserving both existing printed standoff centres. Its two clipped
control-edge holes therefore align without changing the production fixture.
The installed orientation follows the owner photograph:

- blue four-position power/load terminal bank: **−X**
- J1 PWM/ground control pads and two mounting holes: **+X**
- populated face: **+Z**

## Preserved product evidence

Reference files are retained outside Git at
`/home/matt/Downloads/pocketforge-reference/ceksezx/mtsd001/B0FMJH3DML/`.
That directory's `SOURCES.txt` records every source URL, retrieval note, and
immutable hash.

| Saved file | Role | SHA-256 |
|---|---|---|
| `5184uNdVRhL.jpg` | Amazon-hosted exact listing hero | `42a2bc3a51587a51649d885db1ae87d65b1166c204ddd6e5e669cb8f76c5fd69` |
| `ebay-mirror-view-4.webp` | exact same-listing dimensional view | `6706f3e1594e2b63a8366370717503e2b09ffabacd3650f80048e746d8538fc7` |
| `onbuy-view-1.png` | higher-resolution exact-population top/oblique view | `947402fc50dbccf73f501b1b5a69acdfd32ac4df02736e8290030fb5016197a3` |
| `/home/matt/Downloads/20260718_233317.jpg` | owner's photograph of the actual module | `cf2419bc0a5a33edcec808d35592dc417749536ee2e8cc67885f74a656c9e2a6` |
| `/home/matt/Downloads/20260718_233729.jpg` | owner's annotated mounting sketch | `21c898ad240c23d2bb120cad9bfc16d6e9410fb80a551e3eb4f354313f743eaa` |

Amazon exposed its hero through the media CDN. The remaining seven exact
gallery views were retained from an eBay mirror of the same MTSD001 listing;
six 990 px corroborating views of the same board revision were retained from
OnBuy. Their URLs and hashes are recorded in `SOURCES.txt`.

The preserved views establish the blue PCB, two pairs of blue screw-terminal
cells, four plated screws, dual `PD4184`/AOD4184-class DPAK MOSFETs, six-hole
J1 control footprint, indicator LED, gate-network passives, clipped mounting
holes, and visible `R1`/`R2`/`R3`, `Q1`/`Q2`, `J1`, `LED`, PWM/GND, load, and
power markings.

## Online-model search and clean-room decision

Searches on 2026-07-26 covered Ceksezx/MTSD001 and XY-MOS product results,
general STEP/STL/CAD queries for the 34 × 17 mm dual-MOSFET module,
GrabCAD-indexed results, GitHub code and repository search,
Printables/Thingiverse-indexed results, and electronics seller/manufacturer
pages. No downloadable model was found that simultaneously:

1. matched the exact MTSD001 PCB population and clipped-hole revision;
2. preserved the owner's measured mounting datums; and
3. carried an explicit license permitting repository redistribution.

No third-party geometry was imported. `ceksezx-mtsd001.scad` is an original
repository-native reconstruction from the measured fit contract, preserved
listing gallery, and owner photograph.

## Redistribution statement

No Amazon image, Ceksezx artwork, third-party mesh, STEP body, or EDA file is
stored in Git. Compact product and component markings identify the physical
board in the assembly view; the original reference evidence remains outside
the repository.
