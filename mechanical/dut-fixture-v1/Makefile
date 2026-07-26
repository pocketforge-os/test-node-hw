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
ESP32_SOURCE := esp32-s3-supermini-hw747-v0.0.2.scad
ESP32_PROVENANCE := ESP32-S3-SUPERMINI-PROVENANCE.md
C270_SOURCE := logitech-c270.scad
C270_PROVENANCE := LOGITECH-C270-PROVENANCE.md
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

.PHONY: all lint validate validate-overlap-guard validate-service-guard \
	validate-preview-export validate-presentation-assets \
	validate-bpi-model-guard validate-bpi-provenance \
	validate-relay-model-guard validate-relay-provenance \
	validate-boost-model-guard validate-boost-provenance \
	validate-esp32-model-guard validate-esp32-provenance \
	validate-c270-model-guard validate-c270-provenance preview split clean

all: $(BUILD)/pocketforge-dut-fixture-v1.stl $(BUILD)/fit-coupon.stl

# Repository-wide CSG export is the fast parse/evaluation gate. The wrapper
# also rejects OpenSCAD ERROR diagnostics because CSG assertion failures may
# otherwise return a successful process status.
lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD):
	mkdir -p $@

$(BUILD)/pocketforge-dut-fixture-v1.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/pocketforge-dut-fixture-components.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_components"' $<

$(BUILD)/pocketforge-dut-fixture-labels.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
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

$(BUILD)/fit-coupon.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/preview-export.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/plate-lower.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_lower"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/plate-upper.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_upper"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/joiner.stl: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="joiner"' -D 'SHOW_COMPONENTS=false' $<

split: $(BUILD)/plate-lower.stl $(BUILD)/plate-upper.stl $(BUILD)/joiner.stl

$(BUILD)/layout-preview.png: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho --viewall \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/layout-top.png: $(SOURCE) $(BPI_SOURCE) $(RELAY_SOURCE) $(BOOST_SOURCE) $(ESP32_SOURCE) $(C270_SOURCE) | $(BUILD)
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

$(BUILD)/layout-esp32-s3-supermini.png: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1400 --projection=ortho \
		--viewall --camera=17,68,65,17,68,8 \
		-D 'PART="presentation_esp32"' $<

$(BUILD)/layout-logitech-c270.png: $(SOURCE) $(C270_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 --projection=ortho \
		--viewall --camera=100,85,-130,100,132,-5 \
		-D 'PART="presentation_c270"' $<

preview: $(BUILD)/layout-preview.png $(BUILD)/layout-top.png \
	$(BUILD)/layout-bpi-m2-zero.png $(BUILD)/layout-elegoo-relay.png \
	$(BUILD)/layout-hiletgo-xl6009.png \
	$(BUILD)/layout-esp32-s3-supermini.png \
	$(BUILD)/layout-logitech-c270.png

validate-overlap-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-overlap.log; mesh=$(BUILD)/intentional-overlap.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="fit_coupon"' \
			-D 'antenna_origin=[50,160]' $(SOURCE) >$$log 2>&1; then \
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

validate-presentation-assets: $(BUILD)/pocketforge-dut-fixture-components.stl \
	$(BUILD)/pocketforge-dut-fixture-labels.stl \
	$(RELAY_COMPLETE_STL) $(RELAY_PRESENTATION_STLS) \
	$(BOOST_COMPLETE_STL) $(BOOST_PRESENTATION_STLS) \
	$(BPI_PRESENTATION_STLS) \
	$(ESP32_COMPLETE_STL) $(ESP32_PRESENTATION_STLS) \
	$(C270_COMPLETE_STL) $(C270_PRESENTATION_STLS)
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
	@echo 'fixture_presentation_assets=pass proxies=5 labels=10 relay_layers=6 boost_layers=5 bpi_layers=5 esp32_layers=6 c270_layers=5'

validate: lint all split validate-overlap-guard validate-service-guard \
	validate-preview-export validate-bpi-model-guard validate-bpi-provenance \
	validate-relay-model-guard validate-relay-provenance \
	validate-boost-model-guard validate-boost-provenance \
	validate-esp32-model-guard validate-esp32-provenance \
	validate-c270-model-guard validate-c270-provenance \
	validate-presentation-assets
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 --allow-rotate $(BUILD)/pocketforge-dut-fixture-v1.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 250 --max-y 210 $(BUILD)/fit-coupon.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate $(BUILD)/plate-lower.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate \
		--min-size-z 29.2 --max-z 29.2 $(BUILD)/plate-upper.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 20 --max-y 30 $(BUILD)/joiner.stl

clean:
	rm -rf $(BUILD)
