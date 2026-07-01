# DESIGN BRIEF — PocketForge Test-Node Board (single SKU, whole board)

> Paste this whole brief into flux's Copilot as the design spec, then work block-by-block
> (see `04-block-by-block-prompts.md`). This is the COMPLETE integrated board — power stage
> + ESP32 controller + integrated microSD mux + 12 V switch + power-button presser + FEL
> strap + connectors. Assume you (the AI) are doing the full design: pick real in-stock
> parts (give MPNs), place them, and wire every net. If you can't find a part, say so —
> do NOT silently substitute. Use the exact net names in the "NET LIST" section.

---

## 0. WHAT THIS BOARD IS

A single open-hardware PCB — **one per device under test, ONE SKU** — that is the front-end
of an automated firmware test rig. It permanently **replaces the LiPo battery** in a handheld
game console (and other single-cell devices) and gives a remote host full control of the
device: it powers the device with a **firmware-programmable "virtual battery" voltage**, can
**swap the device's microSD card between a host writer and the device** without a human, can
**press the power button**, drive a **12 V LED light strip**, and force the SoC's **USB-boot
(FEL) recovery mode**. An on-board **ESP32-S3** is the local controller; the host talks to it
over **USB (CDC serial)**. The board is meant to run **24/7 for years** across a ~40-node
fleet, so reliability and protection are first-class.

Form factor target: **~2-layer, ~60 × 90 mm**, all parts **JLCPCB-assemblable** (prefer JLC
Basic/Preferred parts; hand-solderable footprints where noted). Put the **Open Source Hardware
gear logo** on the silkscreen.

---

## 1. POWER TREE (from a single 12 V input)

- **Input:** one **12 V DC barrel jack** (DC-005, 2.1 mm center-positive, ≥3 A). This is the
  ONLY external supply. Add a **reverse-polarity ideal-diode P-FET** + a **fuse** + a
  **12 V-rail TVS (~15–20 V standoff, NOT a 5 V part)** + bulk cap right at the input.
- **12 V rail** feeds: the LED-strip switch, and the two step-down regulators below. **12 V must
  NEVER reach any analog signal pin or the cell node except through the buck.**
- **5 V rail:** a **MP1584EN**-class buck (12 V→5 V) — a servo/aux rail (bulk cap for inrush).
- **3.3 V rail:** a **buck (NOT an LDO** — an LDO dropping 12→3.3 V at SD-write current
  overheats). 3.3 V powers the **ESP32-S3** and the **microSD reader + mux**. Prefer giving the
  SD reader its own quiet 3.3 V and the ESP32 a clean feed; star-ground the analog section.
- **Cell rail:** produced by the virtual-battery buck in §2 (this is the programmable output).

## 2. SUBSYSTEM A — VIRTUAL BATTERY (programmable cell, the heart)

A **12 V → Vcell forced-CCM (FPWM) synchronous buck** that regulates a single emulated Li-ion
cell: **2.5 – 4.4 V programmable, ~3 A continuous** (design the magnetics/FET/thermals for 3 A
continuous, 24/7). Output goes to the cell node **CELLP** → the power connector.

**CORE, NON-DEFAULT REQUIREMENT (DECIDED — use this exact part):** the output voltage is set by a
**DAC driving the buck's ISET reference pin at UNITY GAIN (Vout = V(ISET))**. **Do NOT build a
resistor feedback divider and do NOT inject the DAC into a divider.** The DAC is `MCP4728` (12-bit,
I²C); drive ISET directly across 2.5–4.4 V (the DAC sinks the ISET 50 µA source); the ESP32 closes a
slow outer trim loop on the INA226 reading.

- **Buck = Analog Devices `LTC3649`** (monolithic integrated-FET synchronous buck, Vin 3.1–60 V, 4 A,
  QFN/TSSOP-28). It is chosen specifically because **Vout = V(ISET) at unity gain** (a true continuous
  external reference — drive ISET with the MCP4728), and it runs **forced-continuous (float MODE/SYNC)
  so it SINKS current** at light load. Feed VIN from **+12 V** (huge margin to the 60 V rating). Wire:
  MCP4728 ch-A → `ISET` (with a small series R + a soft-start/noise cap to GND); `MODE/SYNC` floating
  (forced-continuous); FB per the datasheet unity-gain config; size the inductor for 3 A continuous.
  Cite the ISET and MODE/SYNC pins from the LTC3649 datasheet. (The buck only needs to sink ~1 A as a
  backup — the dedicated 0.25 A sink-clamp below is the primary sink.)
- **Post-filter:** one **≥3 A low-DCR ferrite bead** (or 0.47–1 µH) + **22–47 µF low-ESR
  MLCC/polymer** caps, corner ~10–30 kHz → sub-mV ripple at CELLP. **NO aluminium
  electrolytics anywhere.**
- **Telemetry:** **INA226** bidirectional V/I sense across a **10 mΩ shunt**, AFTER the filter,
  on I²C → ESP32.
- **Sink-clamp:** a small **~0.25 A active low-side sink** at CELLP (absorbs the device's
  charge-back when the emulated cell is held low). Spec ~0.6–1.1 W; can double as OVP assist.
- **INDEPENDENT over-voltage protection (must NOT depend on the buck controller):**
  a **TL431** (its OWN 2.5 V reference) senses CELLP through a divider; if CELLP > ~4.6 V it
  **fires an SCR crowbar** that shorts CELLP → blows the **B+ fuse** → isolates the device.
  Add a **cell-node TVS** as the fast (ns) backstop. (Rationale: the device PMIC's BAT-pin
  abs-max is ~7 V; keep the worst-case fault excursion ≤ ~5 V. SPICE shows the crowbar+TVS
  hold CELLP ≤ ~5 V.) The OVP reference must be independent of the DAC/buck reference so a
  regulator fault can neither false-trip nor fail to trip.
- **Grounding:** single-point **STAR ground at the CELLP cap**; **Kelvin/4-wire remote sense**
  (B+ and AUX-SENSE form the sense pair to the device).

## 3. SUBSYSTEM B — ESP32-S3 CONTROLLER NODE

- Module: **ESP32-S3-WROOM-1-N16R8** (16 MB flash / 8 MB PSRAM; PCB-antenna module,
  castellated, hand-solderable). It talks to the host over **native USB-CDC** (GPIO19/20).
- **Duties:** I²C master to the DAC + INA226; GPIO drives the buck ENABLE, the FEL-strap, the
  SD-mux select, the LED-strip FET, the power-button photoMOS; UART to the device's console.
- **GPIO / I²C budget (~14 lines):**
  | function | net(s) | count |
  |---|---|---|
  | I²C (DAC + INA226) | I2C_SDA, I2C_SCL | 2 |
  | USB-CDC (fixed) | USB_DM (GPIO19), USB_DP (GPIO20) | 2 |
  | UART to device console | UART_TX, UART_RX | 2 |
  | buck ENABLE (default-OFF at POR) | EN_BUCK | 1 |
  | FEL-strap assert (default NORMAL-BOOT unpowered) | FEL_STRAP | 1 |
  | SD-mux select | MUX_SEL (IN1), MUX_EN, [IN2] | 2–3 |
  | LED-strip FET gate (PWM) | LED_GATE | 1 |
  | power-button photoMOS drive | BTN_DRV | 1 |
  | INA226 ALERT (optional) | INA_ALERT | 0–1 |
  - **Avoid strapping pins GPIO0/3/45/46** for must-be-defined-at-boot outputs; add external
    pulls so EN_BUCK, FEL_STRAP, LED_GATE, and the mux lines sit at SAFE levels at power-on
    (buck OFF, normal-boot, LED off).

## 4. SUBSYSTEM C — INTEGRATED microSD MUX (the "card insert" path)

This is how the board provisions the device with **zero human card-swapping**. A **live microSD
card sits in an on-board socket**; an analog mux switches that card's SD bus between the
**on-board USB card-reader** (host writes the OS image) and the **device's microSD slot** (the
device boots from it).

- **On-board microSD socket** (push-push, card-detect switch used → CARD_DETECT to ESP32).
- **USB card-reader:** **GL823K-HCY04** (USB2 SD reader, SSOP-16, hand-solderable, LCSC
  C284879) with its crystal + decoupling + a USB connector upstream to the host.
- **Analog SD mux:** **TI TS3A27518E** (TS3A27518EPWR, C443721) — a 6-channel bidirectional
  analog switch. It carries the SD bus (CLK, CMD, DAT0-3) and switches between HOST side (the
  GL823K) and DUT side (the extender flex). Driven directly by **ESP32 3.3 V GPIO**:
  - IN1/IN2 = channel select (HOST vs DUT), EN = enable. Map: `MUX_SEL` = select-DUT,
    `MUX_EN`/PWR-disable, optional data-disable. (Truth-table + the DNP fallback bit-map are in
    `02-netlist-wiring-guide.md`.)
- **DUT side:** an **SD-extender FLEX** from the mux DUT-side pads out to the device's microSD
  slot (per-variant, kept SHORT).
- **SIGNAL INTEGRITY (hard constraint):** this mux+flex is documented to transmit reliably only
  to **~High-Speed / ≤50 MHz** (it FAILS at DDR50/SDR104). Add **series source-termination
  resistors** on CLK/CMD/DAT at the mux, keep the flex short, and the firmware/DT forces the
  device to High-Speed. The mux + flex are a **contained sub-region** (short terminated traces,
  flex connector at the board edge) so a v2 can re-route just this block.
- **DNP fallback (Option A, lay footprints UNPOPULATED):** a **Microchip USB2642** reader +
  **PCA9536** I²C expander that flips the SAME TS3A27518E — the Linux-Automation "Classic"
  usbsdmux circuit. Route TS3A27518E IN1/IN2/EN to EITHER the ESP32 GPIOs OR the PCA9536 via
  **DNP 0-Ω jumpers**. If ever populated, PCA9536 @ **I²C 0x41**, bits DAT_disable=0,
  PWR_disable=1, select_DUT=2. Leave these **DNP** (do not populate by default).

## 5. SUBSYSTEM D — 12 V LED-STRIP SWITCH

- **AO3400A** logic-level N-FET (SOT-23, 30 V/5.7 A, JLC Basic), **low-side**: source→GND,
  drain→strip return, strip+→12 V. Gate from `LED_GATE` GPIO via **100 Ω series + 10 kΩ
  pulldown** (defined-OFF at boot). PWM-capable. Resistive strip → no flyback diode needed.

## 6. SUBSYSTEM E — POWER-BUTTON PRESSER

- A **bidirectional MOSFET-output PhotoMOS relay** (Panasonic AQY PhotoMOS family) across the
  device's power-button **PADS** (nets BTN_A / BTN_B on the signal connector): polarity-
  agnostic, low Ron, galvanically isolated. Driven by `BTN_DRV` GPIO (LED side, with series R).
  (Do NOT use a PC817 phototransistor — it's polarity-fragile and a real button is non-polar.)

## 7. SUBSYSTEM F — FEL / USB-BOOT STRAP

- A GPIO (`FEL_STRAP`) + a small MOSFET/analog-switch that can pull the device's **FEL/USB-boot
  strap pad** to the level that forces the SoC into USB recovery boot. **Default = NORMAL BOOT
  when the ESP32 is unpowered** (external pull enforces the safe level). Routed out on the
  signal connector to a per-device pigtail.

## 8. SUBSYSTEM G — CONNECTORS (the "pigtail, not respin" contract)

The board exposes a FIXED board-side interface; each device variant is a crimped adapter
pigtail + an SD-flex, never a respin. Board-side boundaries:

- **POWER — Molex Micro-Fit 3.0, 5-circuit** (3.0 mm, keyed+latched, ~5 A/ckt):
  1. **B+** (emulated cell + = the post-filter CELLP node)
  2. **B-** (cell - / battery return = the star-ground reference)
  3. **NTC/TS** (a fixed **10 kΩ 1 % to B-** by default = the X-Powers ~25 °C default)
  4. **AUX-SENSE** (Kelvin remote-sense return; forms the sense pair with B+)
  5. **ID/SEL** (device-ID / sense-select strap)
- **SIGNAL — JST-GH 1.25, 8-pin** (keyed + latched):
  1 UART_TX · 2 UART_RX · 3 GND · 4 BTN_A · 5 BTN_B · 6 I2C_SDA · 7 I2C_SCL · 8 GND
- **SD — an SD-extender FLEX** header from the mux DUT-side to the device microSD slot (short).
- **BOARD INPUT — the 12 V barrel** (shared, not per-variant).
- **Conventions:** connectors at the board EDGE, key-notch toward the edge, strain relief, a
  per-variant silk color/label so a device-A pigtail can't seat in a device-B board.

## 9. GLOBAL CONSTRAINTS / RELIABILITY (permanent 24/7 infrastructure)

- DAC drives the buck REFERENCE, never a feedback divider.
- Forced-CCM buck only (no auto-PFM).
- OVP/crowbar independent of the buck loop, with its own reference.
- 12 V never reaches the cell node or any analog pin except through the buck.
- Kelvin 4-wire remote sense; single-point star ground at the CELLP cap.
- **No aluminium electrolytics** on stressed nodes (ceramic/polymer only).
- Continuous thermal design: **Tj ≤ ~85–90 °C** at a **45–50 °C rack ambient**, **50 % SOA
  derate**. The virtual-battery buck runs hot 24/7 — size it for continuous 3 A.
- Everything default-safe at power-on: buck OFF/high-Z, LED off, normal-boot, mux in a defined
  state, until firmware asserts otherwise.

## 10. DELIVERABLE (what I want you to produce)

1. A **block-by-block schematic** — pick real, in-stock parts (give **MPNs**, prefer JLC
   Basic/Preferred), place them grouped by subsystem, and wire **every net** in the NET LIST.
2. For each block, **confirm connections against the datasheet** you used and **cite the pins**.
3. **Flag anything that needs a human decision** (buck controller's exact reference-pin
   behaviour, fuse/SCR I²t coordination, SD SI termination values, module pinout conflicts).
4. Then a **PCB placement** honouring: analog star-ground at CELLP, the SD-mux+flex as a short
   series-terminated edge sub-region, connectors at the edge, thermal copper for the buck FET,
   OSHW logo on silk. (Layout second — get the schematic right first.)
