OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
GUIDE_BUILD := $(BUILD)/handbook
GUIDE_LAYER_BUILD := $(GUIDE_BUILD)/layers
GUIDE_BATCH_LAYER_BUILD := $(GUIDE_BUILD)/batch-layers
GUIDE_MODEL_BUILD := $(GUIDE_BUILD)/model
SOURCE := pocketforge-node-chassis.scad
BOUNDS := ../dut-cradle-v1/scripts/stl_bounds.py
CUT_LIST := CUT_LIST.md
GUIDE_MODEL_SCRIPT := scripts/build_handbook_model.py
GUIDE_BATCH_MODEL_SCRIPT := scripts/build_handbook_batch_model.py
GUIDE_MODEL_REQUIREMENTS := scripts/handbook-model-requirements.txt
GUIDE_MODEL := $(GUIDE_MODEL_BUILD)/pocketforge-test-node.glb
GUIDE_MODEL_PROVENANCE := $(GUIDE_MODEL_BUILD)/pocketforge-test-node.provenance.json
SOURCE_REPOSITORY := https://github.com/pocketforge-os/test-node-hw

FIXTURE_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-v1.stl
FIXTURE_COMPONENTS_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-components.stl
FIXTURE_LABELS_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-labels.stl
CRADLE_BODY_STL := ../dut-cradle-v1/build/trimui-smart-pro-family-carrier-body.stl
CRADLE_LABELS_STL := ../dut-cradle-v1/build/trimui-smart-pro-labels.stl
CRADLE_S_LABELS_STL := ../dut-cradle-v1/build/trimui-smart-pro-s-labels.stl
CRADLE_HOOKS_STL := ../dut-cradle-v1/build/trimui-smart-pro-family-installed-hooks.stl

PRESENTATION_IMPORT_DIR := $(BUILD)/imports
PRESENTATION_FIXTURE_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-v1.stl
PRESENTATION_FIXTURE_COMPONENTS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-components.stl
PRESENTATION_FIXTURE_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-labels.stl
PRESENTATION_CRADLE_BODY_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-family-carrier-body.stl
PRESENTATION_CRADLE_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-labels.stl
PRESENTATION_CRADLE_S_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-s-labels.stl
PRESENTATION_CRADLE_HOOKS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-family-installed-hooks.stl

DEVICE_MODEL_COMMIT := 59bba8e022b7ec107c88b4099820d4faf81e08dd
DEVICE_MODEL_SHA256 := 75f9455ab6d2fe799630cf3a0da52964ec5013da7cfa72e6c1dc634e2f6104e4
DEVICE_MODEL_URL := https://raw.githubusercontent.com/pocketforge-os/platform/$(DEVICE_MODEL_COMMIT)/device-models/trimui-smart-pro/trimui-smart-pro.scad
PRESENTATION_DEVICE_SCAD := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-device-model.scad
PRESENTATION_DEVICE_SHELL_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-device-shell.stl
PRESENTATION_DEVICE_CONTROLS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-device-controls.stl
PRESENTATION_DEVICE_SCREEN_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-device-screen.stl

PRESENTATION_ASSETS := \
	$(PRESENTATION_FIXTURE_STL) \
	$(PRESENTATION_FIXTURE_COMPONENTS_STL) \
	$(PRESENTATION_FIXTURE_LABELS_STL) \
	$(PRESENTATION_CRADLE_BODY_STL) \
	$(PRESENTATION_CRADLE_LABELS_STL) \
	$(PRESENTATION_CRADLE_S_LABELS_STL) \
	$(PRESENTATION_CRADLE_HOOKS_STL) \
	$(PRESENTATION_DEVICE_SHELL_STL) \
	$(PRESENTATION_DEVICE_CONTROLS_STL) \
	$(PRESENTATION_DEVICE_SCREEN_STL)

PRODUCTION_BATCHES := \
	$(BUILD)/production-batch-01-ironed-interfaces.stl \
	$(BUILD)/production-batch-02-splice-collars.stl \
	$(BUILD)/production-batch-03-movable-mounts.stl \
	$(BUILD)/production-batch-04-frame-hardware.stl \
	$(BUILD)/production-batch-05-placard-holder.stl \
	$(BUILD)/production-batch-06-device-nameplate.stl

CALIBRATION := $(BUILD)/production-batch-00-calibration.stl

REPLACEMENT_PARTS := \
	$(BUILD)/device-id-placard.stl \
	$(BUILD)/placard-holder.stl \
	$(BUILD)/placard-slide-fit-coupon.stl \
	$(BUILD)/power-strip-fit-coupon-set.stl \
	$(BUILD)/power-strip-mount-block.stl \
	$(BUILD)/power-strip-mount-block-pair.stl \
	$(BUILD)/placard-riser.stl \
	$(BUILD)/placard-riser-pair.stl \
	$(BUILD)/placard-spacer.stl \
	$(BUILD)/placard-spacer-pair.stl \
	$(BUILD)/plate-spacer.stl \
	$(BUILD)/plate-spacer-set.stl \
	$(BUILD)/rear-carrier-link-top.stl \
	$(BUILD)/rear-carrier-link-bottom.stl \
	$(BUILD)/rear-carrier-link-set.stl \
	$(BUILD)/gantry-joint-plate.stl \
	$(BUILD)/gantry-joint-plate-set.stl \
	$(BUILD)/gantry-upright-splice-full-collar.stl \
	$(BUILD)/gantry-upright-splice-full-collar-internal-bar.stl \
	$(BUILD)/gantry-upright-splice-full-collar-internal-bar-pair.stl \
	$(BUILD)/stacking-registration-tab.stl \
	$(BUILD)/stacking-registration-tab-set.stl \
	$(BUILD)/rail-fit-coupon.stl \
	$(BUILD)/m3-slide-nut-carrier.stl \
	$(BUILD)/m3-slide-nut-carrier-set.stl \
	$(BUILD)/m3-slide-nut-fit-coupon.stl

GUIDE_STEPS := \
	$(GUIDE_BUILD)/hero.png \
	$(GUIDE_BUILD)/prep-captive-nut.png \
	$(GUIDE_BUILD)/prep-captive-nut-count.png \
	$(GUIDE_BUILD)/preload-channel-bar.png \
	$(GUIDE_BUILD)/preload-map.png \
	$(GUIDE_BUILD)/preload-width-rails.png \
	$(GUIDE_BUILD)/preload-parked-replacement.png \
	$(GUIDE_BUILD)/preload-depth-rails.png \
	$(GUIDE_BUILD)/preload-camera-frame.png \
	$(GUIDE_BUILD)/step-01-splice-uprights.png \
	$(GUIDE_BUILD)/step-02-build-gantry.png \
	$(GUIDE_BUILD)/step-03-open-frame.png \
	$(GUIDE_BUILD)/step-04-install-gantry.png \
	$(GUIDE_BUILD)/step-05-close-frame.png \
	$(GUIDE_BUILD)/step-06-mount-carrier.png \
	$(GUIDE_BUILD)/step-07-mount-fixture.png \
	$(GUIDE_BUILD)/step-08-complete.png \
	$(GUIDE_BUILD)/detail-01-splice-xray.png \
	$(GUIDE_BUILD)/detail-02-crossbar-corner.png \
	$(GUIDE_BUILD)/detail-03-lower-frame-layout.png \
	$(GUIDE_BUILD)/detail-03-flush-corner.png \
	$(GUIDE_BUILD)/detail-04-lower-gantry.png \
	$(GUIDE_BUILD)/detail-04-joint-plate.png \
	$(GUIDE_BUILD)/detail-04-gantry-position.png \
	$(GUIDE_BUILD)/detail-05-lower-top-ring.png \
	$(GUIDE_BUILD)/detail-05-square-diagonals.png \
	$(GUIDE_BUILD)/detail-06-carrier-link-lengths.png \
	$(GUIDE_BUILD)/detail-07-fixture-spacers.png \
	$(GUIDE_BUILD)/detail-07-optical-axis.png \
	$(GUIDE_BUILD)/detail-08-placard.png \
	$(GUIDE_BUILD)/detail-08-power-strip.png \
	$(GUIDE_BUILD)/detail-08-stacking-corner.png

GUIDE_BATCH_PREVIEWS := \
	$(GUIDE_BUILD)/batch-00-calibration.png \
	$(GUIDE_BUILD)/batch-01-ironed-interfaces.png \
	$(GUIDE_BUILD)/batch-02-splice-collars.png \
	$(GUIDE_BUILD)/batch-03-movable-mounts.png \
	$(GUIDE_BUILD)/batch-04-frame-hardware.png \
	$(GUIDE_BUILD)/batch-05-placard-holder.png \
	$(GUIDE_BUILD)/batch-06-device-nameplate.png

GUIDE_BATCH_MODELS := \
	$(GUIDE_BUILD)/batch-00-calibration.glb \
	$(GUIDE_BUILD)/batch-01-ironed-interfaces.glb \
	$(GUIDE_BUILD)/batch-02-splice-collars.glb \
	$(GUIDE_BUILD)/batch-03-movable-mounts.glb \
	$(GUIDE_BUILD)/batch-04-frame-hardware.glb \
	$(GUIDE_BUILD)/batch-05-placard-holder.glb \
	$(GUIDE_BUILD)/batch-06-device-nameplate.glb

GUIDE_LAYERS := \
	$(GUIDE_LAYER_BUILD)/aluminum.stl \
	$(GUIDE_LAYER_BUILD)/connectors.stl \
	$(GUIDE_LAYER_BUILD)/printed-hardware.stl \
	$(GUIDE_LAYER_BUILD)/fixture-plate.stl \
	$(GUIDE_LAYER_BUILD)/fixture-components.stl \
	$(GUIDE_LAYER_BUILD)/fixture-labels.stl \
	$(GUIDE_LAYER_BUILD)/carrier-body.stl \
	$(GUIDE_LAYER_BUILD)/carrier-labels.stl \
	$(GUIDE_LAYER_BUILD)/carrier-hooks.stl \
	$(GUIDE_LAYER_BUILD)/device-shell.stl \
	$(GUIDE_LAYER_BUILD)/device-controls.stl \
	$(GUIDE_LAYER_BUILD)/device-screen.stl \
	$(GUIDE_LAYER_BUILD)/webcam.stl \
	$(GUIDE_LAYER_BUILD)/power-strip.stl \
	$(GUIDE_LAYER_BUILD)/placard-holder.stl \
	$(GUIDE_LAYER_BUILD)/placard-insert.stl \
	$(GUIDE_LAYER_BUILD)/placard-labels.stl \
	$(GUIDE_LAYER_BUILD)/camera-frustum.stl

GUIDE_CAMERA := --projection=ortho --camera=560,-650,470,173,179,184
GUIDE_IMAGE := --imgsize=1400,1100 --viewall $(GUIDE_CAMERA)
GUIDE_MESH_DEPS := $(SOURCE) lib/pf-2020.scad $(PRESENTATION_ASSETS)

.NOTPARALLEL:

.PHONY: all batches calibration replacements lint preview presentation-assets \
	guide-static guide-batch-models guide-layers guide-model handbook-assets \
	cutlist refresh-cut-list \
	validate-cut-list-sync validate validate-margin-guard \
	validate-fov-guard validate-nut-carrier-guard \
	validate-gantry-travel-guard validate-production-batches clean

all: batches replacements cutlist

batches: $(PRODUCTION_BATCHES)

calibration: $(CALIBRATION)

replacements: $(REPLACEMENT_PARTS)

$(BUILD) $(GUIDE_BUILD) $(GUIDE_LAYER_BUILD) $(GUIDE_BATCH_LAYER_BUILD) \
$(GUIDE_MODEL_BUILD) $(PRESENTATION_IMPORT_DIR):
	mkdir -p $@

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(BUILD)/device-id-placard.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard"' $<

$(BUILD)/placard-holder.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard_holder"' $<

$(BUILD)/placard-slide-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="placard_slide_fit_coupon"' $<

$(BUILD)/power-strip-fit-coupon-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="power_strip_fit_coupon_set"' $<

$(BUILD)/power-strip-mount-block.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="power_strip_mount_block"' $<

$(BUILD)/power-strip-mount-block-pair.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="power_strip_mount_block_pair"' $<

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

$(BUILD)/rear-carrier-link-top.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="rear_carrier_link_top"' $<

$(BUILD)/rear-carrier-link-bottom.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="rear_carrier_link_bottom"' $<

$(BUILD)/rear-carrier-link-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="rear_carrier_link_set"' $<

$(BUILD)/gantry-joint-plate.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="gantry_joint_plate"' $<

$(BUILD)/gantry-joint-plate-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="gantry_joint_plate_set"' $<

$(BUILD)/gantry-upright-splice-full-collar.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="gantry_splice_full_collar"' $<

$(BUILD)/gantry-upright-splice-full-collar-internal-bar.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="gantry_splice_full_collar_internal_bar"' $<

$(BUILD)/gantry-upright-splice-full-collar-internal-bar-pair.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="gantry_splice_full_collar_internal_bar_pair"' $<

$(BUILD)/stacking-registration-tab.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="registration_tab"' $<

$(BUILD)/stacking-registration-tab-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="registration_tab_set"' $<

$(BUILD)/rail-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="rail_fit_coupon"' $<

$(BUILD)/m3-slide-nut-carrier.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_slide_nut"' $<

$(BUILD)/m3-slide-nut-carrier-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_slide_nut_set"' $<

$(BUILD)/m3-slide-nut-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_slide_nut_coupon"' $<

$(BUILD)/production-batch-00-calibration.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_00_calibration"' $<

$(BUILD)/production-batch-01-ironed-interfaces.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_01_ironed_interfaces"' $<

$(BUILD)/production-batch-02-splice-collars.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_02_splice_collars"' $<

$(BUILD)/production-batch-03-movable-mounts.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_03_movable_mounts"' $<

$(BUILD)/production-batch-04-frame-hardware.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_04_frame_hardware"' $<

$(BUILD)/production-batch-05-placard-holder.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_05_placard_holder"' $<

$(BUILD)/production-batch-06-device-nameplate.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_06_device_nameplate"' $<

$(FIXTURE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-v1.stl

$(FIXTURE_COMPONENTS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-components.stl

$(FIXTURE_LABELS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-labels.stl

$(CRADLE_BODY_STL):
	$(MAKE) -C ../dut-cradle-v1 build/trimui-smart-pro-family-carrier-body.stl

$(CRADLE_LABELS_STL):
	$(MAKE) -C ../dut-cradle-v1 build/trimui-smart-pro-labels.stl

$(CRADLE_S_LABELS_STL):
	$(MAKE) -C ../dut-cradle-v1 build/trimui-smart-pro-s-labels.stl

$(CRADLE_HOOKS_STL):
	$(MAKE) -C ../dut-cradle-v1 build/trimui-smart-pro-family-installed-hooks.stl

$(PRESENTATION_FIXTURE_STL): $(FIXTURE_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_COMPONENTS_STL): $(FIXTURE_COMPONENTS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_LABELS_STL): $(FIXTURE_LABELS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_CRADLE_BODY_STL): $(CRADLE_BODY_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_CRADLE_LABELS_STL): $(CRADLE_LABELS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_CRADLE_S_LABELS_STL): $(CRADLE_S_LABELS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_CRADLE_HOOKS_STL): $(CRADLE_HOOKS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_DEVICE_SCAD): | $(PRESENTATION_IMPORT_DIR)
	curl --fail --location --silent --show-error $(DEVICE_MODEL_URL) -o $@
	@printf '%s  %s\n' '$(DEVICE_MODEL_SHA256)' '$@' | sha256sum -c -

$(PRESENTATION_DEVICE_SHELL_STL): $(PRESENTATION_DEVICE_SCAD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="shell"' \
		-D 'QUALITY="draft"' -D 'SHOW_GLYPHS=true' \
		-D 'SHOW_MICRO_DETAILS=false' $<

$(PRESENTATION_DEVICE_CONTROLS_STL): $(PRESENTATION_DEVICE_SCAD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="controls"' \
		-D 'QUALITY="draft"' -D 'SHOW_GLYPHS=true' \
		-D 'SHOW_MICRO_DETAILS=false' $<

$(PRESENTATION_DEVICE_SCREEN_STL): $(PRESENTATION_DEVICE_SCAD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="screen"' \
		-D 'QUALITY="draft"' -D 'SHOW_GLYPHS=false' \
		-D 'SHOW_MICRO_DETAILS=false' $<

presentation-assets: $(PRESENTATION_ASSETS)

$(BUILD)/layout-assembly.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="assembly"' \
		-D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-assembly-mesh.png: $(GUIDE_MESH_DEPS) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall -D 'PART="presentation"' $<

$(BUILD)/layout-front.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --camera=200,-500,220,200,200,220 \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-stacked.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1600 \
		--projection=ortho --viewall -D 'PART="stacked_assembly"' \
		-D 'PLATE_DETAIL="proxy"' $<

$(BUILD)/layout-corner-joint.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,900 \
		--projection=ortho --viewall --camera=150,-160,130,25,25,20 \
		-D 'PART="corner_joint_detail"' $<

$(BUILD)/layout-m3-slide-nut.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,800 \
		--projection=ortho --viewall --camera=18,-24,18,0,0,1 \
		-D 'PART="m3_slide_nut"' $<

$(BUILD)/layout-gantry-splice-installed.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --viewall --camera=145,-135,105,0,0,13 \
		-D 'PART="gantry_splice_installed_preview"' $<

$(BUILD)/layout-placard-system.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,700 \
		--projection=ortho --viewall -D 'PART="placard_system_preview"' $<

$(BUILD)/layout-power-strip-system.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,1100 \
		--projection=ortho --viewall -D 'PART="power_strip_system_preview"' $<

$(GUIDE_BUILD)/hero.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1800,1200 \
		--viewall $(GUIDE_CAMERA) -D 'PART="guide_step_08_complete"' $<

$(GUIDE_BUILD)/step-01-splice-uprights.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_01_splice_uprights"' $<

$(GUIDE_BUILD)/step-02-build-gantry.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_02_build_gantry"' $<

$(GUIDE_BUILD)/step-03-open-frame.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_03_open_frame"' $<

$(GUIDE_BUILD)/step-04-install-gantry.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_04_install_gantry"' $<

$(GUIDE_BUILD)/step-05-close-frame.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_05_close_frame"' $<

$(GUIDE_BUILD)/step-06-mount-carrier.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_06_mount_carrier"' $<

$(GUIDE_BUILD)/step-07-mount-fixture.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_07_mount_fixture"' $<

$(GUIDE_BUILD)/step-08-complete.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_step_08_complete"' $<

$(GUIDE_BUILD)/prep-captive-nut.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,600 \
		--projection=ortho --camera=120,-135,95,0,0,0 \
		-D 'PART="guide_captive_nut_install"' $<

$(GUIDE_BUILD)/prep-captive-nut-count.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,620 \
		--projection=ortho --camera=205,30,675,205,30,0 \
		-D 'PART="guide_captive_nut_count"' $<

$(GUIDE_BUILD)/preload-channel-bar.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,820 \
		--projection=ortho \
		--camera=-70,-40,48,33,0,10 \
		-D 'PART="guide_preload_channel_bar"' $<

$(GUIDE_BUILD)/preload-map.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall \
		--camera=520,-560,480,173,179,184 \
		-D 'PART="guide_preload_map"' $<

$(GUIDE_BUILD)/preload-width-rails.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1800,700 \
		--projection=ortho --camera=352,20,850,352,20,0 \
		-D 'PART="guide_preload_width_rails"' $<

$(GUIDE_BUILD)/preload-parked-replacement.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,850 \
		--projection=ortho --camera=210,70,1600,210,70,0 \
		-D 'PART="guide_parked_replacement_explained"' $<

$(GUIDE_BUILD)/preload-depth-rails.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,1200 \
		--projection=ortho --viewall --camera=185,175,1000,185,175,0 \
		-D 'PART="guide_preload_depth_rails"' $<

$(GUIDE_BUILD)/preload-camera-frame.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1450,1200 \
		--projection=ortho --viewall \
		--camera=173,-600,184,173,75,184 \
		-D 'PART="guide_preload_camera_frame"' $<

$(GUIDE_BUILD)/detail-01-splice-xray.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,820 \
		--projection=ortho --viewall --camera=145,-135,105,0,0,13 \
		-D 'PART="gantry_splice_installed_preview"' $<

$(GUIDE_BUILD)/detail-02-crossbar-corner.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,900 \
		--projection=ortho --viewall --camera=190,-210,145,50,75,0 \
		-D 'PART="guide_detail_02_crossbar_corner"' $<

$(GUIDE_BUILD)/detail-03-lower-frame-layout.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_detail_03_lower_frame_layout"' $<

$(GUIDE_BUILD)/detail-03-flush-corner.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1100,900 \
		--projection=ortho --viewall --camera=150,-160,130,25,25,20 \
		-D 'PART="corner_joint_detail"' $<

$(GUIDE_BUILD)/detail-04-lower-gantry.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--viewall $(GUIDE_CAMERA) \
		-D 'PART="guide_detail_04_lower_gantry"' $<

$(GUIDE_BUILD)/detail-04-joint-plate.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,900 \
		--projection=ortho --viewall --camera=150,-170,120,10,75,28 \
		-D 'PART="guide_detail_04_joint_plate"' $<

$(GUIDE_BUILD)/detail-04-gantry-position.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_detail_04_gantry_position"' $<

$(GUIDE_BUILD)/detail-05-lower-top-ring.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--viewall $(GUIDE_CAMERA) \
		-D 'PART="guide_detail_05_lower_top_ring"' $<

$(GUIDE_BUILD)/detail-05-square-diagonals.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_detail_05_square_diagonals"' $<

$(GUIDE_BUILD)/detail-06-carrier-link-lengths.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,760 \
		--projection=ortho --viewall --camera=0,-180,310,0,0,0 \
		-D 'PART="guide_detail_06_carrier_link_lengths"' $<

$(GUIDE_BUILD)/detail-07-fixture-spacers.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1000 \
		--projection=ortho --viewall --camera=430,-360,350,173,65,184 \
		-D 'PART="guide_detail_07_fixture_spacers"' $<

$(GUIDE_BUILD)/detail-07-optical-axis.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,900 \
		--projection=ortho --viewall --camera=530,-70,250,173,179,184 \
		-D 'PART="guide_detail_07_optical_axis"' $<

$(GUIDE_BUILD)/detail-08-placard.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,800 \
		--projection=ortho --viewall --camera=520,-450,470,173,0,330 \
		-D 'PART="guide_detail_08_placard"' $<

$(GUIDE_BUILD)/detail-08-power-strip.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --viewall --camera=470,-430,300,173,45,28 \
		-D 'PART="guide_detail_08_power_strip"' $<

$(GUIDE_BUILD)/detail-08-stacking-corner.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1000 \
		--projection=ortho --viewall --camera=230,-240,510,30,30,370 \
		-D 'PART="guide_detail_08_stacking_corner"' $<

$(GUIDE_BUILD)/batch-00-calibration.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,800 \
		--projection=ortho --viewall -D 'PART="production_batch_00_calibration"' $<

$(GUIDE_BUILD)/batch-01-ironed-interfaces.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,800 \
		--projection=ortho --viewall -D 'PART="production_batch_01_ironed_interfaces"' $<

$(GUIDE_BUILD)/batch-02-splice-collars.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,800 \
		--projection=ortho --viewall -D 'PART="production_batch_02_splice_collars"' $<

$(GUIDE_BUILD)/batch-03-movable-mounts.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --viewall -D 'PART="production_batch_03_movable_mounts"' $<

$(GUIDE_BUILD)/batch-04-frame-hardware.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --viewall -D 'PART="production_batch_04_frame_hardware"' $<

$(GUIDE_BUILD)/batch-05-placard-holder.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,700 \
		--projection=ortho --viewall \
		--camera=115,-70,320,115,22,0 \
		-D 'PART="production_batch_05_placard_holder"' $<

$(GUIDE_BUILD)/batch-06-device-nameplate.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,700 \
		--projection=ortho --viewall \
		--camera=109,-70,320,109,22,0 \
		-D 'PART="production_batch_06_device_nameplate_preview"' $<

$(GUIDE_BUILD)/batch-00-calibration.glb: $(CALIBRATION) \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 00 calibration"

$(GUIDE_BUILD)/batch-01-ironed-interfaces.glb: \
		$(BUILD)/production-batch-01-ironed-interfaces.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 01 ironed interfaces"

$(GUIDE_BUILD)/batch-02-splice-collars.glb: \
		$(BUILD)/production-batch-02-splice-collars.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 02 splice collars"

$(GUIDE_BUILD)/batch-03-movable-mounts.glb: \
		$(BUILD)/production-batch-03-movable-mounts.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 03 movable mounts"

$(GUIDE_BUILD)/batch-04-frame-hardware.glb: \
		$(BUILD)/production-batch-04-frame-hardware.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 04 frame hardware"

$(GUIDE_BUILD)/batch-05-placard-holder.glb: \
		$(BUILD)/production-batch-05-placard-holder.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 05 placard holder"

$(GUIDE_BATCH_LAYER_BUILD)/batch-06-device-nameplate-body.stl: \
		$(SOURCE) lib/pf-2020.scad | $(GUIDE_BATCH_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="production_batch_06_device_nameplate_body"' $<

$(GUIDE_BATCH_LAYER_BUILD)/batch-06-device-nameplate-labels.stl: \
		$(SOURCE) lib/pf-2020.scad | $(GUIDE_BATCH_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'PART="production_batch_06_device_nameplate_labels"' $<

$(GUIDE_BUILD)/batch-06-device-nameplate.glb: \
		$(GUIDE_BATCH_LAYER_BUILD)/batch-06-device-nameplate-body.stl \
		$(GUIDE_BATCH_LAYER_BUILD)/batch-06-device-nameplate-labels.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--layer "$(GUIDE_BATCH_LAYER_BUILD)/batch-06-device-nameplate-body.stl::White nameplate body::#f5f5ed" \
		--layer "$(GUIDE_BATCH_LAYER_BUILD)/batch-06-device-nameplate-labels.stl::Black raised labels::#050505" \
		--output $@ --name "Batch 06 device nameplate"

$(GUIDE_LAYER_BUILD)/aluminum.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_aluminum"' $<

$(GUIDE_LAYER_BUILD)/connectors.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_connectors"' $<

$(GUIDE_LAYER_BUILD)/printed-hardware.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_printed_hardware"' $<

$(GUIDE_LAYER_BUILD)/fixture-plate.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_plate"' $<

$(GUIDE_LAYER_BUILD)/fixture-components.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_components"' $<

$(GUIDE_LAYER_BUILD)/fixture-labels.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_labels"' $<

$(GUIDE_LAYER_BUILD)/carrier-body.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_carrier_body"' $<

$(GUIDE_LAYER_BUILD)/carrier-labels.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_carrier_labels"' $<

$(GUIDE_LAYER_BUILD)/carrier-hooks.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_carrier_hooks"' $<

$(GUIDE_LAYER_BUILD)/device-shell.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_device_shell"' $<

$(GUIDE_LAYER_BUILD)/device-controls.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_device_controls"' $<

$(GUIDE_LAYER_BUILD)/device-screen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_device_screen"' $<

$(GUIDE_LAYER_BUILD)/webcam.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_webcam"' $<

$(GUIDE_LAYER_BUILD)/power-strip.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_power_strip"' $<

$(GUIDE_LAYER_BUILD)/placard-holder.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_placard_holder"' $<

$(GUIDE_LAYER_BUILD)/placard-insert.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_placard_insert"' $<

$(GUIDE_LAYER_BUILD)/placard-labels.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_placard_labels"' $<

$(GUIDE_LAYER_BUILD)/camera-frustum.stl: $(SOURCE) lib/pf-2020.scad | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_camera_frustum"' $<

guide-static: $(GUIDE_STEPS) $(GUIDE_BATCH_PREVIEWS)

guide-batch-models: $(GUIDE_BATCH_MODELS)

guide-layers: $(GUIDE_LAYERS)

$(GUIDE_MODEL) $(GUIDE_MODEL_PROVENANCE) &: $(GUIDE_LAYERS) \
		$(GUIDE_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_MODEL_BUILD)
	$(PYTHON) $(GUIDE_MODEL_SCRIPT) \
		--layers $(GUIDE_LAYER_BUILD) \
		--output $(GUIDE_MODEL) \
		--provenance $(GUIDE_MODEL_PROVENANCE) \
		--repository-root ../.. \
		--source-repository $(SOURCE_REPOSITORY)

guide-model: $(GUIDE_MODEL) $(GUIDE_MODEL_PROVENANCE)

handbook-assets: calibration batches guide-static guide-batch-models \
	guide-model cutlist

preview: $(BUILD)/layout-assembly.png $(BUILD)/layout-assembly-mesh.png \
	$(BUILD)/layout-front.png $(BUILD)/layout-stacked.png \
	$(BUILD)/layout-corner-joint.png $(BUILD)/layout-m3-slide-nut.png \
	$(BUILD)/layout-gantry-splice-installed.png \
	$(BUILD)/layout-placard-system.png \
	$(BUILD)/layout-power-strip-system.png \
	guide-static

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
			-D 'structural_x_length=304' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: undersized routing margin was not rejected' >&2; exit 1; \
		fi; \
	grep -q 'routing margin fell below 29 mm' $$log; \
	echo 'routing_margin_guard=pass rejected_structural_x=304mm'

validate-fov-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-fov.log; mesh=$(BUILD)/invalid-fov.stl; \
		if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh -D 'PART="placard_spacer"' \
			-D 'camera_diagonal_fov=40' $(SOURCE) >$$log 2>&1; then \
			echo 'ERROR: narrow camera FOV was not rejected' >&2; exit 1; \
		fi; \
	grep -q 'Estimated horizontal FOV is too narrow' $$log; \
	depth_log=$(BUILD)/invalid-frame-depth.log; \
	depth_mesh=$(BUILD)/invalid-frame-depth.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$depth_mesh \
			-D 'PART="placard_spacer"' \
			-D 'structural_y_length=260' $(SOURCE) >$$depth_log 2>&1; then \
		echo 'ERROR: undersized optical depth was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'Estimated horizontal FOV is too narrow' $$depth_log; \
	echo 'camera_fov_guard=pass diagonal_fov=40deg rejected_depth=260mm'

validate-nut-carrier-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-nut-carrier.log; \
	mesh=$(BUILD)/invalid-nut-carrier.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="m3_slide_nut"' \
			-D 'm3_slide_nut_bearing_width=12.2' $(SOURCE) >$$log 2>&1; then \
		echo 'ERROR: oversized carrier was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'fit inside the measured slot pocket' $$log; \
	narrow_log=$(BUILD)/invalid-nut-carrier-narrow.log; \
	narrow_mesh=$(BUILD)/invalid-nut-carrier-narrow.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$narrow_mesh \
			-D 'PART="m3_slide_nut"' \
			-D 'm3_slide_nut_bearing_width=6.7' $(SOURCE) >$$narrow_log 2>&1; then \
		echo 'ERROR: pull-through carrier was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'wider than the slot mouth' $$narrow_log; \
	deep_log=$(BUILD)/invalid-nut-carrier-deep-face.log; \
	deep_mesh=$(BUILD)/invalid-nut-carrier-deep-face.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$deep_mesh \
			-D 'PART="m3_slide_nut"' \
			-D 'm3_slide_nut_deep_width=8.7' $(SOURCE) >$$deep_log 2>&1; then \
		echo 'ERROR: over-wide deep face was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'clear measured rail dimension F' $$deep_log; \
	tall_log=$(BUILD)/invalid-nut-carrier-tall.log; \
	tall_mesh=$(BUILD)/invalid-nut-carrier-tall.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$tall_mesh \
			-D 'PART="m3_slide_nut"' \
			-D 'm3_slide_nut_height=4.9' $(SOURCE) >$$tall_log 2>&1; then \
		echo 'ERROR: over-depth carrier was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'fit behind the measured slot lip' $$tall_log; \
	echo 'nut_carrier_guard=pass rejected_bearing_widths=6.7,12.2mm rejected_deep_width=8.7mm rejected_height=4.9mm'

validate-gantry-travel-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-gantry-travel.log; \
	mesh=$(BUILD)/invalid-gantry-travel.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'PART="gantry_joint_plate"' \
			-D 'fixture_gantry_y=20' $(SOURCE) >$$log 2>&1; then \
		echo 'ERROR: out-of-range gantry was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'Fixture gantry Y is outside legal travel' $$log; \
	service_log=$(BUILD)/invalid-fixture-service.log; \
	service_mesh=$(BUILD)/invalid-fixture-service.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$service_mesh \
			-D 'PART="gantry_joint_plate"' \
			-D 'fixture_gantry_y=60' $(SOURCE) >$$service_log 2>&1; then \
		echo 'ERROR: undersized human-side service bay was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'at least 30 mm of human-side service bay' $$service_log; \
	echo 'gantry_guards=pass rejected_y=20mm rejected_service_y=60mm'

validate-production-batches: $(CALIBRATION) $(PRODUCTION_BATCHES)
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 10 \
		$(BUILD)/production-batch-00-calibration.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 6 \
		$(BUILD)/production-batch-01-ironed-interfaces.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 85 \
		$(BUILD)/production-batch-02-splice-collars.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 8 \
		$(BUILD)/production-batch-03-movable-mounts.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 30 \
		$(BUILD)/production-batch-04-frame-hardware.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 8 \
		$(BUILD)/production-batch-05-placard-holder.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 8 \
		$(BUILD)/production-batch-06-device-nameplate.stl
	@echo 'production_batches=pass count=6 optional_calibration=pass'

validate: lint all calibration preview validate-margin-guard \
	validate-fov-guard validate-nut-carrier-guard \
	validate-gantry-travel-guard validate-production-batches \
	validate-cut-list-sync
	printf '%s  %s\n' '$(DEVICE_MODEL_SHA256)' \
		'$(PRESENTATION_DEVICE_SCAD)' | sha256sum -c -
	grep -q '^outer_vertical_rail,4,360.00,1440.00' $(BUILD)/cut-list.csv
	grep -q '^outer_width_rail,4,306.00,1224.00' $(BUILD)/cut-list.csv
	grep -q '^outer_depth_rail,4,318.00,1272.00' $(BUILD)/cut-list.csv
	grep -q '^fixture_gantry_upright_half,4,164.00,656.00' $(BUILD)/cut-list.csv
	grep -q '^fixture_gantry_crossbar,2,306.00,612.00' $(BUILD)/cut-list.csv
	grep -q 'External assembled envelope (W × D × H): 346.00 × 358.00 × 368.00 mm' $(BUILD)/cut-list.md
	grep -q 'Clear internal envelope (W × D × H): 306.00 × 318.00 × 328.00 mm' $(BUILD)/cut-list.md
	grep -q 'Stock bars required: \*\*6\*\*' $(BUILD)/cut-list.md
	@echo 'chassis_validation=pass production_batches=6 stock_bars=6 handbook_major_steps=8 handbook_detail_panels=23'

clean:
	rm -rf $(BUILD)
