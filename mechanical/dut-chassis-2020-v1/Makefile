OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
SOURCE := pocketforge-node-chassis.scad
BOUNDS := ../dut-cradle-v1/scripts/stl_bounds.py
FIXTURE_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-v1.stl
CRADLE_STL := ../dut-cradle-v1/build/trimui-smart-pro-carrier.stl
PRESENTATION_IMPORT_DIR := $(BUILD)/imports
PRESENTATION_FIXTURE_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-v1.stl
PRESENTATION_CRADLE_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-carrier.stl
CUT_LIST := CUT_LIST.md

PRINTABLES := \
	$(BUILD)/device-id-placard.stl \
	$(BUILD)/placard-riser.stl \
	$(BUILD)/placard-riser-pair.stl \
	$(BUILD)/placard-spacer.stl \
	$(BUILD)/placard-spacer-pair.stl \
	$(BUILD)/plate-spacer.stl \
	$(BUILD)/plate-spacer-set.stl \
	$(BUILD)/gantry-joint-plate.stl \
	$(BUILD)/gantry-joint-plate-set.stl \
	$(BUILD)/stacking-registration-tab.stl \
	$(BUILD)/stacking-registration-tab-set.stl \
	$(BUILD)/rail-fit-coupon.stl \
	$(BUILD)/m3-twist-nut-carrier.stl \
	$(BUILD)/m3-twist-nut-carrier-set.stl \
	$(BUILD)/m3-twist-nut-fit-coupon.stl \
	$(BUILD)/print-group-01-calibration.stl \
	$(BUILD)/print-group-02-gantry-hardware.stl \
	$(BUILD)/print-group-03-plate-mounts.stl \
	$(BUILD)/print-group-04-stacking-guides.stl \
	$(BUILD)/print-group-05-device-label.stl

.NOTPARALLEL:

.PHONY: all lint preview presentation-assets cutlist refresh-cut-list \
	validate-cut-list-sync \
	validate validate-margin-guard \
	validate-fov-guard validate-nut-carrier-guard \
	validate-gantry-travel-guard clean

all: $(PRINTABLES) cutlist

$(BUILD):
	mkdir -p $@

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD)/device-id-placard.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
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

$(BUILD)/gantry-joint-plate.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="gantry_joint_plate"' $<

$(BUILD)/gantry-joint-plate-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="gantry_joint_plate_set"' $<

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

$(BUILD)/print-group-01-calibration.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="print_group_calibration"' $<

$(BUILD)/print-group-02-gantry-hardware.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="print_group_gantry_hardware"' $<

$(BUILD)/print-group-03-plate-mounts.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="print_group_plate_mounts"' $<

$(BUILD)/print-group-04-stacking-guides.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="print_group_stacking_guides"' $<

$(BUILD)/print-group-05-device-label.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="print_group_device_label"' $<

$(FIXTURE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-v1.stl

$(CRADLE_STL):
	$(MAKE) -C ../dut-cradle-v1 build/trimui-smart-pro-carrier.stl

$(PRESENTATION_IMPORT_DIR):
	mkdir -p $@

$(PRESENTATION_FIXTURE_STL): $(FIXTURE_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_CRADLE_STL): $(CRADLE_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

presentation-assets: $(PRESENTATION_FIXTURE_STL) $(PRESENTATION_CRADLE_STL)

$(BUILD)/layout-assembly.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' \
		-D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-assembly-mesh.png: $(SOURCE) lib/pf-2020.scad \
	$(PRESENTATION_FIXTURE_STL) $(PRESENTATION_CRADLE_STL) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="presentation"' $<

$(BUILD)/layout-front.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall --camera=200,-500,220,200,200,220 \
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

$(BUILD)/layout-gantry-joint-plate.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,800 \
		--projection=ortho --viewall --camera=55,-70,55,42,22,1 \
		-D 'PART="gantry_joint_plate_set"' $<

$(BUILD)/layout-print-group-01.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,800 \
		--projection=ortho --viewall \
		-D 'PART="print_group_calibration"' $<

$(BUILD)/layout-print-group-02.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,900 \
		--projection=ortho --viewall \
		-D 'PART="print_group_gantry_hardware"' $<

$(BUILD)/layout-print-group-03.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,800 \
		--projection=ortho --viewall \
		-D 'PART="print_group_plate_mounts"' $<

$(BUILD)/layout-print-group-04.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1200 \
		--projection=ortho --viewall \
		-D 'PART="print_group_stacking_guides"' $<

$(BUILD)/layout-print-group-05.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,600 \
		--projection=ortho --viewall \
		-D 'PART="print_group_device_label"' $<

preview: $(BUILD)/layout-assembly.png $(BUILD)/layout-assembly-mesh.png \
	$(BUILD)/layout-front.png $(BUILD)/layout-stacked.png \
	$(BUILD)/layout-m3-twist-nut.png \
	$(BUILD)/layout-m3-twist-nut-coupon.png \
	$(BUILD)/layout-gantry-joint-plate.png \
	$(BUILD)/layout-print-group-01.png \
	$(BUILD)/layout-print-group-02.png \
	$(BUILD)/layout-print-group-03.png \
	$(BUILD)/layout-print-group-04.png \
	$(BUILD)/layout-print-group-05.png

$(BUILD)/cutlist.log: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $(BUILD)/cutlist.csg \
		-D 'PART="cutlist"' $< >$(BUILD)/cutlist.stdout 2>$@

$(BUILD)/cut-list.csv $(BUILD)/cut-list.md &: $(BUILD)/cutlist.log scripts/cutlist.py
	$(PYTHON) scripts/cutlist.py --input $(BUILD)/cutlist.log \
		--csv $(BUILD)/cut-list.csv --markdown $(BUILD)/cut-list.md

cutlist: $(BUILD)/cut-list.csv $(BUILD)/cut-list.md

refresh-cut-list: cutlist
	cp $(BUILD)/cut-list.md $(CUT_LIST)

validate-cut-list-sync: cutlist
	@cmp -s $(BUILD)/cut-list.md $(CUT_LIST) || { \
		echo 'ERROR: CUT_LIST.md is stale; run make refresh-cut-list' >&2; \
		diff -u $(CUT_LIST) $(BUILD)/cut-list.md || true; \
		exit 1; \
	}
	@echo 'cut_list_sync=pass artifact=$(CUT_LIST)'

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

validate-gantry-travel-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-gantry-travel.log; \
		mesh=$(BUILD)/invalid-gantry-travel.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="gantry_joint_plate"' \
			-D 'fixture_gantry_y=20' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: out-of-range gantry was not rejected' >&2; exit 1; \
		fi; \
	grep -q 'Fixture gantry Y is outside legal travel' $$log; \
	collision_log=$(BUILD)/invalid-gantry-collision.log; \
		collision_mesh=$(BUILD)/invalid-gantry-collision.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$collision_mesh \
			-D 'PART="gantry_joint_plate"' \
			-D 'fixture_gantry_y=200' -D 'cradle_gantry_y=210' \
			$(SOURCE) >$$collision_log 2>&1; then \
			echo 'ERROR: intersecting gantries were not rejected' >&2; exit 1; \
		fi; \
	grep -q 'gantries must not intersect' $$collision_log; \
	echo 'gantry_guards=pass rejected_y=20mm rejected_overlap=10mm'

validate: lint all preview validate-margin-guard validate-fov-guard \
	validate-nut-carrier-guard validate-gantry-travel-guard \
	validate-cut-list-sync
	$(PYTHON) $(BOUNDS) --max-x 180 --max-y 60 --max-z 6 \
		$(BUILD)/device-id-placard.stl
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
	$(PYTHON) $(BOUNDS) --max-x 40 --max-y 50 --max-z 8 \
		$(BUILD)/gantry-joint-plate.stl
	$(PYTHON) $(BOUNDS) --max-x 170 --max-y 100 --max-z 8 \
		$(BUILD)/gantry-joint-plate-set.stl
	$(PYTHON) $(BOUNDS) --max-x 30 --max-y 80 --max-z 6 \
		$(BUILD)/stacking-registration-tab.stl
	$(PYTHON) $(BOUNDS) --max-x 130 --max-y 170 --max-z 6 \
		$(BUILD)/stacking-registration-tab-set.stl
	$(PYTHON) $(BOUNDS) --max-x 80 --max-y 40 --max-z 10 \
		$(BUILD)/rail-fit-coupon.stl
	$(PYTHON) $(BOUNDS) --max-x 15 --max-y 10 --max-z 6 \
		$(BUILD)/m3-twist-nut-carrier.stl
	$(PYTHON) $(BOUNDS) --max-x 130 --max-y 30 --max-z 6 \
		$(BUILD)/m3-twist-nut-carrier-set.stl
	$(PYTHON) $(BOUNDS) --max-x 45 --max-y 10 --max-z 6 \
		$(BUILD)/m3-twist-nut-fit-coupon.stl
	$(PYTHON) $(BOUNDS) --max-x 80 --max-y 55 --max-z 10 \
		$(BUILD)/print-group-01-calibration.stl
	$(PYTHON) $(BOUNDS) --max-x 170 --max-y 135 --max-z 8 \
		$(BUILD)/print-group-02-gantry-hardware.stl
	$(PYTHON) $(BOUNDS) --max-x 150 --max-y 90 --max-z 8 \
		$(BUILD)/print-group-03-plate-mounts.stl
	$(PYTHON) $(BOUNDS) --max-x 130 --max-y 170 --max-z 6 \
		$(BUILD)/print-group-04-stacking-guides.stl
	$(PYTHON) $(BOUNDS) --max-x 180 --max-y 60 --max-z 6 \
		$(BUILD)/print-group-05-device-label.stl
	grep -q '^outer_vertical_rail,4,360.00,1440.00' $(BUILD)/cut-list.csv
	@test "$$(grep -c ',4,360.00,1440.00,' $(BUILD)/cut-list.csv)" -eq 5
	grep -q 'Stock bars required: \*\*10\*\*' $(BUILD)/cut-list.md
	@echo 'chassis_validation=pass printable_outputs=20 stock_bars=10'

clean:
	rm -rf $(BUILD)
