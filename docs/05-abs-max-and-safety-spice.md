# AXP2202 BAT-pin limits + SPICE resolution of the two §J safety BLOCKERS

**Date:** 2026-06-30  **Thread:** infra-201 (Track-D board)  **For:** the Fri 2026-07-03 EE review
**Inputs:** 5 datasheet-grounded research subagents (web + primary PDFs + kernel/driver source) and an
ngspice transient model of the (d) power stage fault path.
**TL;DR:** The "keep Vcell < **4.5 V** abs-max" premise behind BLOCKER-1 was **wrong** — 4.5 V is the
AXP2202's *operating/ADC* ceiling, not a destruction limit. The real BAT-pin abs-max is **≈ 7 V**
(AXP2202 ≡ AXP717). SPICE shows the worst-case HS-FET-short fault peaks the cell node at **4.7–5.0 V**
(crowbar active) or **6.5 V** (crowbar failed, TVS-only) — **both under ~7 V**. **BLOCKER-1 and
BLOCKER-2 both resolve to PASS** pending Friday confirmation with chosen MPNs + a bench pulse test.

---

## 1. AXP2202 battery-pin voltage facts (research-verified, high confidence)

**Identity.** There is **no public AXP2202 datasheet.** Multiple primary sources (linux-sunxi, LWN
kernel article, the TrimUI Brick power-off hook, mainline `drivers/power/supply/axp20x_battery.c`)
establish **AXP2202 ≡ AXP717** (same silicon; "AXP2202" is the Allwinner BSP/boot0 name, "AXP717" is the
published part) and that both share the **AXP2101 register family**. So the **AXP717 datasheet V1.0** is
the authoritative electrical source, with AXP2101 as a corroborating sibling.

| Quantity | Value | Source / confidence |
|---|---|---|
| **BAT-pin absolute-max voltage** | **−0.3 to +7 V** | AXP717 DS Table 5-1 "Others pin (exp VBUS, EP, GND)" catch-all row; BAT (pins 41/42) is a general signal pin not broken out separately. AXP2101 V1.0 identical (7 V). **High** (category rating, not a BAT-specific line). |
| VBAT operating-range max | 4.4 V (DS V1.0) → **4.5 V** (DS V1.4) | AXP2101 Recommended Operating Conditions / operating range. High. |
| BATSENSE **ADC full-scale** | **≈ 4.5045 V** | AXP803/813 ADC spec — the gauge *cannot measure* above ~4.5 V. High. |
| CV charge target (REG 0x64[2:0]) | 4.0 / 4.1 / 4.2 / 4.35 / **4.4** / **5.0** V; default **4.2 V** | AXP717 DS REG64 + mainline kernel `AXP717_CHRG_CV_*` enum (agree exactly). **Very high.** |
| **4.45 V a selectable target?** | **No** | Not in REG64 nor the driver; the "4.44/4.45 V" strings in the DS are *other* registers (DPM/Vsys, button-cell). Very high. |
| Internal BAT over-voltage protection | **Yes** — autonomous: charging gated while `VBAT < VBAT_OVP`, + sticky `bovp_irq` (REG 0x42/0x4A bit0, default on). Does **not** open BATFET. Numeric threshold not published (≳4.5 V). | AXP2101 DS §6.7.2 + register tables + XPowersLib enum. High (mechanism); Low (exact number). |
| VBUS (USB) over-voltage | 7 V typ rising; VBUS abs-max 12 V | Separate mechanism from BAT. High. |

**The load-bearing correction:** §J/the bead treated **4.5 V** as the AXP2202 BAT *abs-max*. It is not —
it is the **operating-range max / ADC full-scale**. The destruction limit is the **~7 V** BAT-pin abs-max.
There is therefore a **~2.5 V margin** between the 4.4 V normal charge ceiling and the ~7 V abs-max, where
§J assumed essentially **zero** margin. Two further points:
- Because the cell is **emulated** (no physical LiPo at the node), the "never exceed ~4.45 V or the LiPo
  vents/ignites" safety rule **does not apply** — the only things on the node are the PMIC + caps, bounded
  by the ~7 V silicon limit.
- The PMIC **self-protects** against BAT over-voltage (stops charging + IRQ), an independent backstop to
  our board-level crowbar.
- **Emulator range should be 2.5–4.4 V** (the device's true max CV target) with headroom to ~4.5 V — not
  "2.5–4.45 V". (A 5.0 V "high-voltage" CV option exists on AXP717 but is not needed.)

> Caveat carried forward: 7 V is read from the AXP717/AXP2101 *category* abs-max row (BAT not itemised),
> standing in for the unpublished AXP2202. Treat ~7 V as the abs-max and **design to a conservative ≤ ~5 V
> fault ceiling anyway** (defense-in-depth + keeps the device's own OVP/charge logic sane). Confirm on the
> bench if an AXP2202-titled sheet ever surfaces.

---

## 2. SPICE model of the fault path (BLOCKER-1 / -2)

**Deck:** `evidence/test-node-d-blocker-spice.cir` (ngspice-42). **Scenario:** during the SINK phase
(cell held low ~3.2 V) the buck **high-side FET shorts**, slamming 12 V through the buck inductor → post-
filter (ferrite + caps) → B+ fuse → 10 mΩ shunt → cell node. Protections on the cell node: a **TVS**, an
**independent latching crowbar** (TL431 sense, 4.6 V trip → SCR shorts the node → blows the fuse), and the
cell/device capacitance. Behavioural models: diode-latched crowbar with an RC sense delay; fuse = low-R
until ∫i²dt reaches its I²t rating, then latches open. **Candidate values, Friday-gated**
(L=1 µH, C2=C3=47 µF, C4=47 µF, Cdev=100 µF, fuse I²t=2.0 A²s, RHS=20 mΩ).

### Results (base case)
| Metric | Value | Meaning |
|---|---|---|
| **CELLP peak (crowbar active)** | **4.81 V** | worst the device's BAT pin sees during the fault |
| CELLP peak (crowbar FAILED, TVS-only) | **6.55 V** | single-fault backstop — still < ~7 V |
| Fuse clear time | **0.60 ms** (TVS-only 1.57 ms) | how long until the device is isolated |
| Peak fuse current | 60.8 A | sizes the fuse + copper |
| Peak SCR current | 96.2 A | sizes the crowbar SCR surge (ITSM) |
| SCR conduction energy | **0.10 J** over ~0.6 ms | within a small SCR's I²t / ITSM |

### Sensitivity sweeps (worst-case bounding)
- **Crowbar latency 0.5 → 10 µs:** CELLP peak **flat at 4.81 V.** The 147 µF cell-node capacitance +
  inductor-limited di/dt set the peak, *not* crowbar speed → **BLOCKER-2 timing is non-critical.**
- **Device input cap 220 → 10 µF:** peak 4.75 → 4.89 V (smaller cap = higher).
- **Buck inductor 4.7 → 0.47 µH:** peak 4.72 → 4.85 V (smaller L = faster di/dt = higher).
- **Worst-case combo (10 µF dev-cap + 0.47 µH), crowbar active:** **4.97 V.**
- **Worst-case combo, crowbar FAILED (TVS-only):** **6.54 V.**
- **TVS standoff 4.5 → 6.0 V:** peak ~4.79–4.81 V (crowbar dominates; TVS choice not critical when the
  crowbar fires).

### Interpretation
- **BLOCKER-1 → PASS.** Across *every* parameter combination with the crowbar working, CELLP stays
  **≤ ~5.0 V**, and even with the crowbar **failed** the TVS alone holds **≤ ~6.55 V** — both inside the
  ~7 V BAT abs-max. The two-layer (TVS + crowbar) protection gives single-fault tolerance with margin.
- **BLOCKER-2 → PASS / non-critical.** The trip→clear lag does not drive the peak (insensitive to 0.5–10 µs).
  The crowbar collapses the node and the fuse clears in ~0.6 ms; the SCR sees ~96–99 A / ~0.1 J for ~0.6 ms,
  well within a small SCR's surge rating. **Design rule:** pick F1 so its total I²t (let-through) < the SCR's
  I²t rating, and the SCR's ITSM > ~100 A for ~1 ms.

### Honest limitations (for the EE review)
First-order behavioural model with candidate values and *idealised* TVS (linear clamp above standoff),
fuse (fixed-I²t open), and SCR (instant latch). It captures the dominant physics (LC di/dt, node-cap
charge, two-layer clamp, fuse let-through) and the **trend/margins are robust**, but the exact numbers
will shift with the real TVS clamp curve, the fuse's I²t-vs-current curve, the SCR turn-on di/dt, and the
*measured* device input capacitance. **Friday actions:** (1) drop in the chosen TVS/SCR/fuse MPNs and re-run;
(2) bench-validate with a controlled HS-FET-short pulse while holding the cell low and a ≥100 kHz B+ capture;
(3) confirm SCR ITSM/I²t > fuse let-through.

---

## 3. Net effect on §J and the Friday agenda

- **BLOCKER-1 and BLOCKER-2 downgrade from "pre-PCB blockers" to "confirm-at-Friday-with-MPNs"** — the
  conceptual risk (no margin to abs-max) is gone; what remains is part selection + a bench check.
- **Correct the abs-max number everywhere** it says "4.5 V abs-max": the BAT abs-max is **~7 V**; 4.5 V is the
  operating/ADC ceiling. Keep a **conservative ≤ ~5 V design ceiling** as defense-in-depth.
- **Relax the emulator top end to 2.5–4.4 V** (true max CV target) with headroom to ~4.5 V; 4.45 V was not
  grounded in the AXP2202's actual charge targets.
- **Still gates KiCad layout:** the **grounding / Kelvin-sense reference schematic** (the §J MAJOR) is
  unaffected by this analysis and remains a defer-KiCad item.
- **tsp-bcx.9 unchanged in priority:** M1 continuous I_peak (sizes the buck/inductor/FET, and the SOURCE-side
  thermal which is the *real* binding case) + the AXP2202 gauge-ripple tolerance (sizes the post-filter).

## Sources
AXP717 DS V1.0 (dl.100ask.net …/AXP717_Datasheet_V1.0_en.pdf; LCSC C2997897). AXP2101 DS V1.0/V1.4
(M5Stack; LCSC C3036461). Mainline Linux `drivers/power/supply/axp20x_battery.c` (`AXP717_CHRG_CV_*`,
`AXP717_CV_CHG_SET 0x64`). Zephyr `charger_axp2101.c` + DT binding. XPowersLib `XPOWERS_AXP2101_BAT_OVER_VOL_IRQ`.
LWN 964958 (AXP717≡AXP2202). TrimUI Brick poweroff-hook (AXP2202↔AXP717). Full URL list in the research
subagent transcripts for this session.
