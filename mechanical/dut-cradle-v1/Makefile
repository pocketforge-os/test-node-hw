OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := trimui-smart-pro-s-cradle.scad

.PHONY: all lint validate validate-profile-guard validate-preview-export \
	preview clean

all: $(BUILD)/trimui-smart-pro-s-carrier.stl \
	$(BUILD)/j-hook.stl $(BUILD)/j-hook-set.stl $(BUILD)/fit-coupon.stl

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD):
	mkdir -p $@

$(BUILD)/trimui-smart-pro-s-carrier.stl: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

$(BUILD)/j-hook.stl: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook"' $<

$(BUILD)/j-hook-set.stl: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook_set"' $<

$(BUILD)/fit-coupon.stl: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' $<

$(BUILD)/assembly-export.stl: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(BUILD)/layout-preview.png: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' $<

$(BUILD)/layout-top.png: $(SOURCE) lib/dut-cradle-library.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --autocenter --viewall \
		--camera=123.5,100,380,123.5,100,0 \
		-D 'PART="assembly"' $<

preview: $(BUILD)/layout-preview.png $(BUILD)/layout-top.png

validate-profile-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-throat.log; mesh=$(BUILD)/invalid-throat.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="hook"' \
			-D 'hook_throat=11.5' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized hook throat was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Hook throat must retain the DUT with positive clearance' $$log; \
		rm -f $$log $$mesh; \
		echo 'profile_guard=pass case=undersized_hook_throat'

validate-preview-export: $(BUILD)/trimui-smart-pro-s-carrier.stl \
	$(BUILD)/assembly-export.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(BUILD)/trimui-smart-pro-s-carrier.stl \
		$(BUILD)/assembly-export.stl
	@echo 'preview_export_guard=pass ghosts=excluded'

validate: lint all validate-profile-guard validate-preview-export
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 \
		$(BUILD)/trimui-smart-pro-s-carrier.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 30 --max-z 12 \
		$(BUILD)/j-hook.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 80 --max-y 80 --max-z 12 \
		$(BUILD)/j-hook-set.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 80 --max-y 80 --max-z 12 \
		$(BUILD)/fit-coupon.stl

clean:
	rm -rf $(BUILD)
