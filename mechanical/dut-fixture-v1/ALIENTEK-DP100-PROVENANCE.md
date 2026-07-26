# ALIENTEK DP100 model provenance

## Identity and dimensional contract

This source-native model represents the exact **ALIENTEK DP100 compact
programmable DC power supply** supplied by the owner:

- Amazon listing: <https://www.amazon.com/dp/B0CWRG6YFM>
- ASIN: `B0CWRG6YFM`
- listing model: `DP100-1`
- item model number: `DP100`
- manufacturer: `ALIENTEK`
- retrieval date: **2026-07-26**

The Amazon listing and ALIENTEK manual specify **100.4 × 62.2 × 17.2 mm** and
95 g. The owner's fixture measurement establishes the enclosure itself as
**94.6 × 62.2 × 17.2 mm**. These are not competing scales: the model preserves
the measured 94.6 mm installed enclosure and adds the photographed **5.8 mm**
banana-interface projection on its −X edge, producing the official **100.4 mm**
overall length.

The installed orientation follows the manual's numbered appearance diagram:

- black negative and red positive 4 mm banana outputs: **−X**
- USB-C power input and USB-A communications interface: **+X**
- 0.96-inch IPS screen, three buttons, and adjustment wheel: **−Y**

The fixture origin, two opposite-side tie slots, and 94.6 × 62.2 mm collision
envelope remain unchanged.

## Preserved product evidence

Reference files are retained outside Git at
`/home/matt/Downloads/pocketforge-reference/alientek/dp100/B0CWRG6YFM/`.
That directory also contains `SOURCES.txt` with the source URLs and retrieval
notes.

| Saved file | Role | SHA-256 |
|---|---|---|
| `41UAh4KNqfL.jpg` | Amazon listing hero | `d1cc4a01bcb721d4008ab76b5ed69d7946b5a39c68044a902c942d604a63ae0f` |
| `DP100-user-manual.pdf` | authoritative dimensions and interface diagram | `8878f9aa3be219964c41ad3a4e679526bea54946a262fc61f35ed965d7e5f97b` |
| `DP100-manual-appearance.png` | derived page-5 appearance-diagram render | `b159077910e492e4b89ae799d4b1a33a58099f083935db80fc7cc7690488ad0f` |

The listing hero was obtained from Amazon's media CDN after the product page
served a CAPTCHA. Its association with ASIN `B0CWRG6YFM` was independently
corroborated by the listing mirror at
<https://uk.findthedeal.org/p/B0CWRG6YFM/>.

The authoritative English manual is retained from:
<https://ae01.alicdn.com/kf/Sb2c89a7846a64031bba328366a77ffe9K.pdf>.
The same dimensional and interface facts were cross-checked against the
Switch Science and Eleshop DP100 catalog pages.

## Online-model search and clean-room decision

Searches on 2026-07-26 covered the ALIENTEK product site, general web results,
GrabCAD, Printables, Thingiverse-indexed results, STEP/CAD queries, and
electronics distributor pages. Results exposed product photographs, reviews,
the user manual, and unrelated parts named “DP100,” but no downloadable model
that simultaneously:

1. proved the exact ALIENTEK DP100 enclosure revision and interface layout;
2. matched the 94.6 mm measured installed enclosure datum; and
3. carried an explicit license permitting repository redistribution.

No third-party geometry was imported. `alientek-dp100.scad` is an original
repository-native reconstruction from the measured fit contract, official
manual dimensions/interface diagram, and the preserved listing view.

## Redistribution statement

No Amazon image, ALIENTEK artwork, manual page, third-party mesh, STEP body,
or EDA file is stored in Git. Product names and compact markings identify the
physical component in an assembly view; the original reference evidence
remains outside the repository.
