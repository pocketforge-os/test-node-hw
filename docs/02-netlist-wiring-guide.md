# NET LIST / wiring guide — whole board (paste alongside the brief)

Net names to use verbatim. `*` = value/MPN Friday-gated. Power rails: `+12V`, `+5V`, `+3V3`,
`+3V3_SD` (optional), `GND`. This is the connectivity source-of-truth — draw these as wires.

## A. Virtual-battery power stage
| net | pins | notes |
|---|---|---|
| +12V_RAW | BARREL.+, Q_revpol.S | raw input |
| +12V | Q_revpol.D, BUCK.VIN, C_bulk.1, D_TVS12.1, R_bleed.1, MP1584.VIN | protected 12 V |
| SW | BUCK.SW, L1.1 | buck switch node |
| VPRE | L1.2, FB1.1, C_pre.1 | pre-filter rail |
| VFILT | FB1.2, C_filt.1, FUSE.1 | post-filter rail |
| DAC_REF | MCP4728.VOUT_A, BUCK.REF/FB-ref | DAC → buck reference, gain ~+1, NO divider |
| EN_BUCK | BUCK.EN, ESP32.GPIO(EN_BUCK) | default-OFF at POR |
| CELLP | FUSE.2, R_shunt.1, C_cell.1, R_ovp_top.1, R_cbpu.1, SCR.A, D_TVScell.1, Q_sink.D | cell node (star gnd at C_cell) |
| BPLUS | R_shunt.2, INA226.IN+, MicroFit.1 | emulated cell + (post-shunt) |
| (shunt) | R_shunt across CELLP↔BPLUS; INA226.IN+ = BPLUS, INA226.IN- = CELLP | 10 mΩ, Kelvin |
| OVP_SENSE | R_ovp_top.2, R_ovp_bot.1, TL431.REF | divider → TL431 ref (~4.6 V trip) |
| CROWBAR_GATE | TL431.CATHODE, R_cbpu.2, R_scrg.1 | TL431 cathode → SCR gate drive |
| SCR_G | R_scrg.2, SCR.G | SCR gate |
| SINK_EN | Q_sink.G, ESP32.GPIO(SINK_EN) | sink-clamp enable |
| SINK_S | Q_sink.S, R_sinksns.1 | sink source-sense |

## B. Rails / regulators
| net | pins | notes |
|---|---|---|
| +5V | MP1584.SW→L→out, servo header.+ | 12→5 V buck (aux/servo) |
| +3V3 | BUCK33.out, ESP32.3V3, (SD ICs if shared) | 12(or5)→3.3 V BUCK, NOT an LDO |
| +3V3_SD | (optional separate 3.3 V for the SD reader/mux) | quiet SD rail |
| GND | all grounds; single-point star at C_cell | — |

## C. ESP32-S3 control + I²C + USB + UART
| net | pins | notes |
|---|---|---|
| I2C_SDA / I2C_SCL | ESP32.I2C ↔ MCP4728, INA226, (PCA9536 DNP) ↔ GH.6/7 | I²C master; 4.7 k pull-ups |
| USB_DM / USB_DP | ESP32.GPIO19/20 ↔ USB-C/USB-micro (host CDC) | native USB-CDC to host |
| UART_TX / UART_RX | ESP32.UART ↔ GH.1/2 | device console |
| EN_BUCK | ESP32 → BUCK.EN | ext pulldown (OFF at POR) |
| FEL_STRAP | ESP32 → FEL switch → device FEL pad (pigtail) | ext pull = NORMAL boot when ESP32 off |
| MUX_SEL (IN1) | ESP32 → TS3A27518E.IN1 | select HOST vs DUT |
| MUX_IN2 | ESP32 → TS3A27518E.IN2 | 2nd select bit (or tie per truth table) |
| MUX_EN | ESP32 → TS3A27518E.EN | mux enable / power-disable |
| LED_GATE | ESP32 → AO3400A.G (100 Ω series, 10 k pulldown) | PWM, OFF at boot |
| BTN_DRV | ESP32 → PhotoMOS LED (series R) | press = drive on |
| INA_ALERT | INA226.ALERT → ESP32 (optional) | fast OV/OC flag |
| CARD_DETECT | microSD socket CD switch → ESP32 | card present sense |

## D. SD-mux bus (TS3A27518E common = the on-board microSD socket)
Each SD line (CLK, CMD, DAT0, DAT1, DAT2, DAT3) is one mux channel with 3 taps:
- **CARD (common):** `SD_CLK, SD_CMD, SD_D0..D3` → the on-board microSD socket.
- **HOST side:** `SD_CLK_H, SD_CMD_H, SD_D0..D3_H` → GL823K reader (write path).
- **DUT side:** `SD_CLK_D, SD_CMD_D, SD_D0..D3_D` → the SD-extender FLEX to the device.
- Add **series source-termination R** on CLK/CMD/DAT at the mux; keep flex short; force HS ≤50 MHz.
- microSD socket power via a switchable 3.3 V (so the card can be power-cycled).

## E. TS3A27518E select truth table (Option B, ESP32-driven)
- Populate B: drive IN1/IN2/EN from ESP32 GPIO directly (3.3 V logic OK, 1.65–3.6 V).
  - EN=low → mux enabled; IN selects HOST (host writes the card) vs DUT (device boots).
  - Provide a DISABLE/high-Z state (card isolated) for safe power-up.
- DNP fallback A (leave UNPOPULATED): PCA9536 @ I²C **0x41**, bits `DAT_disable=0`,
  `PWR_disable=1`, `select_DUT=2`; route IN1/IN2/EN to EITHER ESP32 GPIO or PCA9536 via DNP 0 Ω.

## F. Connectors
- **Micro-Fit 3.0 5-pin (POWER):** 1=B+(BPLUS) · 2=B-(GND) · 3=NTC(10k→B-) · 4=AUX_SENSE · 5=ID_SEL
- **JST-GH 1.25 8-pin (SIGNAL):** 1=UART_TX · 2=UART_RX · 3=GND · 4=BTN_A · 5=BTN_B · 6=I2C_SDA · 7=I2C_SCL · 8=GND
- **SD-extender FLEX (per-variant):** SD_CLK_D, SD_CMD_D, SD_D0_D..D3_D, GND (+ card 3.3 V if needed)
- **Barrel DC-005:** center=+12V_RAW, sleeve=GND
- **USB (to host):** USB_DM, USB_DP, VBUS(n/c or sense), GND

## Off-board / firmware
- MCP4728 ch-A = DAC_REF (buck reference). INA226 across the 10 mΩ shunt (BPLUS/CELLP).
- EN_BUCK, SINK_EN, FEL_STRAP, MUX_*, LED_GATE, BTN_DRV = ESP32 GPIO. CARD_DETECT, INA_ALERT = inputs.
- FEL strap + power-button + UART leave via the GH signal connector / per-device pigtail.
