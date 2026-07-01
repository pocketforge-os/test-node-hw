# Grounding & Kelvin-sense reference (LAYOUT-CRITICAL)

**This is the make-or-break layout item for the analog section.** Read it before placing/routing
the power stage. Source: infra-201 §J (the "GROUNDING is the make-or-break bring-up item" gate).
The board mixes a hot switching buck, a 12 V LED-strip FET, and USB/SD switching **right next to** a
precision programmable cell voltage (mV-level accuracy) and a bidirectional current sense (INA226).
If the grounds and sense lines aren't disciplined, switching noise couples into the regulation/telemetry
and you get a jittery cell voltage + wrong current readings — an expensive respin. The rules:

## 1. Single-point STAR ground at the cell-node cap
- Define ONE star point: the ground terminal of the **cell-node capacitor (CELLP cap, C4)**.
- The following "quiet" returns tie to the STAR by dedicated traces, NOT to the general power/GND pour:
  - the **LTC3649 ISET reference** return (the DAC reference ground),
  - the **INA226** ground / its input filter return,
  - the **buck feedback (FB) / sense** ground,
  - the **OVP divider (TL431)** ground.
- The "noisy" returns — buck power ground (PGND, input caps, LS-FET source), the **AO3400 LED-FET
  source**, the **MP1584/3.3 V buck** grounds, the **USB/SD (GL823K + TS3A27518E)** grounds — return to
  the power ground pour and meet the quiet section at the star **once**.
- Practically on 2 layers: a solid bottom-layer ground pour for the power/switching side; a small,
  locally-connected quiet-analog ground island around CELLP/ISET/INA226 that bridges to the main pour
  at the single star via/point under the CELLP cap. Do NOT let quiet-return current share copper with
  the buck SW/PGND loop or the LED-FET switching current.

## 2. Kelvin / 4-wire remote sense to the cell
- The board regulates the voltage **at the device's battery pin**, not at the board — cabling IR drop at
  3 A would otherwise show up as cell-voltage error.
- **B+ (Micro-Fit pin 1)** and **AUX-SENSE (pin 4)** form the **remote-sense pair** to the cell node.
  Route them as a dedicated (ideally shielded/twisted in the pigtail) pair; keep them off the high-current
  B+ return path. The sense pair carries ~no current — it only measures.
- The INA226 measures across the **10 mΩ shunt (R7, CELLP↔BPLUS)** with **Kelvin taps**: two dedicated
  traces from the *exact* shunt pads (not from the fat B+ copper) to INA226 IN+/IN−, run as a tight
  differential pair, with the INA226 input RC filter close to the IC. The shunt's high-current path
  (CELLP→BPLUS→connector) is separate fat copper.

## 3. DAC reference (ISET) integrity
- The **MCP4728 → LTC3649 ISET** trace is a high-impedance precision reference. Keep it short, away from
  the SW node / LED-FET / USB lines; its series R + soft-start/noise cap sit **at the ISET pin**; its
  ground returns to the STAR. Guard/keep-out from the buck inductor field.

## 4. Domain separation (placement)
- Group and physically separate: (a) the **buck power loop** (VIN caps → LTC3649 → inductor → CELLP
  caps) — keep this loop TINY; (b) the **quiet analog** (ISET, INA226, OVP divider, TL431); (c) the
  **12 V LED-FET** switching; (d) the **USB/SD** sub-region (see §5). Don't route quiet-analog traces
  under the inductor or over the SW node.

## 5. SD-mux sub-region (a separate SI constraint — from infra-201 §Subsystem-6)
- The microSD mux + extender-flex is documented to work only to **High-Speed / ≤50 MHz** (fails at
  DDR50/SDR104). Contain it as a **modular edge sub-region**: short, length-matched-ish CLK/CMD/DAT
  traces with **series source-termination resistors at the TS3A27518E**, the flex connector at the board
  EDGE, and its own local ground. Keep this block re-routable without touching the analog star.

## 6. Fail-safe path (from §J safety)
- The **crowbar SCR → CELLP → B+ fuse** loop must be low-inductance (short, wide) so the crowbar can
  actually dump current and clear the fuse fast. The **cell-node TVS** sits right at CELLP with a short
  ground return to the star. The independent OVP (TL431) reference must NOT share the DAC/buck reference.

## Quick layout checklist for Ian
- [ ] One star point at the CELLP cap ground; quiet returns dedicated to it.
- [ ] Buck power loop (VIN→LTC3649→L→CELLP) minimized; SW node small.
- [ ] INA226 Kelvin taps from the shunt pads; differential; RC filter at the IC.
- [ ] B+/AUX-SENSE remote-sense pair, dedicated, low-current.
- [ ] ISET trace short, guarded, series-R + cap at the pin, star-grounded.
- [ ] SD-mux as a short series-terminated edge sub-region, own ground.
- [ ] Crowbar/TVS/fuse loop short + wide; TVS at CELLP.
- [ ] Thermal copper + vias under the LTC3649 (3 A continuous, 24/7, 45–50 °C ambient).
