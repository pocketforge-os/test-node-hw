# Parts list / BOM hints — known MPNs + what's TBD

Give these to flux so it uses real parts, not placeholders. `TBD` = let flux propose an in-stock MPN,
then upload that part's datasheet and have it re-verify pins. Prefer JLCPCB Basic/Preferred.

## Known / preferred parts
| function | part | MPN / LCSC | notes |
|---|---|---|---|
| Controller | ESP32-S3-WROOM-1-N16R8 | Espressif | 16MB/8MB, PCB antenna, castellated |
| Setpoint DAC | MCP4728 | Microchip MCP4728-E/UN | 12-bit quad I²C DAC, internal Vref → buck REF |
| Telemetry | INA226 | TI INA226AIDGSR | bidirectional V/I, 10 mΩ shunt, I²C, has ALERT |
| OVP reference | TL431 | TL431 (adjustable, tight tol) | own 2.5 V ref; sets ~4.6 V trip via divider |
| 5 V buck | MP1584EN | MPS MP1584EN | 12→5 V aux/servo rail |
| LED switch FET | AO3400A | AOS AO3400A (C20917) | SOT-23 logic-level N-FET, JLC Basic |
| USB SD reader | GL823K-HCY04 | Genesys GL823K-HCY04 (LCSC C284879) | SSOP-16, hand-solderable |
| SD analog mux | TS3A27518E | TI TS3A27518EPWR (C443721) | 6-ch bidir switch, ~50 MHz SI ceiling |
| Power button | Panasonic AQY PhotoMOS | e.g. AQY212 / AQY282 family | bidirectional MOSFET-output photorelay |
| Power connector | Molex Micro-Fit 3.0, 5-circuit | Molex 43045 / 43025 family | keyed + latched, ~5 A/ckt |
| Signal connector | JST-GH 1.25, 8-pin | JST GH SM08B-GHS / BM08B-GHS | keyed + LATCHED |
| Barrel jack | DC-005 2.1 mm | ≥3 A, center-positive | consider a locking/higher-current jack |

## Virtual-battery buck — DECIDED
| function | part | notes |
|---|---|---|
| **Virtual-battery buck** | **Analog Devices LTC3649** (LTC3649EUFD/EFE) | monolithic integrated-FET sync buck, Vin 3.1–60 V, 4 A. **Vout = V(ISET) unity gain** (drive ISET with the MCP4728 DAC). Forced-continuous (float MODE/SYNC) → sinks. DigiKey ~$16–19; thinner LCSC stock — confirm fleet sourcing. JLC-in-stock alt if needed: MPS **MPQ8633A** (C357781, ~$6.32; analog TRK/REF ×~3.1 divider, 12A/−5.5A sink, but 16 V Vin needs input clamp). |

## Other TBD (let flux propose in-stock MPNs, then verify against datasheet)
| function | requirement |
|---|---|
| **Buck inductor L1** | sized for ~3 A continuous, low DCR; corner with the post-filter |
| **Ferrite bead FB1** | ≥3 A, low DCR, for the post-filter |
| **B+ fuse** | fast, I²t low enough to clear when the SCR fires (coordinate with the SCR ITSM) |
| **Crowbar SCR** | ITSM > ~100 A for ~1 ms, sensitive gate; sized to survive the ~0.6 ms fault |
| **Cell-node TVS** | standoff > 4.45 V, clamp < ~7 V at the fault current |
| **12 V-rail TVS** | ~15–20 V standoff (NOT a 5 V part) |
| **Reverse-polarity P-FET** | ideal-diode on 12 V input (a small controller + P-FET, or a smart diode) |
| **3.3 V buck** | 12(or5)→3.3 V, enough current for SD-write bursts (NOT an LDO) |
| **microSD socket** | push-push with card-detect switch |
| **Sink-clamp FET** | small N-FET for the ~0.25 A low-side sink |
| **ESD/TVS on USB + SD** | protection on the exposed USB + SD-flex lines |

## Reminders for flux
- Buck: DAC → REFERENCE pin (gain ~+1), **never a feedback divider**.
- Forced-CCM (no PFM), 12 V feed (not 5 V).
- OVP crowbar independent of the buck loop.
- SD mux + flex: series source-termination, short flex, HS ≤50 MHz.
- No aluminium electrolytics on stressed nodes; ceramic/polymer only.
- Everything default-safe at power-on.
