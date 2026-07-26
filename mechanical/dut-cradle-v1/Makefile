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
QUALIFICATION_MANIFEST := qualification/trimui-smart-pro-family-v1.json
QUALIFIED_ARTIFACTS := $(CHECKS)/smart-pro-unlabelled.stl \
	$(BUILD)/j-hook.stl $(BUILD)/j-hook-set.stl $(BUILD)/fit-coupon.stl

# OpenSCAD 2021.01 can corrupt a back-to-back off-screen PNG frame while its
# previous GL context is settling. Serialize previews and leave a short gap.
.NOTPARALLEL:

.PHONY: all lint test-fingerprint validate validate-qualified \
	validate-qualified-mutation validate-profile-guard validate-rear-gap-guard \
	validate-nut-capture-guard validate-family-equivalence \
	validate-preview-export validate-presentation-split preview clean

all: $(BUILD)/trimui-smart-pro-s-carrier.stl \
	$(BUILD)/trimui-smart-pro-carrier.stl \
	$(BUILD)/j-hook.stl $(BUILD)/j-hook-set.stl $(BUILD)/fit-coupon.stl

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

test-fingerprint:
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py' -v

$(BUILD) $(CHECKS):
	mkdir -p $@

$(BUILD)/trimui-smart-pro-s-carrier.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

$(BUILD)/trimui-smart-pro-carrier.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_DEVICE=false' -D 'SHOW_HOOKS=false' $<

# Presentation-only material split.  These touching, non-overlapping meshes
# preserve the slicer's white-to-black layer change in higher-level renders;
# neither is a replacement for the unified production carrier above.
$(BUILD)/trimui-smart-pro-family-carrier-body.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_body"' $<

$(BUILD)/trimui-smart-pro-labels.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_labels"' $<

$(BUILD)/trimui-smart-pro-s-labels.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="presentation_labels"' $<

$(BUILD)/j-hook.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook"' $<

$(BUILD)/j-hook-set.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook_set"' $<

# Presentation-only: six hooks transformed into their accepted installed
# positions.  This is consumed by the chassis model and is never a print STL.
$(BUILD)/trimui-smart-pro-family-installed-hooks.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="installed_hooks"' $<

$(BUILD)/fit-coupon.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="fit_coupon"' $<

$(CHECKS)/smart-pro-s-assembly-export.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/smart-pro-assembly-export.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="assembly"' \
		-D 'SHOW_DEVICE=true' -D 'SHOW_HOOKS=true' -D 'SHOW_KEEP_OUTS=true' $<

$(CHECKS)/smart-pro-s-unlabelled.stl: $(SMART_PRO_S_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_LABELS=false' $<

$(CHECKS)/smart-pro-unlabelled.stl: $(SMART_PRO_SOURCE) $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="plate"' \
		-D 'SHOW_LABELS=false' $<

$(CHECKS)/qualified-mutated-j-hook.stl: $(FAMILY_SOURCE) $(LIBRARY) | $(CHECKS)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="hook"' \
		-D 'hook_throat=11.4' $<

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

preview: $(BUILD)/layout-smart-pro-s-preview.png \
	$(BUILD)/layout-smart-pro-s-top.png \
	$(BUILD)/layout-smart-pro-preview.png \
	$(BUILD)/layout-smart-pro-top.png

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

validate-presentation-split: $(BUILD)/trimui-smart-pro-family-carrier-body.stl \
	$(BUILD)/trimui-smart-pro-labels.stl \
	$(BUILD)/trimui-smart-pro-s-labels.stl \
	$(CHECKS)/smart-pro-unlabelled.stl
	$(PYTHON) scripts/stl_bounds.py \
		--equivalent-to $(CHECKS)/smart-pro-unlabelled.stl \
		$(BUILD)/trimui-smart-pro-family-carrier-body.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 247 --max-y 200 --max-z 4.4 \
		$(BUILD)/trimui-smart-pro-labels.stl
	$(PYTHON) scripts/stl_bounds.py --max-x 247 --max-y 200 --max-z 4.4 \
		$(BUILD)/trimui-smart-pro-s-labels.stl
	@echo 'presentation_split_guard=pass body=off-white labels=variant-specific-black boundary_z=3.2mm'

validate-qualified: test-fingerprint $(QUALIFIED_ARTIFACTS) \
		$(QUALIFICATION_MANIFEST) qualification/cad-toolchain.json
	$(PYTHON) scripts/qualified_geometry.py --root . check \
		--manifest $(QUALIFICATION_MANIFEST) --openscad '$(OPENSCAD)'

validate-qualified-mutation: $(CHECKS)/qualified-mutated-j-hook.stl \
		$(QUALIFICATION_MANIFEST)
	$(PYTHON) scripts/stl_bounds.py --max-x 30 --max-y 30 --max-z 16 \
		$(CHECKS)/qualified-mutated-j-hook.stl
	@set -eu; log=$(CHECKS)/qualified-mutation.log; \
		if $(PYTHON) scripts/qualified_geometry.py --root . compare \
			--manifest $(QUALIFICATION_MANIFEST) --artifact j_hook \
			--stl $(CHECKS)/qualified-mutated-j-hook.stl >$$log 2>&1; then \
			echo 'ERROR: printable hook mutation matched qualified geometry' >&2; \
			exit 1; \
		fi; \
		grep -q 'qualified_geometry_mismatch artifact=j_hook field=fingerprint' $$log; \
		rm -f $$log; \
		echo 'qualified_mutation_guard=pass case=hook_throat_11.3_to_11.4'

validate: lint all $(BUILD)/trimui-smart-pro-family-installed-hooks.stl \
	validate-profile-guard validate-rear-gap-guard \
	validate-nut-capture-guard validate-family-equivalence \
	validate-preview-export validate-presentation-split \
	validate-qualified validate-qualified-mutation
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
	$(PYTHON) scripts/stl_bounds.py --max-x 220 --max-y 110 --max-z 28 \
		$(BUILD)/trimui-smart-pro-family-installed-hooks.stl

clean:
	rm -rf $(BUILD)
