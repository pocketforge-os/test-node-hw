OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := dut-fixture.scad
BPI_SOURCE := bpi-m2-zero-v1.scad
BPI_PROVENANCE := BPI-M2-ZERO-PROVENANCE.md
ESP32_SOURCE := esp32-s3-supermini-hw747-v0.0.2.scad
ESP32_PROVENANCE := ESP32-S3-SUPERMINI-PROVENANCE.md
BPI_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-bpi-m2-zero-pcb.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-dark.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-metal.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-gold.stl \
	$(BUILD)/pocketforge-bpi-m2-zero-silkscreen.stl
ESP32_PRESENTATION_STLS := \
	$(BUILD)/pocketforge-esp32-s3-supermini-pcb.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-dark.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-metal.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-gold.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-antenna.stl \
	$(BUILD)/pocketforge-esp32-s3-supermini-silkscreen.stl
ESP32_COMPLETE_STL := $(BUILD)/pocketforge-esp32-s3-supermini-complete.stl

.PHONY: all lint validate validate-overlap-guard validate-service-guard \
	validate-preview-export validate-presentation-assets \
	validate-bpi-model-guard validate-bpi-provenance \
	validate-esp32-model-guard validate-esp32-provenance preview split clean

all: $(BUILD)/pocketforge-dut-fixture-v1.stl $(BUILD)/fit-coupon.stl

# Repository-wide CSG export is the fast parse/evaluation gate. The wrapper
# also rejects OpenSCAD ERROR diagnostics because CSG assertion failures may
# otherwise return a successful process status.
lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD):
	mkdir -p $@

$(BUILD)/pocketforge-dut-fixture-v1.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/pocketforge-dut-fixture-components.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_components"' $<

$(BUILD)/pocketforge-dut-fixture-labels.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
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

$(BUILD)/fit-coupon.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/preview-export.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/plate-lower.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_lower"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/plate-upper.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_upper"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/joiner.stl: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="joiner"' -D 'SHOW_COMPONENTS=false' $<

split: $(BUILD)/plate-lower.stl $(BUILD)/plate-upper.stl $(BUILD)/joiner.stl

$(BUILD)/layout-preview.png: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho --viewall \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/layout-top.png: $(SOURCE) $(BPI_SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho \
		--autocenter --viewall --camera=100,120,400,100,120,0 \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/layout-bpi-m2-zero.png: $(SOURCE) $(BPI_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1400 --projection=ortho \
		--viewall --camera=29,60,115,29,117,10 \
		-D 'PART="presentation_bpi"' $<

$(BUILD)/layout-esp32-s3-supermini.png: $(SOURCE) $(ESP32_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1400 --projection=ortho \
		--viewall --camera=17,68,65,17,68,8 \
		-D 'PART="presentation_esp32"' $<

preview: $(BUILD)/layout-preview.png $(BUILD)/layout-top.png \
	$(BUILD)/layout-bpi-m2-zero.png $(BUILD)/layout-esp32-s3-supermini.png

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

validate-presentation-assets: $(BUILD)/pocketforge-dut-fixture-components.stl \
	$(BUILD)/pocketforge-dut-fixture-labels.stl $(BPI_PRESENTATION_STLS) \
	$(ESP32_COMPLETE_STL) $(ESP32_PRESENTATION_STLS)
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-dut-fixture-components.stl
	$(PYTHON) scripts/stl_bounds.py $(BUILD)/pocketforge-dut-fixture-labels.stl
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
	@echo 'fixture_presentation_assets=pass proxies=8 labels=10 bpi_layers=5 esp32_layers=6'

validate: lint all split validate-overlap-guard validate-service-guard \
	validate-preview-export validate-bpi-model-guard validate-bpi-provenance \
	validate-esp32-model-guard validate-esp32-provenance \
	validate-presentation-assets
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 --allow-rotate $(BUILD)/pocketforge-dut-fixture-v1.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 250 --max-y 210 $(BUILD)/fit-coupon.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate $(BUILD)/plate-lower.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate \
		--min-size-z 29.2 --max-z 29.2 $(BUILD)/plate-upper.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 20 --max-y 30 $(BUILD)/joiner.stl

clean:
	rm -rf $(BUILD)
