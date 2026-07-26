# Smays microb-hub-8152 model provenance

`smays-microb-hub-8152.scad` is an original PocketForge reconstruction of the
white top-facing powered USB/Ethernet hub installed on the fixture. No listing
image or third-party geometry is redistributed.

## Identity, dimensions, and installed pose

- Owner-supplied listing: <https://www.amazon.com/dp/B00L32UUJK>
- Brand/model: Smays microb-hub-8152 /
  SMAYS-ETHERNET-ADAPTOR-HUB, UPC 522014547314
- Interfaces: three USB 2.0 Type-A receptacles, 10/100 RJ45, 3.5 mm 5 V DC
  input, and a fixed 250 mm micro-USB OTG lead
- Catalog metadata varies between 4.1 × 0.83 × 0.59 in and
  3.74 × 0.83 × 0.59 in. The listing appearance diagram shows approximately
  4.1 × 0.9 × 0.7 in. The owner-fit 105.07 × 24 mm footprint controls X/Y;
  the populated body height remains 15 mm.
- Installed orientation: USB bank +Y/top, RJ45 −X/left, OTG lead +X/right,
  and DC input −Y/bottom

The owner photograph proves why the apparently inverted pairing is necessary:
the DC plug leaves the Smays hub into the six-millimetre body gap, rises away
from the plate, and crosses above the thinner VIENON hub. The model and
validation encode that three-dimensional arch instead of pretending a flat
unused corridor exists.

## Preserved references

The Amazon gallery and owner photo were saved outside git under
`/home/matt/Downloads/pocketforge-reference/final-fixture-components/` on
2026-07-26. The root `SOURCES.txt` records every file and hash. Key files are:

- Amazon hero: `31pH9HNN7dL.jpg`,
  SHA-256 `c5600a55adcf666a92c37a2af2c99cc611d47b4fa8738257b04a655e0b69478f`
- Amazon dimension/interface view: `419ZJLQOkGL.jpg`,
  SHA-256 `35268f4c3e4f45a74d5b010440570d1ead0b20dd9a472ae11d9cfb2a803fb16`
- Owner installed-state photograph:
  `owner/20260726-installed-usb-hubs.png`,
  SHA-256 `01ecb407d5862a442ac77eb52c60763db44b5067d2c55e2e0d08fc6aed7d51e5`

## Geometry and license decision

Exact ASIN, UPC, model-number, STEP, STL, and CAD searches found no matching
model with a redistribution license. The source reconstructs the chamfered
white shell, three USB sockets and LEDs, RJ45 shield/contacts, DC jack,
branding, OTG lead, and the installed DC plug/cable arch. Reference photos
remain evidence only and are not committed.

Searches used `B00L32UUJK`, `522014547314`, `microb-hub-8152`,
`SMAYS-ETHERNET-ADAPTOR-HUB`, and their combinations with `STEP`, `STL`,
`CAD`, and `3D model` across general search and public CAD-model indexes. No
exact geometry candidate was found, so there is no third-party author or
license to carry forward; generic USB/Ethernet dongles were rejected because
their port population and DC-input placement did not establish a match.
