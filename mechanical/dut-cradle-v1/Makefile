OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PREVIEW_SETTLE ?= sleep 1
PYTHON ?= python3
BUILD := build
CHECKS := $(BUILD)/checks
LIBRARY := lib/dut-cradle-library.scad
FAMILY_SOURCE := trimui-smart-pro-family-cradle.scad
SMART_PRO_S_SOURCE := trimui-smart-pro-s-cradle.scad
SMART_PRO_SOURCE := trimui-smart-pro-cradle.scad
BRICK_SOURCE := trimui-brick-cradle.scad

# OpenSCAD 2021.01 can corrupt a back-to-back off-screen PNG frame while its
# previous GL context is settling. Serialize previews and leave a short gap.
.NOTPARALLEL:

.PHONY: all lint validate validate-profile-guard validate-rear-gap-guard \
	validate-nut-capture-guard validate-family-equivalence \
	validate-preview-export validate-brick-flat-datum-guard \
	validate-brick-clearance-guard validate-brick-side-contact-guard \
	validate-brick-label-clearance-guard validate-brick-preview-export \
	preview clean

all: $(BUILD)/trimui-smart-pro-s-carrier.stl \
	$(BUILD)/trimui-smart-pro-carrier.stl \
	$(BUILD)/j-hook.stl $(BUILD)/j-hook-set.stl $(BUILD)/fit-coupon.stl \
	$(BUILD)/trimui-brick-carrier.stl \
	$(BUILD)/trimui-brick-lower-hook.stl \
	$(BUILD)/trimui-brick-upper-hook.stl \
	$(BUILD)/trimui-brick-hook-set.stl \
	$(BUILD)/trimui-brick-fit-coupon.stl

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD) $(CHECKS):
	mkdir -p $@

$(BUILD)/trimui-smart-pro-s-carrier.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

$(BUILD)/trimui-smart-pro-carrier.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

$(BUILD)/j-hook.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook"' $<

$(BUILD)/j-hook-set.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook_set"' $<

$(BUILD)/fit-coupon.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' $<

$(BUILD)/trimui-brick-carrier.stl: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

$(BUILD)/trimui-brick-lower-hook.stl: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="lower_hook"' $<

$(BUILD)/trimui-brick-upper-hook.stl: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="upper_hook"' $<

$(BUILD)/trimui-brick-hook-set.stl: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook_set"' $<

$(BUILD)/trimui-brick-fit-coupon.stl: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' $<

$(CHECKS)/smart-pro-s-assembly-export.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/smart-pro-assembly-export.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/brick-assembly-export.stl: $(BRICK_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/smart-pro-s-unlabelled.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_LABELS=false' $<

$(CHECKS)/smart-pro-unlabelled.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_LABELS=false' $<

$(BUILD)/layout-smart-pro-s-preview.png: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' $<

$(BUILD)/layout-smart-pro-s-top.png: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --camera=123.5,100,900,123.5,100,0 \
		-D 'PART="assembly"' $<

$(BUILD)/layout-smart-pro-preview.png: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' $<

$(BUILD)/layout-smart-pro-top.png: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --camera=123.5,100,900,123.5,100,0 \
		-D 'PART="assembly"' $<

$(BUILD)/layout-trimui-brick-preview.png: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1400 \
		--projection=ortho --viewall -D 'PART="assembly"' $<

$(BUILD)/layout-trimui-brick-top.png: $(BRICK_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1400 \
		--projection=ortho --camera=74,102.5,700,74,102.5,0 \
		-D 'PART="assembly"' $<

preview: $(BUILD)/layout-smart-pro-s-preview.png \
	$(BUILD)/layout-smart-pro-s-top.png \
	$(BUILD)/layout-smart-pro-preview.png \
	$(BUILD)/layout-smart-pro-top.png \
	$(BUILD)/layout-trimui-brick-preview.png \
	$(BUILD)/layout-trimui-brick-top.png

validate-profile-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-throat.log; mesh=$(BUILD)/invalid-throat.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="hook"' \
			-D 'hook_throat=10.6' $(FAMILY_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized hook throat was not rejected' >&2; exit 1; \
		fi; \
		grep -q 'Hook throat must retain the DUT with positive clearance' $$log; \
		rm -f $$log $$mesh; \
		echo 'profile_guard=pass case=undersized_hook_throat'

validate-rear-gap-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-rear-gap.log; mesh=$(BUILD)/invalid-rear-gap.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="hook"' \
			-D 'device_rear_gap=10.0' $(FAMILY_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized rear carrier gap was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'Rear carrier gap must preserve the owner-validated trigger clearance' $$log; \
		rm -f $$log $$mesh; \
		echo 'rear_gap_guard=pass case=undersized_trigger_clearance'

validate-nut-capture-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-nut-capture.log; \
		mesh=$(BUILD)/invalid-nut-capture.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="hook"' \
			-D 'm3_nut_capture_wall=1.6' $(FAMILY_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized nut capture wall was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'M3 nut capture wall must remain at least three 0.8 mm nozzle widths' $$log; \
		rm -f $$log $$mesh; \
		echo 'nut_capture_guard=pass case=undersized_capture_wall'

validate-family-equivalence: $(CHECKS)/smart-pro-s-unlabelled.stl \
	$(CHECKS)/smart-pro-unlabelled.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(CHECKS)/smart-pro-s-unlabelled.stl \
		$(CHECKS)/smart-pro-unlabelled.stl
	@echo 'family_equivalence_guard=pass differences=labels_only'

validate-preview-export: $(BUILD)/trimui-smart-pro-s-carrier.stl \
	$(BUILD)/trimui-smart-pro-carrier.stl \
	$(CHECKS)/smart-pro-s-assembly-export.stl \
	$(CHECKS)/smart-pro-assembly-export.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(BUILD)/trimui-smart-pro-s-carrier.stl \
		$(CHECKS)/smart-pro-s-assembly-export.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(BUILD)/trimui-smart-pro-carrier.stl \
		$(CHECKS)/smart-pro-assembly-export.stl
	@echo 'preview_export_guard=pass models=smart_pro_s,smart_pro ghosts=excluded'

validate-brick-flat-datum-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-brick-datum.log; \
		mesh=$(BUILD)/invalid-brick-datum.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="lower_hook"' \
			-D 'upper_rear_gap=17.0' $(BRICK_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: misaligned Brick front datum was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'Brick front contact plane must remain flat across shell step' $$log; \
		rm -f $$log $$mesh; \
		echo 'brick_flat_datum_guard=pass case=misaligned_step_supports'

validate-brick-clearance-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-brick-clearance.log; \
		mesh=$(BUILD)/invalid-brick-clearance.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="lower_hook"' \
			-D 'lower_rear_gap=7.5' $(BRICK_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized Brick finger clearance was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'Brick lower rear gap must preserve finger access' $$log; \
		rm -f $$log $$mesh; \
		echo 'brick_clearance_guard=pass case=undersized_rear_access'

validate-brick-side-contact-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-brick-side-contact.log; \
		mesh=$(BUILD)/invalid-brick-side-contact.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="lower_hook"' \
			-D 'lower_side_contact_height=12.0' $(BRICK_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: Brick side contact overlapping the corner arc was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'complete Brick side-contact band' $$log; \
		rm -f $$log $$mesh; \
		echo 'brick_side_contact_guard=pass case=corner_arc_overlap'

validate-brick-label-clearance-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-brick-label-clearance.log; \
		mesh=$(BUILD)/invalid-brick-label-clearance.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="plate"' \
			-D 'plate_size=[132,205]' $(BRICK_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: Brick title/mount collision was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'top title box entered a top 4040 frame slot lane' $$log; \
		rm -f $$log $$mesh; \
		echo 'brick_label_clearance_guard=pass case=undersized_top_title_lane'

validate-brick-preview-export: $(BUILD)/trimui-brick-carrier.stl \
	$(CHECKS)/brick-assembly-export.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(BUILD)/trimui-brick-carrier.stl \
		$(CHECKS)/brick-assembly-export.stl
	@echo 'brick_preview_export_guard=pass ghosts=excluded'

validate: lint all validate-profile-guard validate-rear-gap-guard \
	validate-nut-capture-guard validate-family-equivalence \
	validate-preview-export validate-brick-flat-datum-guard \
	validate-brick-clearance-guard validate-brick-side-contact-guard \
	validate-brick-label-clearance-guard validate-brick-preview-export
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 \
		$(BUILD)/trimui-smart-pro-s-carrier.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 \
		$(BUILD)/trimui-smart-pro-carrier.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 30 --max-z 16 \
		$(BUILD)/j-hook.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 80 --max-y 80 --max-z 16 \
		$(BUILD)/j-hook-set.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 80 --max-y 80 --max-z 16 \
		$(BUILD)/fit-coupon.stl
	$(PYTHON) scripts/stl_bounds.py --bed-x 247 --bed-y 207 \
		$(BUILD)/trimui-brick-carrier.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 45 --max-z 18 \
		$(BUILD)/trimui-brick-lower-hook.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 45 --max-z 18 \
		$(BUILD)/trimui-brick-upper-hook.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 80 --max-y 85 --max-z 18 \
		$(BUILD)/trimui-brick-hook-set.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 80 --max-y 80 --max-z 18 \
		$(BUILD)/trimui-brick-fit-coupon.stl

clean:
	rm -rf $(BUILD)
