# ELEGOO four-channel relay model provenance

The PocketForge relay-board assembly is an original, repository-native
OpenSCAD reconstruction. No Amazon image, ELEGOO artwork, EDA file, or
third-party mesh is committed or embedded in the model.

## Installed identity and dimensional authority

- Product: ELEGOO 4 Channel DC 5V Relay Module with Optocoupler.
- Owner-supplied listing: `https://www.amazon.com/dp/B09ZQS2JRD`.
- Amazon ASIN: `B09ZQS2JRD`.
- Amazon item model: `US-EL-SM-Relay`.
- Board population: four 5 V active-low channels, four blue
  `SRD-05VDC-SL-C`-style relay cans, twelve NO/COM/NC screw terminals, four
  optocouplers, individual status LEDs, a six-pin MCU header, and a separate
  `JD-VCC` / `VCC` power header with blue shunt.
- The physically fitted board is authoritative at **72.70 × 51.85 mm**,
  with four **Ø3.00 mm** holes on **66.93 × 45.03 mm** centres. In the
  fixture it is rotated to a **51.85 × 72.70 mm** installed envelope on the
  already accepted 26 mm standoffs.
- The installed screw-terminal bank faces fixture **+X**, preserving the
  actual cable-access side and the clearance created when the board was moved
  10 mm left during the physical-fit revision.

Amazon's description claims **134 × 52 × 17 mm**, 129.2 × 46.7 mm upper-hole
centres, and 128.5 × 46.7 mm lower-hole centres. Those values cannot describe
this four-channel board: 134 mm exceeds Amazon's own 3.35 inch (85.09 mm)
package length and matches the proportions of an eight-channel relay board.
They are recorded as listing contamination and are not used for geometry.

## Saved listing evidence

Retrieved 2026-07-25 from Amazon's public media host and preserved outside Git
under:

`/home/matt/Downloads/pocketforge-reference/elegoo/4-channel-relay/B09ZQS2JRD/`

The files remain reference-only listing artwork. The committed model contains
only clean-room geometry reconstructed from observation.

| File | Pixels | SHA-256 |
| --- | ---: | --- |
| `01-main.jpg` | 500 × 500 | `a8a405e23244346ee17a98e7b317e86a2b809719e8304e413bd249308405f144` |
| `02-listing.jpg` | 500 × 500 | `ed50ffe30a407e7f38ffc79e682aba315e0d492ab6087dbbffc12067229fea5b` |
| `03-listing.jpg` | 500 × 500 | `f4dba8f2eafba5a8904e19967d4aa012721cb1e60f5a81d5d4799f7680af92c0` |
| `04-listing.jpg` | 500 × 500 | `11a3944b3743db5f81682fffdb0b549fc102793de9d42a8fe96a76b1459516a2` |
| `05-listing.jpg` | 500 × 500 | `98ed7f23fd39566becd44e3c8265f526f8a7f64aa53c32bbc95281e68f30d74f` |
| `06-listing.jpg` | 500 × 500 | `1acdba553997f93c1b709f94c2ee24c487a7a9b151add1fd5f5c0079d9417521` |
| `07-aplus.jpg` | 970 × 600 | `e3c15bd71d92c9b5b03d02ec7e6ff56038e4f7f723709004b4152b6d78eeeefa` |

The gallery establishes the exact blue board revision and its component order:
terminal bank, four adjacent relay cans, four-channel optocoupler/driver row,
red status LEDs, MCU input header, separate relay-power header/shunt, corner
mounting holes, and visible white labels.

ELEGOO's public product page independently identifies the selectable
four-channel 5 V variant:

`https://www.elegoo.com/en-gb/collections/elegoo-product-ex-s3-s4-m5/products/elegoo-8-channel-relay-module-kit`

## Online CAD candidates evaluated

1. **NamorIt, “Arduino 4 channels relay module,” Thingiverse 4011184**,
   published 2019-12-01 under CC BY 4.0:
   `https://www.thingiverse.com/thing:4011184`. Its saved preview hashes to
   `d967bb2e60d35e36d019f55ab48bb20e838cf1b8e9ab65933090c9585f16ca67`.
   It is a different red PCB with a 3 × 3 high/low header, a screw-terminal
   arrangement on the opposite side, no four-PC817 row, and different
   mounting registration. It was rejected and no geometry is redistributed.
2. GrabCAD search results named **“4 Channel Relay Module”** and
   **“4 Channel Relay Module - 5v No Name”** show per-channel high/low
   jumpers or differently populated generic boards. Neither establishes the
   ELEGOO listing revision or repository-redistribution terms; neither was
   downloaded or imported.
3. Thingiverse, Printables, and MyMiniFactory results provide cases and DIN
   mounts for nominal 72 × 52 mm relay modules. Those confirm the common
   board envelope but contain enclosure geometry, not an accurate populated
   ELEGOO assembly.

No complete exact board model with compatible source and clear redistribution
terms was found.

## Reconstruction and uncertainty

- Physical outline, hole diameter, mounting registration, fixture origin,
  standoff height, and installed orientation are exact fit datums.
- Relay-can and 5.08 mm terminal pitch use standard package envelopes;
  component positions are proportioned from the listing's top and oblique
  views. Small passive packages are presentation geometry and make no claim
  about hidden traces or electrical connectivity.
- Material-specific exports keep PCB, blue electromechanical bodies, dark
  semiconductors/header plastic, metal terminals/pins, red indicators, and
  pale markings independently inspectable in the handbook model.
- Source parameters remain readable in `elegoo-4-channel-relay.scad` so a
  future owner caliper pass can refine individual component offsets without
  replacing the exact mounting contract or importing opaque geometry.
