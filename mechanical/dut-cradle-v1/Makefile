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
RG353V_SOURCE := anbernic-rg353v-cradle.scad

# OpenSCAD 2021.01 can corrupt a back-to-back off-screen PNG frame while its
# previous GL context is settling. Serialize previews and leave a short gap.
.NOTPARALLEL:

.PHONY: all lint validate validate-profile-guard validate-rear-gap-guard \
	validate-nut-capture-guard validate-family-equivalence \
	validate-preview-export validate-rg353v-flat-datum-guard \
	validate-rg353v-trigger-guard validate-rg353v-curve-guard \
	validate-rg353v-bottom-port-guard \
	validate-rg353v-print-foot-guard validate-rg353v-preview-export \
	preview clean

all: $(BUILD)/trimui-smart-pro-s-carrier.stl \
	$(BUILD)/trimui-smart-pro-carrier.stl \
	$(BUILD)/j-hook.stl $(BUILD)/j-hook-set.stl $(BUILD)/fit-coupon.stl \
	$(BUILD)/anbernic-rg353v-carrier.stl \
	$(BUILD)/anbernic-rg353v-lower-hook.stl \
	$(BUILD)/anbernic-rg353v-upper-hook.stl \
	$(BUILD)/anbernic-rg353v-hook-set.stl \
	$(BUILD)/anbernic-rg353v-fit-coupon.stl

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

$(BUILD)/anbernic-rg353v-carrier.stl: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

$(BUILD)/anbernic-rg353v-lower-hook.stl: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="lower_hook"' $<

$(BUILD)/anbernic-rg353v-upper-hook.stl: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="upper_hook"' $<

$(BUILD)/anbernic-rg353v-hook-set.stl: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook_set"' $<

$(BUILD)/anbernic-rg353v-fit-coupon.stl: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' $<

$(CHECKS)/smart-pro-s-assembly-export.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/smart-pro-assembly-export.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/rg353v-assembly-export.stl: $(RG353V_SOURCE) $(LIBRARY) | $(CHECKS)
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

$(BUILD)/layout-anbernic-rg353v-preview.png: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1400 \
		--projection=ortho --viewall -D 'PART="assembly"' $<

$(BUILD)/layout-anbernic-rg353v-top.png: $(RG353V_SOURCE) $(LIBRARY) | $(BUILD)
	$(PREVIEW_SETTLE)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1400 \
		--projection=ortho --camera=90,102.5,700,90,102.5,0 \
		-D 'PART="assembly"' $<

preview: $(BUILD)/layout-smart-pro-s-preview.png \
	$(BUILD)/layout-smart-pro-s-top.png \
	$(BUILD)/layout-smart-pro-preview.png \
	$(BUILD)/layout-smart-pro-top.png \
	$(BUILD)/layout-anbernic-rg353v-preview.png \
	$(BUILD)/layout-anbernic-rg353v-top.png

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

validate-rg353v-flat-datum-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-rg353v-datum.log; \
		mesh=$(BUILD)/invalid-rg353v-datum.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="lower_hook"' \
			-D 'upper_rear_gap=17.0' $(RG353V_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: misaligned RG353V front datum was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'RG353V hook families must share one flat front contact plane' $$log; \
		rm -f $$log $$mesh; \
		echo 'rg353v_flat_datum_guard=pass case=misaligned_hook_family_datums'

validate-rg353v-trigger-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-rg353v-trigger.log; \
		mesh=$(BUILD)/invalid-rg353v-trigger.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="upper_hook"' \
			-D 'top_contact_inset=20.0' $(RG353V_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: RG353V top shoulder-trigger contact was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'RG353V top supports entered an outer shoulder-trigger keep-out' $$log; \
		rm -f $$log $$mesh; \
		echo 'rg353v_trigger_guard=pass case=top_contact_in_shoulder_trigger_band'

validate-rg353v-bottom-port-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-rg353v-bottom-port.log; \
		mesh=$(BUILD)/invalid-rg353v-bottom-port.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="lower_hook"' \
			-D 'lower_hook_width=14.0' $(RG353V_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: blocked RG353V bottom USB-C lane was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'RG353V bottom supports entered the center USB-C cable keep-out' $$log; \
		rm -f $$log $$mesh; \
		echo 'rg353v_bottom_port_guard=pass case=bottom_hook_blocked_usb_c_lane'

validate-rg353v-curve-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-rg353v-curve.log; \
		mesh=$(BUILD)/invalid-rg353v-curve.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="lower_hook"' \
			-D 'lower_support_depth=8.0' $(RG353V_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: short RG353V curved-shell shelf was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'RG353V curved lower shell requires long support shelves' $$log; \
		rm -f $$log $$mesh; \
		echo 'rg353v_curve_guard=pass case=short_lower_shelf'

validate-rg353v-print-foot-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-rg353v-print-foot.log; \
		mesh=$(BUILD)/invalid-rg353v-print-foot.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="upper_hook"' \
			-D 'hook_spine_width=10.0' $(RG353V_SOURCE) >$$log 2>&1; then \
			echo 'ERROR: protruding RG353V print-foot nub was not rejected' >&2; \
			exit 1; \
		fi; \
		grep -q 'anti-rotation keys must not protrude below the broad print face' $$log; \
		rm -f $$log $$mesh; \
		echo 'rg353v_print_foot_guard=pass case=key_below_broad_face'

validate-rg353v-preview-export: $(BUILD)/anbernic-rg353v-carrier.stl \
	$(CHECKS)/rg353v-assembly-export.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(BUILD)/anbernic-rg353v-carrier.stl \
		$(CHECKS)/rg353v-assembly-export.stl
	@echo 'rg353v_preview_export_guard=pass ghosts=excluded'

validate: lint all validate-profile-guard validate-rear-gap-guard \
	validate-nut-capture-guard validate-family-equivalence \
	validate-preview-export validate-rg353v-flat-datum-guard \
	validate-rg353v-trigger-guard validate-rg353v-curve-guard \
	validate-rg353v-bottom-port-guard \
	validate-rg353v-print-foot-guard validate-rg353v-preview-export
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
		$(BUILD)/anbernic-rg353v-carrier.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 45 --max-z 18 \
		--min-bed-contact-area 150 \
		$(BUILD)/anbernic-rg353v-lower-hook.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 45 --max-z 18 \
		--min-bed-contact-area 150 \
		$(BUILD)/anbernic-rg353v-upper-hook.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 85 --max-y 90 --max-z 18 \
		$(BUILD)/anbernic-rg353v-hook-set.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 75 --max-y 90 --max-z 18 \
		$(BUILD)/anbernic-rg353v-fit-coupon.stl

clean:
	rm -rf $(BUILD)
