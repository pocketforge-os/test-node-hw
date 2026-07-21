OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := pocketforge-node-chassis.scad
BOUNDS := ../dut-cradle-v1/scripts/stl_bounds.py
FIXTURE_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-v1.stl
CRADLE_STL := ../dut-cradle-v1/build/trimui-smart-pro-carrier.stl

PRINTABLES := \
	$(BUILD)/rear-id-placard.stl \
	$(BUILD)/placard-riser.stl \
	$(BUILD)/placard-riser-pair.stl \
	$(BUILD)/placard-spacer.stl \
	$(BUILD)/placard-spacer-pair.stl \
	$(BUILD)/plate-spacer.stl \
	$(BUILD)/plate-spacer-set.stl \
	$(BUILD)/stacking-registration-tab.stl \
	$(BUILD)/stacking-registration-tab-set.stl \
	$(BUILD)/rail-fit-coupon.stl \
	$(BUILD)/m3-twist-nut-carrier.stl \
	$(BUILD)/m3-twist-nut-carrier-set.stl \
	$(BUILD)/m3-twist-nut-fit-coupon.stl

.NOTPARALLEL:

.PHONY: all lint preview cutlist validate validate-margin-guard \
	validate-fov-guard validate-nut-carrier-guard clean

all: $(PRINTABLES) cutlist

$(BUILD):
	mkdir -p $@

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD)/rear-id-placard.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard"' $<

$(BUILD)/placard-riser.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard_riser"' $<

$(BUILD)/placard-riser-pair.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard_riser_pair"' $<

$(BUILD)/placard-spacer.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard_spacer"' $<

$(BUILD)/placard-spacer-pair.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard_spacer_pair"' $<

$(BUILD)/plate-spacer.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_spacer"' $<

$(BUILD)/plate-spacer-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate_spacer_set"' $<

$(BUILD)/stacking-registration-tab.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="registration_tab"' $<

$(BUILD)/stacking-registration-tab-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="registration_tab_set"' $<

$(BUILD)/rail-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="rail_fit_coupon"' $<

$(BUILD)/m3-twist-nut-carrier.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_twist_nut"' $<

$(BUILD)/m3-twist-nut-carrier-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_twist_nut_set"' $<

$(BUILD)/m3-twist-nut-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_twist_nut_coupon"' $<

$(FIXTURE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-v1.stl

$(CRADLE_STL):
	$(MAKE) -C ../dut-cradle-v1 build/trimui-smart-pro-carrier.stl

$(BUILD)/layout-assembly.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' \
		-D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-assembly-mesh.png: $(SOURCE) lib/pf-2020.scad \
	$(FIXTURE_STL) $(CRADLE_STL) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' \
		-D 'PLATE_DETAIL="mesh"' $<

$(BUILD)/layout-rear.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall --camera=200,900,220,200,200,220 \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-stacked.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 \
		--projection=ortho --viewall -D 'PART="stacked_assembly"' \
		-D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-m3-twist-nut.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,800 \
		--projection=ortho --viewall --camera=18,-24,18,0,0,1 \
		-D 'PART="m3_twist_nut"' $<

$(BUILD)/layout-m3-twist-nut-coupon.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,700 \
		--projection=ortho --viewall --camera=35,-40,25,14,0,1 \
		-D 'PART="m3_twist_nut_coupon"' $<

preview: $(BUILD)/layout-assembly.png $(BUILD)/layout-assembly-mesh.png \
	$(BUILD)/layout-rear.png $(BUILD)/layout-stacked.png \
	$(BUILD)/layout-m3-twist-nut.png \
	$(BUILD)/layout-m3-twist-nut-coupon.png

$(BUILD)/cutlist.log: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $(BUILD)/cutlist.csg \
		-D 'PART="cutlist"' $< >$(BUILD)/cutlist.stdout 2>$@

$(BUILD)/cut-list.csv $(BUILD)/cut-list.md &: $(BUILD)/cutlist.log scripts/cutlist.py
	$(PYTHON) scripts/cutlist.py --input $(BUILD)/cutlist.log \
		--csv $(BUILD)/cut-list.csv --markdown $(BUILD)/cut-list.md

cutlist: $(BUILD)/cut-list.csv $(BUILD)/cut-list.md

validate-margin-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-margin.log; mesh=$(BUILD)/invalid-margin.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="placard_spacer"' \
			-D 'frame_outer=[380,380,380]' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized routing margin was not rejected' >&2; exit 1; \
		fi; \
	grep -q 'routing margin fell below 50 mm' $$log; \
	echo 'routing_margin_guard=pass frame=380mm'

validate-fov-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-fov.log; mesh=$(BUILD)/invalid-fov.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="placard_spacer"' \
			-D 'camera_diagonal_fov=40' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: narrow camera FOV was not rejected' >&2; exit 1; \
		fi; \
	grep -q 'Estimated horizontal FOV is too narrow' $$log; \
	echo 'camera_fov_guard=pass diagonal_fov=40deg'

validate-nut-carrier-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-nut-carrier.log; \
		mesh=$(BUILD)/invalid-nut-carrier.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="m3_twist_nut"' \
			-D 'm3_twist_nut_width=6.8' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: oversized carrier was not rejected' >&2; exit 1; \
		fi; \
	grep -q 'pass through the measured slot mouth' $$log; \
	echo 'nut_carrier_guard=pass rejected_width=6.8mm'

validate: lint all preview validate-margin-guard validate-fov-guard \
	validate-nut-carrier-guard
	$(PYTHON) $(BOUNDS) --max-x 180 --max-y 60 --max-z 6 \
		$(BUILD)/rear-id-placard.stl
	$(PYTHON) $(BOUNDS) --max-x 30 --max-y 70 --max-z 6 \
		$(BUILD)/placard-riser.stl
	$(PYTHON) $(BOUNDS) --max-x 60 --max-y 70 --max-z 6 \
		$(BUILD)/placard-riser-pair.stl
	$(PYTHON) $(BOUNDS) --max-x 30 --max-y 30 --max-z 8 \
		$(BUILD)/placard-spacer.stl
	$(PYTHON) $(BOUNDS) --max-x 30 --max-y 30 --max-z 8 \
		$(BUILD)/plate-spacer.stl
	$(PYTHON) $(BOUNDS) --max-x 60 --max-y 30 --max-z 8 \
		$(BUILD)/placard-spacer-pair.stl
	$(PYTHON) $(BOUNDS) --max-x 120 --max-y 60 --max-z 8 \
		$(BUILD)/plate-spacer-set.stl
	$(PYTHON) $(BOUNDS) --max-x 30 --max-y 80 --max-z 6 \
		$(BUILD)/stacking-registration-tab.stl
	$(PYTHON) $(BOUNDS) --max-x 130 --max-y 170 --max-z 6 \
		$(BUILD)/stacking-registration-tab-set.stl
	$(PYTHON) $(BOUNDS) --max-x 80 --max-y 40 --max-z 10 \
		$(BUILD)/rail-fit-coupon.stl
	$(PYTHON) $(BOUNDS) --max-x 15 --max-y 10 --max-z 6 \
		$(BUILD)/m3-twist-nut-carrier.stl
	$(PYTHON) $(BOUNDS) --max-x 70 --max-y 20 --max-z 6 \
		$(BUILD)/m3-twist-nut-carrier-set.stl
	$(PYTHON) $(BOUNDS) --max-x 45 --max-y 10 --max-z 6 \
		$(BUILD)/m3-twist-nut-fit-coupon.stl
	grep -q '^outer_vertical_rail,4,360.00,1440.00' $(BUILD)/cut-list.csv
	@test "$$(grep -c ',4,360.00,1440.00,' $(BUILD)/cut-list.csv)" -eq 4
	grep -q 'Stock bars required: \*\*8\*\*' $(BUILD)/cut-list.md
	@echo 'chassis_validation=pass printable_parts=13 stock_bars=8'

clean:
	rm -rf $(BUILD)
