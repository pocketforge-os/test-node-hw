OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := dut-fixture.scad

.PHONY: all validate preview split clean

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
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 --projection=ortho --viewall \
		-D 'PART="preview"' -D 'SHOW_COMPONENTS=true' $<

preview: $(BUILD)/layout-preview.png

validate: all split
	$(PYTHON) scripts/stl_bounds.py --max-x 250 --max-y 210 $(BUILD)/pocketforge-dut-fixture-v1.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 250 --max-y 210 $(BUILD)/fit-coupon.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 125 --max-y 210 $(BUILD)/plate-left.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 125 --max-y 210 $(BUILD)/plate-right.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 20 $(BUILD)/joiner.stl

clean:
	rm -rf $(BUILD)
