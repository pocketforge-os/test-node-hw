OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := dut-fixture.scad
BPI_SOURCE := bpi-m2-zero-v1.scad
BPI_PROVENANCE := BPI-M2-ZERO-PROVENANCE.md
RELAY_SOURCE := elegoo-4-channel-relay.scad
RELAY_PROVENANCE := ELEGOO-4-CHANNEL-RELAY-PROVENANCE.md
BOOST_SOURCE := hiletgo-xl6009.scad
BOOST_PROVENANCE := HILETGO-XL6009-PROVENANCE.md
MOSFET_SOURCE := ceksezx-mtsd001.scad
MOSFET_PROVENANCE := CEKSEZX-MTSD001-PROVENANCE.md
DP100_SOURCE := alientek-dp100.scad
DP100_PROVENANCE := ALIENTEK-DP100-PROVENANCE.md
ESP32_SOURCE := esp32-s3-supermini-hw747-v0.0.2.scad
ESP32_PROVENANCE := ESP32-S3-SUPERMINI-PROVENANCE.md
C270_SOURCE := logitech-c270.scad
C270_PROVENANCE := LOGITECH-C270-PROVENANCE.md
ANTENNA_SOURCE := eightwood-ewua0205.scad
ANTENNA_PROVENANCE := EIGHTWOOD-EWUA0205-PROVENANCE.md
VIENON_SOURCE := vienon-usb-001.scad
VIENON_PROVENANCE := VIENON-USB-001-PROVENANCE.md
SMAYS_SOURCE := smays-microb-hub-8152.scad
SMAYS_PROVENANCE := SMAYS-MICROB-HUB-8152-PROVENANCE.md
BPI_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-bpi-m2-zero-pcb.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-dark.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-metal.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-gold.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-silkscreen.stl
RELAY_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-elegoo-relay-pcb.stl \
	$(BUILD)/pocketforge-elegoo-relay-blue.stl \
	$(BUILD)/pocketforge-elegoo-relay-dark.stl \
	$(BUILD)/pocketforge-elegoo-relay-metal.stl \
	$(BUILD)/pocketforge-elegoo-relay-led.stl \
	$(BUILD)/pocketforge-elegoo-relay-silkscreen.stl
RELAY_COMPLETE_STL := $(BUILD)/pocketforge-elegoo-relay-complete.stl
BOOST_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-hiletgo-xl6009-pcb.stl \
	$(BUILD)/pocketforge-hiletgo-xl6009-dark.stl \
	$(BUILD)/pocketforge-hiletgo-xl6009-adjuster.stl \
	$(BUILD)/pocketforge-hiletgo-xl6009-metal.stl \
	$(BUILD)/pocketforge-hiletgo-xl6009-silkscreen.stl
BOOST_COMPLETE_STL := $(BUILD)/pocketforge-hiletgo-xl6009-complete.stl
MOSFET_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-ceksezx-mtsd001-pcb.stl \
	$(BUILD)/pocketforge-ceksezx-mtsd001-blue.stl \
	$(BUILD)/pocketforge-ceksezx-mtsd001-dark.stl \
	$(BUILD)/pocketforge-ceksezx-mtsd001-metal.stl \
	$(BUILD)/pocketforge-ceksezx-mtsd001-led.stl \
	$(BUILD)/pocketforge-ceksezx-mtsd001-silkscreen.stl
MOSFET_COMPLETE_STL := $(BUILD)/pocketforge-ceksezx-mtsd001-complete.stl
DP100_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-alientek-dp100-shell.stl \
	$(BUILD)/pocketforge-alientek-dp100-dark.stl \
	$(BUILD)/pocketforge-alientek-dp100-controls.stl \
	$(BUILD)/pocketforge-alientek-dp100-screen.stl \
	$(BUILD)/pocketforge-alientek-dp100-accent.stl \
	$(BUILD)/pocketforge-alientek-dp100-metal.stl \
	$(BUILD)/pocketforge-alientek-dp100-markings.stl
DP100_COMPLETE_STL := $(BUILD)/pocketforge-alientek-dp100-complete.stl
ESP32_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-esp32-s3-supermini-pcb.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-dark.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-metal.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-gold.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-antenna.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-silkscreen.stl
ESP32_COMPLETE_STL := $(BUILD)/pocketforge-esp32-s3-supermini-complete.stl
C270_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-logitech-c270-shell.stl \
	$(BUILD)/pocketforge-logitech-c270-dark.stl \
	$(BUILD)/pocketforge-logitech-c270-glass.stl \
	$(BUILD)/pocketforge-logitech-c270-led.stl \
	$(BUILD)/pocketforge-logitech-c270-labels.stl
C270_COMPLETE_STL := $(BUILD)/pocketforge-logitech-c270-complete.stl
ANTENNA_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-eightwood-ewua0205-dark.stl \
	$(BUILD)/pocketforge-eightwood-ewua0205-metal.stl \
	$(BUILD)/pocketforge-eightwood-ewua0205-markings.stl
ANTENNA_COMPLETE_STL := $(BUILD)/pocketforge-eightwood-ewua0205-complete.stl
ANTENNA_BODY_STL := $(BUILD)/pocketforge-eightwood-ewua0205-body-check.stl
VIENON_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-vienon-usb-001-shell.stl \
	$(BUILD)/pocketforge-vienon-usb-001-dark.stl \
	$(BUILD)/pocketforge-vienon-usb-001-metal.stl \
	$(BUILD)/pocketforge-vienon-usb-001-blue.stl \
	$(BUILD)/pocketforge-vienon-usb-001-led.stl
VIENON_COMPLETE_STL := $(BUILD)/pocketforge-vienon-usb-001-complete.stl
VIENON_BODY_STL := $(BUILD)/pocketforge-vienon-usb-001-body-check.stl
SMAYS_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-smays-microb-hub-8152-shell.stl \
	$(BUILD)/pocketforge-smays-microb-hub-8152-dark.stl \
	$(BUILD)/pocketforge-smays-microb-hub-8152-metal.stl \
	$(BUILD)/pocketforge-smays-microb-hub-8152-led.stl \
	$(BUILD)/pocketforge-smays-microb-hub-8152-markings.stl
SMAYS_COMPLETE_STL := $(BUILD)/pocketforge-smays-microb-hub-8152-complete.stl
SMAYS_BODY_STL := $(BUILD)/pocketforge-smays-microb-hub-8152-body-check.stl
FINAL_COMPONENT_SOURCES := $(ANTENNA_SOURCE) $(VIENON_SOURCE) $(SMAYS_SOURCE)

.PHONY: all lint validate validate-overlap-guard validate-service-guard \
	validate-preview-export validate-presentation-assets \
	validate-bpi-model-guard validate-bpi-provenance \
	validate-relay-model-guard validate-relay-provenance \
	validate-boost-model-guard validate-boost-provenance \
	validate-mosfet-model-guard validate-mosfet-provenance \
	validate-dp100-model-guard validate-dp100-provenance \
	validate-esp32-model-guard validate-esp32-provenance \
	validate-c270-model-guard validate-c270-provenance \
	validate-final-components-model-guard \
	validate-final-components-provenance preview split clean

all: $(BUILD)/pocketforge-dut-fixture-v1.stl $(BUILD)/fit-coupon.stl

# Repository-wide CSG export is the fast parse/evaluation gate. The wrapper
# also rejects OpenSCAD ERROR diagnostics because CSG assertion failures may
# otherwise return a successful process status.
lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD):
	mkdir -p $@

$(BUILD)/pocketforge-dut-fixture-v1.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/pocketforge-dut-fixture-components.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_components"' $<

$(BUILD)/pocketforge-dut-fixture-labels.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_labels"' $<

$(BUILD)/pocketforge-bpi-m2-zero-pcb.stl: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_bpi_pcb"' $<

$(BUILD)/pocketforge-bpi-m2-zero-dark.stl: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_bpi_dark"' $<

$(BUILD)/pocketforge-bpi-m2-zero-metal.stl: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_bpi_metal"' $<

$(BUILD)/pocketforge-bpi-m2-zero-gold.stl: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_bpi_gold"' $<

$(BUILD)/pocketforge-bpi-m2-zero-silkscreen.stl: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_bpi_silkscreen"' $<

$(BUILD)/pocketforge-elegoo-relay-complete.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay"' $<

$(BUILD)/pocketforge-elegoo-relay-pcb.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay_pcb"' $<

$(BUILD)/pocketforge-elegoo-relay-blue.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay_blue"' $<

$(BUILD)/pocketforge-elegoo-relay-dark.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay_dark"' $<

$(BUILD)/pocketforge-elegoo-relay-metal.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay_metal"' $<

$(BUILD)/pocketforge-elegoo-relay-led.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay_led"' $<

$(BUILD)/pocketforge-elegoo-relay-silkscreen.stl: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_relay_silkscreen"' $<

$(BUILD)/pocketforge-hiletgo-xl6009-complete.stl: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_boost"' $<

$(BUILD)/pocketforge-hiletgo-xl6009-pcb.stl: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_boost_pcb"' $<

$(BUILD)/pocketforge-hiletgo-xl6009-dark.stl: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_boost_dark"' $<

$(BUILD)/pocketforge-hiletgo-xl6009-adjuster.stl: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_boost_adjuster"' $<

$(BUILD)/pocketforge-hiletgo-xl6009-metal.stl: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_boost_metal"' $<

$(BUILD)/pocketforge-hiletgo-xl6009-silkscreen.stl: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_boost_silkscreen"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-complete.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-pcb.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet_pcb"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-blue.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet_blue"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-dark.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet_dark"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-metal.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet_metal"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-led.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet_led"' $<

$(BUILD)/pocketforge-ceksezx-mtsd001-silkscreen.stl: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_mosfet_silkscreen"' $<

$(BUILD)/pocketforge-alientek-dp100-complete.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100"' $<

$(BUILD)/pocketforge-alientek-dp100-shell.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_shell"' $<

$(BUILD)/pocketforge-alientek-dp100-dark.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_dark"' $<

$(BUILD)/pocketforge-alientek-dp100-controls.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_controls"' $<

$(BUILD)/pocketforge-alientek-dp100-screen.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_screen"' $<

$(BUILD)/pocketforge-alientek-dp100-accent.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_accent"' $<

$(BUILD)/pocketforge-alientek-dp100-metal.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_metal"' $<

$(BUILD)/pocketforge-alientek-dp100-markings.stl: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_dp100_markings"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-complete.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-pcb.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32_pcb"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-dark.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32_dark"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-metal.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32_metal"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-gold.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32_gold"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-antenna.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32_antenna"' $<

$(BUILD)/pocketforge-esp32-s3-supermini-silkscreen.stl: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_esp32_silkscreen"' $<

$(BUILD)/pocketforge-logitech-c270-complete.stl: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_c270"' $<

$(BUILD)/pocketforge-logitech-c270-shell.stl: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_c270_shell"' $<

$(BUILD)/pocketforge-logitech-c270-dark.stl: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_c270_dark"' $<

$(BUILD)/pocketforge-logitech-c270-glass.stl: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_c270_glass"' $<

$(BUILD)/pocketforge-logitech-c270-led.stl: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_c270_led"' $<

$(BUILD)/pocketforge-logitech-c270-labels.stl: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_c270_labels"' $<

$(ANTENNA_COMPLETE_STL): $(SOURCE) $(ANTENNA_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_antenna"' $<

$(BUILD)/pocketforge-eightwood-ewua0205-dark.stl: $(SOURCE) $(ANTENNA_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_antenna_dark"' $<

$(ANTENNA_BODY_STL): $(SOURCE) $(ANTENNA_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_antenna_body"' $<

$(BUILD)/pocketforge-eightwood-ewua0205-metal.stl: $(SOURCE) $(ANTENNA_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_antenna_metal"' $<

$(BUILD)/pocketforge-eightwood-ewua0205-markings.stl: $(SOURCE) $(ANTENNA_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_antenna_markings"' $<

$(VIENON_COMPLETE_STL): $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_unpowered_hub"' $<

$(BUILD)/pocketforge-vienon-usb-001-shell.stl: $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_vienon_shell"' $<

$(VIENON_BODY_STL): $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_vienon_body"' $<

$(BUILD)/pocketforge-vienon-usb-001-dark.stl: $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_vienon_dark"' $<

$(BUILD)/pocketforge-vienon-usb-001-metal.stl: $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_vienon_metal"' $<

$(BUILD)/pocketforge-vienon-usb-001-blue.stl: $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_vienon_blue"' $<

$(BUILD)/pocketforge-vienon-usb-001-led.stl: $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_vienon_led"' $<

$(SMAYS_COMPLETE_STL): $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_powered_hub"' $<

$(BUILD)/pocketforge-smays-microb-hub-8152-shell.stl: $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_smays_shell"' $<

$(SMAYS_BODY_STL): $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_smays_body"' $<

$(BUILD)/pocketforge-smays-microb-hub-8152-dark.stl: $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_smays_dark"' $<

$(BUILD)/pocketforge-smays-microb-hub-8152-metal.stl: $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_smays_metal"' $<

$(BUILD)/pocketforge-smays-microb-hub-8152-led.stl: $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_smays_led"' $<

$(BUILD)/pocketforge-smays-microb-hub-8152-markings.stl: $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_smays_markings"' $<

$(BUILD)/fit-coupon.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/preview-export.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/plate-lower.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_lower"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/plate-upper.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_upper"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/joiner.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="joiner"' -D 'SHOW_COMPONENTS=false' $<

split: $(BUILD)/plate-lower.stl $(BUILD)/plate-upper.stl $(BUILD)/joiner.stl

$(BUILD)/layout-preview.png: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho --viewall \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/layout-top.png: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(MOSFET_SOURCE) $(DP100_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) $(FINAL_COMPONENT_SOURCES) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho \
		--autocenter --viewall --camera=100,120,400,100,120,0 \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/layout-bpi-m2-zero.png: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1400 --projection=ortho \
		--viewall --camera=29,60,115,29,117,10 \
		-D 'PART="presentation_bpi"' $<

$(BUILD)/layout-elegoo-relay.png: $(SOURCE) $(RELAY_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,900 --projection=ortho \
		--viewall --camera=45,189,110,45,189,28 \
		-D 'PART="presentation_relay"' $<

$(BUILD)/layout-hiletgo-xl6009.png: $(SOURCE) $(BOOST_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,800 --projection=ortho \
		--viewall --camera=170,70,60,170,107,10 \
		-D 'PART="presentation_boost"' $<

$(BUILD)/layout-ceksezx-mtsd001.png: $(SOURCE) $(MOSFET_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 --projection=ortho \
		--viewall --camera=174,112,60,174,131,9 \
		-D 'PART="presentation_mosfet"' $<

$(BUILD)/layout-alientek-dp100.png: $(SOURCE) $(DP100_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 --projection=ortho \
		--viewall --camera=137,125,100,137,193,12 \
		-D 'PART="presentation_dp100"' $<

$(BUILD)/layout-esp32-s3-supermini.png: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1400 --projection=ortho \
		--viewall --camera=17,68,65,17,68,8 \
		-D 'PART="presentation_esp32"' $<

$(BUILD)/layout-logitech-c270.png: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 --projection=ortho \
		--viewall --camera=100,85,-130,100,132,-5 \
		-D 'PART="presentation_c270"' $<

$(BUILD)/layout-eightwood-ewua0205.png: $(SOURCE) $(ANTENNA_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,650 --projection=ortho \
		--viewall --camera=97,210,90,97,236,2 \
		-D 'PART="presentation_antenna"' $<

$(BUILD)/layout-vienon-usb-001.png: $(SOURCE) $(VIENON_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,800 --projection=ortho \
		--viewall --camera=116,-20,95,116,20,4 \
		-D 'PART="presentation_unpowered_hub"' $<

$(BUILD)/layout-smays-microb-hub-8152.png: $(SOURCE) $(SMAYS_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,850 --projection=ortho \
		--viewall --camera=120,94,105,120,52,7 \
		-D 'PART="presentation_powered_hub"' $<

preview: $(BUILD)/layout-preview.png $(BUILD)/layout-top.png \
	$(BUILD)/layout-bpi-m2-zero.png $(BUILD)/layout-elegoo-relay.png \
	$(BUILD)/layout-hiletgo-xl6009.png \
	$(BUILD)/layout-ceksezx-mtsd001.png \
	$(BUILD)/layout-alientek-dp100.png \
	$(BUILD)/layout-esp32-s3-supermini.png \
	$(BUILD)/layout-logitech-c270.png \
	$(BUILD)/layout-eightwood-ewua0205.png \
	$(BUILD)/layout-vienon-usb-001.png \
	$(BUILD)/layout-smays-microb-hub-8152.png

validate-overlap-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-overlap.log; mesh=$(BUILD)/intentional-overlap.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="fit_coupon"' \
			-D 'antenna_origin=[50,160]' \
			-D 'antenna_model_tie_x=[17,77]' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional component overlap was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Component envelope clearance violation: relay vs antenna' $$log; \
		rm -f $$log $$mesh; \
		echo 'layout_overlap_guard=pass pair=relay_vs_antenna'

validate-service-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-service-collision.log; \
		mesh=$(BUILD)/intentional-service-collision.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="fit_coupon"' \
			-D 'mosfet_origin=[50,95.22]' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional webcam service-zone collision was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Service keep-out violation: webcam_below_service vs mosfet' $$log; \
		rm -f $$log $$mesh; \
		echo 'service_keepout_guard=pass pair=webcam_below_service_vs_mosfet'

validate-preview-export: $(BUILD)/pocketforge-dut-fixture-v1.stl $(BUILD)/preview-export.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(BUILD)/pocketforge-dut-fixture-v1.stl \
		$(BUILD)/preview-export.stl
	@echo 'preview_export_guard=pass ghosts=excluded'

validate-bpi-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-bpi-scale.log; \
		mesh=$(BUILD)/intentional-bpi-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_bpi_pcb"' \
			-D 'BPI_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional BPI scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'BPI model scale/orientation changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-bpi-registration.log; \
		mesh=$(BUILD)/intentional-bpi-registration.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_bpi_pcb"' \
			-D 'BPI_MODEL_HOLE_CENTRES=[23.01,58.36]' \
			$(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional BPI registration change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'BPI mounting registration changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'bpi_model_guard=pass scale=1 orientation=portrait holes=23.00x58.36'

validate-bpi-provenance: $(BPI_SOURCE) $(BPI_PROVENANCE)
	@grep -Fq '7adbb58ab77addc91a5fc2ee84df689e5db62e7ed2b9b2b12b166684b1632833' \
		$(BPI_SOURCE)
	@grep -Fq '9d0815fd9bdb3cb5dd790d8dda1eb132a36802b586dc5eab696c79cea3dc592a' \
		$(BPI_SOURCE)
	@grep -Fq '7adbb58ab77addc91a5fc2ee84df689e5db62e7ed2b9b2b12b166684b1632833' \
		$(BPI_PROVENANCE)
	@grep -Fq '9d0815fd9bdb3cb5dd790d8dda1eb132a36802b586dc5eab696c79cea3dc592a' \
		$(BPI_PROVENANCE)
	@echo 'bpi_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-relay-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-relay-scale.log; \
		mesh=$(BUILD)/intentional-relay-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_relay_pcb"' \
			-D 'RELAY_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional relay scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ELEGOO relay model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-relay-orientation.log; \
		mesh=$(BUILD)/intentional-relay-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_relay_pcb"' \
			-D 'RELAY_MODEL_TERMINAL_EDGE="-X"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional relay terminal reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ELEGOO relay terminal/header orientation changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-relay-registration.log; \
		mesh=$(BUILD)/intentional-relay-registration.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_relay_pcb"' \
			-D 'RELAY_MODEL_HOLE_CENTRES=[45.04,66.93]' \
			$(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional relay registration change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ELEGOO relay mounting registration changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'relay_model_guard=pass envelope=51.85x72.70 holes=45.03x66.93 terminal_edge=+X'

validate-relay-provenance: $(RELAY_SOURCE) $(RELAY_PROVENANCE)
	@grep -Fq 'a8a405e23244346ee17a98e7b317e86a2b809719e8304e413bd249308405f144' \
		$(RELAY_SOURCE)
	@grep -Fq 'd967bb2e60d35e36d019f55ab48bb20e838cf1b8e9ab65933090c9585f16ca67' \
		$(RELAY_SOURCE)
	@grep -Fq 'a8a405e23244346ee17a98e7b317e86a2b809719e8304e413bd249308405f144' \
		$(RELAY_PROVENANCE)
	@grep -Fq 'd967bb2e60d35e36d019f55ab48bb20e838cf1b8e9ab65933090c9585f16ca67' \
		$(RELAY_PROVENANCE)
	@grep -Fq 'No Amazon image, ELEGOO artwork, EDA file' $(RELAY_PROVENANCE)
	@echo 'relay_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-boost-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-boost-scale.log; \
		mesh=$(BUILD)/intentional-boost-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_boost_pcb"' \
			-D 'BOOST_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional XL6009 scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'HiLetgo XL6009 model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-boost-orientation.log; \
		mesh=$(BUILD)/intentional-boost-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_boost_pcb"' \
			-D 'BOOST_MODEL_INPUT_EDGE="+X"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional XL6009 IN/OUT reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'HiLetgo XL6009 input/output orientation changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-boost-registration.log; \
		mesh=$(BUILD)/intentional-boost-registration.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_boost_pcb"' \
			-D 'BOOST_MODEL_HOLE_CENTRES=[[6.51,18.63],[36.66,2.20]]' \
			$(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional XL6009 hole drift was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'HiLetgo XL6009 mounting registration changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'boost_model_guard=pass envelope=43.16x21.23 holes=diagonal input_edge=-X height=14.00'

validate-boost-provenance: $(BOOST_SOURCE) $(BOOST_PROVENANCE)
	@grep -Fq '128d0d2eac3f0d467e77d895d95eb716cdc16737294c689b6d9f0a57f89b3284' \
		$(BOOST_SOURCE)
	@grep -Fq '4027c0a0f5677449a640507069633a8299516dff8770f56ad484b8fb3ee45e52' \
		$(BOOST_SOURCE)
	@grep -Fq '53aa07b5b5a19d188791895feee68050200ffec113aa7e6bb2c0419c497a2d4b' \
		$(BOOST_SOURCE)
	@grep -Fq '128d0d2eac3f0d467e77d895d95eb716cdc16737294c689b6d9f0a57f89b3284' \
		$(BOOST_PROVENANCE)
	@grep -Fq '4027c0a0f5677449a640507069633a8299516dff8770f56ad484b8fb3ee45e52' \
		$(BOOST_PROVENANCE)
	@grep -Fq '53aa07b5b5a19d188791895feee68050200ffec113aa7e6bb2c0419c497a2d4b' \
		$(BOOST_PROVENANCE)
	@grep -Fq 'No Amazon image, HiLetgo artwork, third-party mesh, STEP body, or EDA file' \
		$(BOOST_PROVENANCE)
	@echo 'boost_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-mosfet-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-mosfet-scale.log; \
		mesh=$(BUILD)/intentional-mosfet-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_mosfet_pcb"' \
			-D 'MOSFET_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional MTSD001 scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Ceksezx MTSD001 model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-mosfet-registration.log; \
		mesh=$(BUILD)/intentional-mosfet-registration.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_mosfet_pcb"' \
			-D 'MOSFET_MODEL_HOLE_CENTRES=[[33.81,2.31],[33.80,15.69]]' \
			$(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional MTSD001 hole drift was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Ceksezx MTSD001 mounting registration changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-mosfet-orientation.log; \
		mesh=$(BUILD)/intentional-mosfet-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_mosfet_pcb"' \
			-D 'MOSFET_MODEL_TERMINAL_EDGE="+X"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional MTSD001 terminal reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Ceksezx MTSD001 terminal/control orientation changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'mosfet_model_guard=pass board=34.00x17.00 envelope=35.00x18.00 holes=2x2.20 terminal_edge=-X height=12.00'

validate-mosfet-provenance: $(MOSFET_SOURCE) $(MOSFET_PROVENANCE)
	@grep -Fq '42a2bc3a51587a51649d885db1ae87d65b1166c204ddd6e5e669cb8f76c5fd69' \
		$(MOSFET_SOURCE)
	@grep -Fq '6706f3e1594e2b63a8366370717503e2b09ffabacd3650f80048e746d8538fc7' \
		$(MOSFET_SOURCE)
	@grep -Fq 'cf2419bc0a5a33edcec808d35592dc417749536ee2e8cc67885f74a656c9e2a6' \
		$(MOSFET_SOURCE)
	@grep -Fq '42a2bc3a51587a51649d885db1ae87d65b1166c204ddd6e5e669cb8f76c5fd69' \
		$(MOSFET_PROVENANCE)
	@grep -Fq '6706f3e1594e2b63a8366370717503e2b09ffabacd3650f80048e746d8538fc7' \
		$(MOSFET_PROVENANCE)
	@grep -Fq 'cf2419bc0a5a33edcec808d35592dc417749536ee2e8cc67885f74a656c9e2a6' \
		$(MOSFET_PROVENANCE)
	@grep -Fq 'No Amazon image, Ceksezx artwork, third-party mesh, STEP body, or EDA file' \
		$(MOSFET_PROVENANCE)
	@echo 'mosfet_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-dp100-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-dp100-scale.log; \
		mesh=$(BUILD)/intentional-dp100-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_dp100_shell"' \
			-D 'DP100_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional DP100 scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ALIENTEK DP100 model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-dp100-nominal-body.log; \
		mesh=$(BUILD)/intentional-dp100-nominal-body.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_dp100_shell"' \
			-D 'DP100_MODEL_BODY=[100.4,62.2,17.2]' \
			$(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: nominal DP100 length replaced measured body length' >&2; exit 1; \
		fi; \
		grep -q 'ALIENTEK DP100 model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-dp100-orientation.log; \
		mesh=$(BUILD)/intentional-dp100-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_dp100_metal"' \
			-D 'DP100_MODEL_BANANA_EDGE="+X"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional DP100 connector reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ALIENTEK DP100 connector/control orientation changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-dp100-controls.log; \
		mesh=$(BUILD)/intentional-dp100-controls.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_dp100_controls"' \
			-D 'DP100_MODEL_CONTROLS_EDGE="+Y"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional DP100 control-face reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ALIENTEK DP100 connector/control orientation changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'dp100_model_guard=pass body=94.60x62.20x17.20 overall=100.40 banana=-X usb=+X controls=-Y'

validate-dp100-provenance: $(DP100_SOURCE) $(DP100_PROVENANCE)
	@grep -Fq 'd1cc4a01bcb721d4008ab76b5ed69d7946b5a39c68044a902c942d604a63ae0f' \
		$(DP100_SOURCE)
	@grep -Fq '8878f9aa3be219964c41ad3a4e679526bea54946a262fc61f35ed965d7e5f97b' \
		$(DP100_SOURCE)
	@grep -Fq 'b159077910e492e4b89ae799d4b1a33a58099f083935db80fc7cc7690488ad0f' \
		$(DP100_SOURCE)
	@grep -Fq 'd1cc4a01bcb721d4008ab76b5ed69d7946b5a39c68044a902c942d604a63ae0f' \
		$(DP100_PROVENANCE)
	@grep -Fq '8878f9aa3be219964c41ad3a4e679526bea54946a262fc61f35ed965d7e5f97b' \
		$(DP100_PROVENANCE)
	@grep -Fq 'b159077910e492e4b89ae799d4b1a33a58099f083935db80fc7cc7690488ad0f' \
		$(DP100_PROVENANCE)
	@grep -Fq 'No Amazon image, ALIENTEK artwork, manual page, third-party mesh, STEP body' \
		$(DP100_PROVENANCE)
	@echo 'dp100_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-esp32-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-esp32-scale.log; \
		mesh=$(BUILD)/intentional-esp32-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_esp32_pcb"' \
			-D 'ESP32_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional ESP32 scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ESP32 model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-esp32-orientation.log; \
		mesh=$(BUILD)/intentional-esp32-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_esp32_pcb"' \
			-D 'ESP32_MODEL_USB_EDGE="top"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional ESP32 USB rotation was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'ESP32 USB-C orientation changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'esp32_model_guard=pass scale=1 envelope=18.50x23.67 usb_edge=bottom'

validate-esp32-provenance: $(ESP32_SOURCE) $(ESP32_PROVENANCE)
	@grep -Fq '71e35b41584fda9bfad5da9fd9d21c9369f75a2d6a522343e97bd4de5327ae1d' \
		$(ESP32_SOURCE)
	@grep -Fq '71e35b41584fda9bfad5da9fd9d21c9369f75a2d6a522343e97bd4de5327ae1d' \
		$(ESP32_PROVENANCE)
	@grep -Fq 'HW-747 V0.0.2' $(ESP32_SOURCE)
	@grep -Fq 'HW-747 V0.0.2' $(ESP32_PROVENANCE)
	@echo 'esp32_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-c270-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-c270-face.log; \
		mesh=$(BUILD)/intentional-c270-face.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_c270_shell"' \
			-D 'C270_MODEL_FACE=[71.01,31.55]' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional C270 face change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'C270 model face/fixture keep-out changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-c270-orientation.log; \
		mesh=$(BUILD)/intentional-c270-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_c270_glass"' \
			-D 'C270_MODEL_LENS_DIRECTION="+Z"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional C270 lens reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'C270 lens orientation changed' $$log; \
		rm -f $$log $$mesh; \
		echo 'c270_model_guard=pass face=71.00x31.55 lens_direction=-Z lens_plane=-15.00'

validate-c270-provenance: $(C270_SOURCE) $(C270_PROVENANCE)
	@grep -Fq 'c86bc28778c52877a07cbd6ab03082dfe505215617180eb5064455f139a718ae' \
		$(C270_SOURCE)
	@grep -Fq 'ad802bc5705eceb6d75c2eb6ab4219e65e50c97678e1195910ac7b7566cd8d2b' \
		$(C270_SOURCE)
	@grep -Fq 'a69c4917c1f2964df2f6dc082827b46958a11e74ae3cda7a142e4d0bc9b4f3d8' \
		$(C270_SOURCE)
	@grep -Fq 'c86bc28778c52877a07cbd6ab03082dfe505215617180eb5064455f139a718ae' \
		$(C270_PROVENANCE)
	@grep -Fq 'ad802bc5705eceb6d75c2eb6ab4219e65e50c97678e1195910ac7b7566cd8d2b' \
		$(C270_PROVENANCE)
	@grep -Fq 'a69c4917c1f2964df2f6dc082827b46958a11e74ae3cda7a142e4d0bc9b4f3d8' \
		$(C270_PROVENANCE)
	@grep -Fq 'No Logitech image, third-party mesh, STEP body' $(C270_PROVENANCE)
	@echo 'c270_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-final-components-model-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-antenna-scale.log; \
		mesh=$(BUILD)/intentional-antenna-scale.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_antenna_dark"' \
			-D 'ANTENNA_MODEL_SCALE=1.01' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional antenna scale change was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Eightwood EWUA0205 model scale/envelope changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-vienon-orientation.log; \
		mesh=$(BUILD)/intentional-vienon-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_vienon_shell"' \
			-D 'UNPOWERED_HUB_MODEL_USB_EDGE="+Y"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional VIENON port reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'VIENON port population or orientation changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-smays-orientation.log; \
		mesh=$(BUILD)/intentional-smays-orientation.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_smays_shell"' \
			-D 'POWERED_HUB_MODEL_DC_EDGE="+Y"' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional Smays DC reversal was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Smays USB/RJ45/OTG/DC interface orientation changed' $$log; \
		rm -f $$log $$mesh
	@set -eu; log=$(BUILD)/intentional-dc-clearance.log; \
		mesh=$(BUILD)/intentional-dc-clearance.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="presentation_smays_shell"' \
			-D 'powered_hub_dc_service_origin=[147.9,27,13.0]' \
			$(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized Smays DC arch was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Smays DC plug must rise above the VIENON body before crossing it' $$log; \
		rm -f $$log $$mesh; \
		echo 'final_component_model_guard=pass antenna=114x15x3 vienon=100x30x10 ports=-Y smays=105.07x24x15 ports=+Y dc_arch=overhead'

validate-final-components-provenance: $(ANTENNA_SOURCE) $(ANTENNA_PROVENANCE) \
	$(VIENON_SOURCE) $(VIENON_PROVENANCE) \
	$(SMAYS_SOURCE) $(SMAYS_PROVENANCE)
	@grep -Fq '75dcf6792c609f9e500244ad3f05d4b624a6149340f6061efd288f906b51d473' \
		$(ANTENNA_SOURCE)
	@grep -Fq '75dcf6792c609f9e500244ad3f05d4b624a6149340f6061efd288f906b51d473' \
		$(ANTENNA_PROVENANCE)
	@grep -Fq '3c751f1dbf784083af1d7ea2ee700e7ddbccd587d77e17dfada458fb3011dc63' \
		$(VIENON_SOURCE)
	@grep -Fq '3c751f1dbf784083af1d7ea2ee700e7ddbccd587d77e17dfada458fb3011dc63' \
		$(VIENON_PROVENANCE)
	@grep -Fq '01ecb407d5862a442ac77eb52c60763db44b5067d2c55e2e0d08fc6aed7d51e5' \
		$(SMAYS_SOURCE)
	@grep -Fq '01ecb407d5862a442ac77eb52c60763db44b5067d2c55e2e0d08fc6aed7d51e5' \
		$(SMAYS_PROVENANCE)
	@grep -Fq 'geometry is redistributed.' \
		$(ANTENNA_PROVENANCE)
	@grep -Fq 'geometry is redistributed.' \
		$(VIENON_PROVENANCE)
	@grep -Fq 'geometry is redistributed.' \
		$(SMAYS_PROVENANCE)
	@echo 'final_component_provenance=pass external_geometry=not_redistributed reference_hashes=pinned'

validate-presentation-assets: $(BUILD)/pocketforge-dut-fixture-components.stl \
	$(BUILD)/pocketforge-dut-fixture-labels.stl \
	$(RELAY_COMPLETE_STL) $(RELAY_PRESENTATION_STLS) \
	$(BOOST_COMPLETE_STL) $(BOOST_PRESENTATION_STLS) \
	$(MOSFET_COMPLETE_STL) $(MOSFET_PRESENTATION_STLS) \
	$(DP100_COMPLETE_STL) $(DP100_PRESENTATION_STLS) \
	$(BPI_PRESENTATION_STLS) \
	$(ESP32_COMPLETE_STL) $(ESP32_PRESENTATION_STLS) \
	$(C270_COMPLETE_STL) $(C270_PRESENTATION_STLS) \
	$(ANTENNA_COMPLETE_STL) $(ANTENNA_BODY_STL) \
	$(ANTENNA_PRESENTATION_STLS) \
	$(VIENON_COMPLETE_STL) $(VIENON_BODY_STL) \
	$(VIENON_PRESENTATION_STLS) \
	$(SMAYS_COMPLETE_STL) $(SMAYS_BODY_STL) \
	$(SMAYS_PRESENTATION_STLS)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-dut-fixture-components.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-dut-fixture-labels.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 51.85 --max-x 51.85 \
		--min-size-y 72.70 --max-y 72.70 \
		$(RELAY_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 51.85 --max-x 51.85 \
		--min-size-y 72.70 --max-y 72.70 \
		--min-size-z 1.60 --max-z 1.60 \
		$(BUILD)/pocketforge-elegoo-relay-pcb.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-elegoo-relay-blue.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-elegoo-relay-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-elegoo-relay-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-elegoo-relay-led.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-elegoo-relay-silkscreen.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 43.16 --max-x 43.16 \
		--min-size-y 21.23 --max-y 21.23 \
		--min-size-z 14.00 --max-z 14.00 \
		$(BOOST_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 43.16 --max-x 43.16 \
		--min-size-y 21.23 --max-y 21.23 \
		--min-size-z 1.60 --max-z 1.60 \
		$(BUILD)/pocketforge-hiletgo-xl6009-pcb.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-hiletgo-xl6009-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-hiletgo-xl6009-adjuster.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-hiletgo-xl6009-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-hiletgo-xl6009-silkscreen.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 34.00 --max-x 34.00 \
		--min-size-y 17.00 --max-y 17.00 \
		--min-size-z 12.00 --max-z 12.00 \
		$(MOSFET_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 34.00 --max-x 34.00 \
		--min-size-y 17.00 --max-y 17.00 \
		--min-size-z 1.60 --max-z 1.60 \
		$(BUILD)/pocketforge-ceksezx-mtsd001-pcb.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-ceksezx-mtsd001-blue.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-ceksezx-mtsd001-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-ceksezx-mtsd001-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-ceksezx-mtsd001-led.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-ceksezx-mtsd001-silkscreen.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 100.40 --max-x 100.40 \
		--min-size-y 62.20 --max-y 62.20 \
		--min-size-z 17.20 --max-z 17.20 \
		$(DP100_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 94.60 --max-x 94.60 \
		--min-size-y 62.20 --max-y 62.20 \
		--min-size-z 17.20 --max-z 17.20 \
		$(BUILD)/pocketforge-alientek-dp100-shell.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-alientek-dp100-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-alientek-dp100-controls.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-alientek-dp100-screen.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-alientek-dp100-accent.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-alientek-dp100-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-alientek-dp100-markings.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 29.90 --max-x 29.90 \
		--min-size-y 65.00 --max-y 65.00 \
		--min-size-z 1.60 --max-z 1.60 \
		$(BUILD)/pocketforge-bpi-m2-zero-pcb.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-bpi-m2-zero-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-bpi-m2-zero-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-bpi-m2-zero-gold.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-bpi-m2-zero-silkscreen.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 18.50 --max-x 18.50 \
		--min-size-y 23.67 --max-y 23.67 \
		$(ESP32_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-esp32-s3-supermini-pcb.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-esp32-s3-supermini-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-esp32-s3-supermini-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-esp32-s3-supermini-gold.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-esp32-s3-supermini-antenna.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-esp32-s3-supermini-silkscreen.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 71.00 --max-x 71.00 \
		--min-size-y 31.55 --max-y 31.55 \
		$(C270_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-logitech-c270-shell.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-logitech-c270-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-logitech-c270-glass.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-logitech-c270-led.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-logitech-c270-labels.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 114.00 --max-x 114.00 \
		--min-size-y 15.00 --max-y 15.00 \
		--min-size-z 3.00 --max-z 3.00 \
		$(ANTENNA_BODY_STL)
	$(PYTHON) scripts/stl_bounds.py $(ANTENNA_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-eightwood-ewua0205-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-eightwood-ewua0205-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-eightwood-ewua0205-markings.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 100.00 --max-x 100.00 \
		--min-size-y 30.00 --max-y 30.00 \
		--min-size-z 10.00 --max-z 10.00 \
		$(VIENON_BODY_STL)
	$(PYTHON) scripts/stl_bounds.py $(VIENON_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-vienon-usb-001-shell.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-vienon-usb-001-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-vienon-usb-001-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-vienon-usb-001-blue.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-vienon-usb-001-led.stl
	$(PYTHON) scripts/stl_bounds.py \
		--min-size-x 105.07 --max-x 105.07 \
		--min-size-y 24.00 --max-y 24.00 \
		--min-size-z 15.00 --max-z 15.00 \
		$(SMAYS_BODY_STL)
	$(PYTHON) scripts/stl_bounds.py $(SMAYS_COMPLETE_STL)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-smays-microb-hub-8152-shell.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-smays-microb-hub-8152-dark.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-smays-microb-hub-8152-metal.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-smays-microb-hub-8152-led.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-smays-microb-hub-8152-markings.stl
	@echo 'fixture_presentation_assets=pass proxies=0 labels=10 retention_layers=1 antenna_layers=3 vienon_layers=5 smays_layers=5 relay_layers=6 boost_layers=5 mosfet_layers=6 dp100_layers=7 bpi_layers=5 esp32_layers=6 c270_layers=5'

validate: lint all split validate-overlap-guard validate-service-guard \
	validate-preview-export validate-bpi-model-guard validate-bpi-provenance \
	validate-relay-model-guard validate-relay-provenance \
	validate-boost-model-guard validate-boost-provenance \
	validate-mosfet-model-guard validate-mosfet-provenance \
	validate-dp100-model-guard validate-dp100-provenance \
	validate-esp32-model-guard validate-esp32-provenance \
	validate-c270-model-guard validate-c270-provenance \
	validate-final-components-model-guard \
	validate-final-components-provenance \
	validate-presentation-assets
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 --allow-rotate $(BUILD)/pocketforge-dut-fixture-v1.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 250 --max-y 210 $(BUILD)/fit-coupon.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate $(BUILD)/plate-lower.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate \
		--min-size-z 29.2 --max-z 29.2 $(BUILD)/plate-upper.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 20 --max-y 30 $(BUILD)/joiner.stl

clean:
	rm -rf $(BUILD)
