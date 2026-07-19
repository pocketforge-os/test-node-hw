OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := dut-fixture.scad

.PHONY: all validate validate-overlap-guard preview split clean

all: $(BUILD)/pocketforge-dut-fixture-v1.stl $(BUILD)/fit-coupon.stl

$(BUILD):
	mkdir -p $@

$(BUILD)/pocketforge-dut-fixture-v1.stl: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/fit-coupon.stl: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/plate-left.stl: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_left"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/plate-right.stl: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_right"' -D 'SHOW_COMPONENTS=false' $<

$(BUILD)/joiner.stl: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="joiner"' -D 'SHOW_COMPONENTS=false' $<

split: $(BUILD)/plate-left.stl $(BUILD)/plate-right.stl $(BUILD)/joiner.stl

$(BUILD)/layout-preview.png: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho --viewall \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

$(BUILD)/layout-top.png: $(SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 --projection=ortho \
		--autocenter --viewall --camera=100,120,400,100,120,0 \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

preview: $(BUILD)/layout-preview.png $(BUILD)/layout-top.png

validate-overlap-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/intentional-overlap.log; mesh=$(BUILD)/intentional-overlap.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="fit_coupon"' \
			-D 'antenna_origin=[50,122]' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: intentional component overlap was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Component envelope clearance violation: relay vs antenna' $$log; \
		rm -f $$log $$mesh; \
		echo 'layout_overlap_guard=pass pair=relay_vs_antenna'

validate: all split validate-overlap-guard
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate $(BUILD)/pocketforge-dut-fixture-v1.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 250 --max-y 210 $(BUILD)/fit-coupon.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate $(BUILD)/plate-left.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 250 --bed-y 210 --allow-rotate $(BUILD)/plate-right.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 20 $(BUILD)/joiner.stl

clean:
	rm -rf $(BUILD)
