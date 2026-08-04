# HiLetgo XL6009 boost-module model provenance

## Identity and fit contract

This source-native model represents the exact **HiLetgo 5-piece XL6009
adjustable boost module** supplied by the owner:

- Amazon listing: <https://www.amazon.com/dp/B07BNHR4HW>
- ASIN: `B07BNHR4HW`
- item model number: `5841863421`
- manufacturer part number: `3-01-0101-5pcs`
- PCB silkscreen visible in the listing: `Flying-Fish-XL6009`
- retrieval date: **2026-07-26**

Amazon's prose says `47 x 22 x 13 mm`, but the listing's underside dimension
image labels the exact photographed board **43 × 21 mm**. The independent
XL6009 module manual also specifies **43 × 21 × 14 mm**. The owner's physical
fixture measurement is more precise and governs installed fit:

- PCB: **43.16 × 21.23 × 1.60 mm**
- mounting holes: two diagonal **Ø3.00 mm** bores
- hole centres from the PCB's input/lower-left datum:
  `[6.50, 18.63]` and `[36.66, 2.20]` mm
- installed orientation: `IN+/IN-` on **−X**, `OUT+/OUT-` on **+X**
- populated height: **14.00 mm**

The listing shows a blue PCB, two bare-aluminum electrolytic capacitors
(`220 35V` input and `100 50V` output), a black shielded inductor marked
`470` (47 µH), XL6009E1 TO-263-5L regulator, black Schottky diode, blue
`W103` multi-turn trimmer with brass adjustment screw, four large edge pads,
and diagonal plated mounting holes.

## Preserved listing evidence

Original gallery files are retained outside Git at
`/home/matt/Downloads/pocketforge-reference/hiletgo/xl6009/B07BNHR4HW/`.
The directory also contains `SOURCES.txt` with the direct media URLs.

| Saved file | SHA-256 |
|---|---|
| `81iGekOWO4L.jpg` | `128d0d2eac3f0d467e77d895d95eb716cdc16737294c689b6d9f0a57f89b3284` |
| `51g934uVQKL.jpg` | `8e3bbb3f2574791934125bccb5e9eebb58c305b13221193663ea1b2e7c9d59fe` |
| `41vES5ouMCL.jpg` | `b732c09a83b410baa0c3dacdc93e89242b72f9a3475b363561ad66b1de0728c5` |
| `51YeMTx3otL.jpg` | `4027c0a0f5677449a640507069633a8299516dff8770f56ad484b8fb3ee45e52` |
| `51niq4vKERL.jpg` | `53aa07b5b5a19d188791895feee68050200ffec113aa7e6bb2c0419c497a2d4b` |
| `31Nwgc2EDRL.jpg` | `a8e3ed25bdf7ea3ad12680c2d82edb058a8e58260575a6e261d57410987c6dd0` |

The most useful reconstruction views are:

- `51YeMTx3otL.jpg`: orthographic top population, labels, and IN/OUT polarity;
- `51niq4vKERL.jpg`: underside, diagonal holes, `DC-DC XL6009E1` marking,
  and 43 × 21 mm dimension annotation;
- `81iGekOWO4L.jpg`: high-resolution oblique component form/material view.

## Authoritative component reference

The XLSEMI XL6009 Rev 1.1 datasheet was consulted for the XL6009E1 identity,
TO-263-5L package, five-lead geometry, and 400 kHz/4 A device markings:

<https://xlsemi.pl/sklep/files/datasheet_XL6009.pdf>

The 43 × 21 × 14 mm assembled-module dimensions were independently
cross-checked against:

<https://www.aneindia.com/wp-content/uploads/2014/10/XL6009-Manual.pdf>

These documents are references only and are not redistributed.

## Online-model search and clean-room decision

The following candidates were reviewed on 2026-07-26:

1. **3D ContentCentral `XL6009/LM2577`**, user-library part
   `aEMmixele_k_12000`, contributor shown as `ElectronicMaker`, modified
   2022-01-02. It visually targets a similar Amazon module, but download
   requires login and the page provides no explicit permissive redistribution
   license for embedding the geometry in this repository.
2. **3D ContentCentral `EVAL BOARD FOR XL6009`**, contributor Brian Dean.
   It is an evaluation-board entry rather than evidence of the exact
   `Flying-Fish-XL6009` population; download likewise requires login and no
   explicit repository-redistribution license is stated.
3. **Thingiverse/CN6009-XL6009 community model** indexed by STLFinder/3DGo,
   attributed to `OkurRo`. The indexed copy did not expose a dependable
   license/source download or prove the exact HiLetgo PCB revision and
   measured diagonal-hole registration.
4. **Hackaday.io DC-DC Boost Converter Module**, author `mbsg99`. Its PCB and
   3D screenshots are a different custom design, not this board revision.

No candidate simultaneously proved exact revision, measured fit, and
redistribution permission. Therefore no third-party mesh or EDA geometry was
imported.

## Redistribution statement

`hiletgo-xl6009.scad` is an original repository-native reconstruction from
the dimensional contract, listing views, and component-package facts.
No Amazon image, HiLetgo artwork, third-party mesh, STEP body, or EDA file is
stored in Git. Product names and compact markings identify the physical part
in an assembly view; listing images remain external evidence only.
