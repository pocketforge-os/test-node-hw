# Symbols & footprints

Project library for the specialized parts, so Ian isn't hunting symbols/footprints. Jellybeans
(R/C/L/diodes/generic connectors) come from KiCad's stock libraries; the parts below are pulled from
LCSC/EasyEDA (which is also what JLCPCB assembles from, so the footprints match the assembly house).

## Library files
- `test-node.kicad_sym` — symbols
- `test-node.pretty/` — footprints (`.kicad_mod`)
- `test-node.3dshapes/` — 3D models (.wrl/.step)

Add to a KiCad project via **Preferences → Manage Symbol/Footprint Libraries → add** `test-node.kicad_sym`
and `test-node.pretty` (project-scoped is fine).

## How to pull a part (the proven flow)
```
uv run --with easyeda2kicad easyeda2kicad --full --lcsc_id=<Cxxxxxx> --output lib/test-node
```
(`easyeda2kicad` v1.0.1; `--full` = symbol + footprint + 3D. Appends to the existing library.)

## Parts pulled so far ✅
| part | LCSC | in lib |
|---|---|---|
| TS3A27518EPWR (SD analog mux) | C443721 | ✅ |
| GL823K-HCY04 (USB SD reader) | C284879 | ✅ |
| AO3400A (N-FET: LED switch / sink-clamp) | C20917 | ✅ |

## Still to pull — confirm the LCSC C-number from `docs/03-BOM.md`, then run the command above
| part | note |
|---|---|
| **LTC3649** (buck) | ADI part — **may not be on LCSC** (thin stock). If `easyeda2kicad` fails, pull the symbol/footprint from SnapEDA / Ultra Librarian / the ADI model, or draw from the datasheet. Confirm fleet sourcing (DigiKey). |
| MCP4728 (DAC) | on LCSC — get the C# |
| INA226 (telemetry) | on LCSC — get the C# |
| TL431 (OVP ref) | jellybean-ish; LCSC C# |
| ESP32-S3-WROOM-1-N16R8 | on LCSC — get the C# (module footprint) |
| Molex Micro-Fit 3.0 5-ckt (power) | LCSC C# or KiCad `Connector_Molex` lib |
| JST-GH 1.25 8-pin (signal) | LCSC C# or KiCad `Connector_JST` lib |
| microSD push-push socket | LCSC C# |
| MP1584 (5 V buck), 3.3 V buck | from the BOM |
| **protection parts** (crowbar SCR, B+ fuse, cell-node TVS, 12 V TVS, rev-pol P-FET, ferrite) | C-numbers land in `docs/03-BOM.md` (being finalized) → pull each |

> Tip: verify each pulled part's footprint pin-count/pitch against the datasheet before trusting it —
> community LCSC footprints are usually right but not guaranteed.
