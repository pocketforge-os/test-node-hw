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
| 5 V buck | MP1584EN | MPS MP1584EN | 12→5 V general-purpose aux rail (DNP if unused) |
| LED switch FET | AO3400A | AOS AO3400A (C20917) | SOT-23 logic-level N-FET, JLC Basic |
| USB SD reader | GL823K-HCY04 | Genesys GL823K-HCY04 (LCSC C284879) | SSOP-16, hand-solderable |
| SD analog mux | TS3A27518E | TI TS3A27518EPWR (C443721) | 6-ch bidir switch, ~50 MHz SI ceiling |
| Power connector | Molex Micro-Fit 3.0, 5-circuit | Molex 43045 / 43025 family | keyed + latched, ~5 A/ckt |
| Signal connector | JST-GH 1.25, 8-pin | JST GH SM08B-GHS / BM08B-GHS | keyed + LATCHED |
| Barrel jack | DC-005 2.1 mm | ≥3 A, center-positive | consider a locking/higher-current jack |

## Virtual-battery buck — DECIDED
| function | part | notes |
|---|---|---|
| **Virtual-battery buck** | **Analog Devices LTC3649** (LTC3649EUFD/EFE) | monolithic integrated-FET sync buck, Vin 3.1–60 V, 4 A. **Vout = V(ISET) unity gain** (drive ISET with the MCP4728 DAC). Forced-continuous (float MODE/SYNC) → sinks. DigiKey ~$16–19; thinner LCSC stock — confirm fleet sourcing. JLC-in-stock alt if needed: MPS **MPQ8633A** (C357781, ~$6.32; analog TRK/REF ×~3.1 divider, 12A/−5.5A sink, but 16 V Vin needs input clamp). |

## Protection + power-tree — DECIDED (2026-06-30; footprints in `../lib/`)
All verified orderable at LCSC; C-numbers confirmed. SCR I²t (~2.5 A²s) ≫ fuse I²t (0.576 A²s), so the
crowbar reliably clears the fuse and survives. `⚠` = a real compromise, see the flags below.
| function | MPN | LCSC | JLC | key ratings |
|---|---|---|---|---|
| Crowbar SCR | ST **X0202MN 5BA4** | C221522 | Ext | 600 V, IGT 200 µA (sensitive gate), ITSM 22.5 A/10 ms, SOT-223 |
| B+ fuse | Littelfuse **0466003.NRHF** | C14165 | Ext | 3 A fast-acting, I²t 0.576 A²s, 1206 |
| Cell-node TVS `⚠` | **SMAJ5.0A** | C140902 | Pref | 5.0 V standoff, VBR 6.4 V, SMA — fast-edge clamp; the SCR is the primary >7 V defense |
| 12 V-rail TVS | **SMBJ15A** | C135046 | Ext | 15 V standoff, 24.4 V clamp, SMB |
| Rev-polarity P-FET `⚠` | AOS **AO3401A** | C15127 | **Basic** | −30 V, 60 mΩ, SOT-23 (see thermal flag) |
| Post-filter inductor | Sunlord **WPN252012H1R0MT** | C98348 | Ext | 1 µH, 3 A/4.2 A sat, shielded 2520 (an inductor, not a bead — see flag) |
| 3.3 V logic/SD buck | MPS **MP2315GJ-Z** | C45889 | Ext | 4.5–24 V in, 3 A, TSOT-23-8 (NOT an LDO) |
| Sink-clamp N-FET | AOS **AO3400A** | C20917 | **Basic** | 30 V, 32 mΩ @4.5 V, SOT-23 (also the LED-switch FET) |

### Flags to resolve at the Fri EE review
1. **Cell-node TVS is a compromise.** No passive silicon TVS meets "standoff ≥4.5 V AND clamp <6.5 V" — a
   5.0 V part clamps ~9.2 V at full rated Ipp. At *this* circuit's few-amp fault it clamps near its
   6.4–7.6 V breakdown, which is acceptable **only because the SCR crowbar (fires ~4.6 V) is the primary
   sustained-overvoltage defense.** Treat the TVS as the fast-dV/dt backstop. A hard <6.5 V guarantee would
   need an active clamp (TLV431 + FET) — the crowbar already is that.
2. **Rev-pol P-FET thermal:** AO3401A at 60 mΩ dissipates ~0.54 W at 3 A (SOT-23 runs hot). Fine if the real
   continuous current is ~1–2 A (tsp-bcx.9/M1 confirms); if genuinely 3 A continuous, step to a lower-RDS
   P-FET in a bigger package (→ Extended, higher cost).
3. **Post-filter = inductor, not a bead** — a ≥3 A ferrite bead with ≤20 mΩ DCR doesn't exist; a 1 µH
   inductor is the correct buck-output-filter part. (Bead alt on a separate rail: UPZ2012U221 C56066.)

## Still TBD (jellybean / from KiCad stock libs, or confirm C# when Ian places them)
- **Buck inductor** for the LTC3649 (size with tsp-bcx.9/M1 current; ~2.2–4.7 µH, ≥4 A sat).
- microSD push-push socket (w/ card-detect); MP1584 5 V buck; MCP4728 DAC; INA226; TL431; ESP32-S3-WROOM-1;
  Micro-Fit 5-ckt; JST-GH 8-pin; DC-005 barrel; USB connector; ESD/TVS on the USB + SD-flex
  lines; the SD-mux series-termination resistors; the 10 mΩ INA226 shunt; the 10 k NTC-fake.

## Design reminders (for schematic capture)
- Buck: MCP4728 DAC → **LTC3649 ISET at unity gain (Vout = V(ISET))**, **no feedback divider**; float
  MODE/SYNC (forced-continuous → sinks). 12 V feed.
- OVP crowbar (TL431→SCR→fuse) **independent** of the buck/DAC reference.
- SD mux + flex: series source-termination, short flex, force HS ≤50 MHz.
- No aluminium electrolytics on stressed nodes; everything default-safe at power-on.
