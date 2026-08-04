OPENSCAD ?= openscad
OPENSCAD_FLAGS := --hardwarnings --check-parameters=true --check-parameter-ranges=true
PYTHON ?= python3
BUILD := build
DUALBAR_BUILD := $(BUILD)/dualbar
BRICK_DUALBAR_BUILD := $(BUILD)/dualbar-brick
GUIDE_BUILD := $(BUILD)/handbook
GUIDE_LAYER_BUILD := $(GUIDE_BUILD)/layers
GUIDE_BATCH_LAYER_BUILD := $(GUIDE_BUILD)/batch-layers
GUIDE_MODEL_BUILD := $(GUIDE_BUILD)/model
SOURCE := pocketforge-node-chassis.scad
RIGHT_ANGLE_CHECKER_SOURCE := right-angle-checker.scad
RIGHT_ANGLE_CHECKER_STL := $(BUILD)/right-angle-checker-150mm.stl
RIGHT_ANGLE_CHECKER_PREVIEW := $(BUILD)/right-angle-checker-150mm.png
RIGHT_ANGLE_CHECKER_CUSTOM_TEST := $(BUILD)/right-angle-checker-custom-test.stl
BOUNDS := ../dut-cradle-v1/scripts/stl_bounds.py
TOPOLOGY := scripts/check_stl_topology.py
RIGHT_ANGLE_CHECKER_GEOMETRY := scripts/check_right_angle_checker.py
FINGERPRINT := ../dut-cradle-v1/scripts/mesh_fingerprint.py
TARGET_CONTRACT_TEST := scripts/test_makefile_targets.py
CUT_LIST := CUT_LIST.md
DUALBAR_CUT_LIST := CUT_LIST_DUALBAR.md
GUIDE_MODEL_SCRIPT := scripts/build_handbook_model.py
GUIDE_BATCH_MODEL_SCRIPT := scripts/build_handbook_batch_model.py
GUIDE_MODEL_REQUIREMENTS := scripts/handbook-model-requirements.txt
GUIDE_MODEL := $(GUIDE_MODEL_BUILD)/pocketforge-test-node.glb
GUIDE_MODEL_PROVENANCE := $(GUIDE_MODEL_BUILD)/pocketforge-test-node.provenance.json
SOURCE_REPOSITORY := https://github.com/pocketforge-os/test-node-hw
GUIDE_DEVICE_SLUG := trimui-smart-pro-s
GUIDE_CHASSIS_VARIANT := dualbar_v1
GUIDE_EXAMPLE_DEVICE_VARIANT := smart_pro_s
GUIDE_DEVICE_REGISTRY := ../device-packs/device-layouts.json
GUIDE_LAYOUT_RECORD := ../device-packs/layouts/chassis-dualbar-v1.json
GUIDE_SCENE_DEFINES := \
	-D 'CHASSIS_VARIANT="$(GUIDE_CHASSIS_VARIANT)"' \
	-D 'CARRIER_LINK_REVISION="stack_clear_v2"' \
	-D 'EXAMPLE_DEVICE_VARIANT="$(GUIDE_EXAMPLE_DEVICE_VARIANT)"'

FIXTURE_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-v1.stl
FIXTURE_COMPONENTS_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-components.stl
FIXTURE_LABELS_STL := ../dut-fixture-v1/build/pocketforge-dut-fixture-labels.stl
FIXTURE_RELAY_PCB_STL := ../dut-fixture-v1/build/pocketforge-elegoo-relay-pcb.stl
FIXTURE_RELAY_BLUE_STL := ../dut-fixture-v1/build/pocketforge-elegoo-relay-blue.stl
FIXTURE_RELAY_DARK_STL := ../dut-fixture-v1/build/pocketforge-elegoo-relay-dark.stl
FIXTURE_RELAY_METAL_STL := ../dut-fixture-v1/build/pocketforge-elegoo-relay-metal.stl
FIXTURE_RELAY_LED_STL := ../dut-fixture-v1/build/pocketforge-elegoo-relay-led.stl
FIXTURE_RELAY_SILKSCREEN_STL := ../dut-fixture-v1/build/pocketforge-elegoo-relay-silkscreen.stl
FIXTURE_BOOST_PCB_STL := ../dut-fixture-v1/build/pocketforge-hiletgo-xl6009-pcb.stl
FIXTURE_BOOST_DARK_STL := ../dut-fixture-v1/build/pocketforge-hiletgo-xl6009-dark.stl
FIXTURE_BOOST_ADJUSTER_STL := ../dut-fixture-v1/build/pocketforge-hiletgo-xl6009-adjuster.stl
FIXTURE_BOOST_METAL_STL := ../dut-fixture-v1/build/pocketforge-hiletgo-xl6009-metal.stl
FIXTURE_BOOST_SILKSCREEN_STL := ../dut-fixture-v1/build/pocketforge-hiletgo-xl6009-silkscreen.stl
FIXTURE_MOSFET_PCB_STL := ../dut-fixture-v1/build/pocketforge-ceksezx-mtsd001-pcb.stl
FIXTURE_MOSFET_BLUE_STL := ../dut-fixture-v1/build/pocketforge-ceksezx-mtsd001-blue.stl
FIXTURE_MOSFET_DARK_STL := ../dut-fixture-v1/build/pocketforge-ceksezx-mtsd001-dark.stl
FIXTURE_MOSFET_METAL_STL := ../dut-fixture-v1/build/pocketforge-ceksezx-mtsd001-metal.stl
FIXTURE_MOSFET_LED_STL := ../dut-fixture-v1/build/pocketforge-ceksezx-mtsd001-led.stl
FIXTURE_MOSFET_SILKSCREEN_STL := ../dut-fixture-v1/build/pocketforge-ceksezx-mtsd001-silkscreen.stl
FIXTURE_DP100_SHELL_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-shell.stl
FIXTURE_DP100_DARK_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-dark.stl
FIXTURE_DP100_CONTROLS_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-controls.stl
FIXTURE_DP100_SCREEN_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-screen.stl
FIXTURE_DP100_ACCENT_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-accent.stl
FIXTURE_DP100_METAL_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-metal.stl
FIXTURE_DP100_MARKINGS_STL := ../dut-fixture-v1/build/pocketforge-alientek-dp100-markings.stl
FIXTURE_BPI_PCB_STL := ../dut-fixture-v1/build/pocketforge-bpi-m2-zero-pcb.stl
FIXTURE_BPI_DARK_STL := ../dut-fixture-v1/build/pocketforge-bpi-m2-zero-dark.stl
FIXTURE_BPI_METAL_STL := ../dut-fixture-v1/build/pocketforge-bpi-m2-zero-metal.stl
FIXTURE_BPI_GOLD_STL := ../dut-fixture-v1/build/pocketforge-bpi-m2-zero-gold.stl
FIXTURE_BPI_SILKSCREEN_STL := ../dut-fixture-v1/build/pocketforge-bpi-m2-zero-silkscreen.stl
FIXTURE_ESP32_PCB_STL := ../dut-fixture-v1/build/pocketforge-esp32-s3-supermini-pcb.stl
FIXTURE_ESP32_DARK_STL := ../dut-fixture-v1/build/pocketforge-esp32-s3-supermini-dark.stl
FIXTURE_ESP32_METAL_STL := ../dut-fixture-v1/build/pocketforge-esp32-s3-supermini-metal.stl
FIXTURE_ESP32_GOLD_STL := ../dut-fixture-v1/build/pocketforge-esp32-s3-supermini-gold.stl
FIXTURE_ESP32_ANTENNA_STL := ../dut-fixture-v1/build/pocketforge-esp32-s3-supermini-antenna.stl
FIXTURE_ESP32_SILKSCREEN_STL := ../dut-fixture-v1/build/pocketforge-esp32-s3-supermini-silkscreen.stl
FIXTURE_C270_SHELL_STL := ../dut-fixture-v1/build/pocketforge-logitech-c270-shell.stl
FIXTURE_C270_DARK_STL := ../dut-fixture-v1/build/pocketforge-logitech-c270-dark.stl
FIXTURE_C270_GLASS_STL := ../dut-fixture-v1/build/pocketforge-logitech-c270-glass.stl
FIXTURE_C270_LED_STL := ../dut-fixture-v1/build/pocketforge-logitech-c270-led.stl
FIXTURE_C270_LABELS_STL := ../dut-fixture-v1/build/pocketforge-logitech-c270-labels.stl
FIXTURE_ANTENNA_DARK_STL := ../dut-fixture-v1/build/pocketforge-eightwood-ewua0205-dark.stl
FIXTURE_ANTENNA_METAL_STL := ../dut-fixture-v1/build/pocketforge-eightwood-ewua0205-metal.stl
FIXTURE_ANTENNA_MARKINGS_STL := ../dut-fixture-v1/build/pocketforge-eightwood-ewua0205-markings.stl
FIXTURE_VIENON_SHELL_STL := ../dut-fixture-v1/build/pocketforge-vienon-usb-001-shell.stl
FIXTURE_VIENON_DARK_STL := ../dut-fixture-v1/build/pocketforge-vienon-usb-001-dark.stl
FIXTURE_VIENON_METAL_STL := ../dut-fixture-v1/build/pocketforge-vienon-usb-001-metal.stl
FIXTURE_VIENON_BLUE_STL := ../dut-fixture-v1/build/pocketforge-vienon-usb-001-blue.stl
FIXTURE_VIENON_LED_STL := ../dut-fixture-v1/build/pocketforge-vienon-usb-001-led.stl
FIXTURE_SMAYS_SHELL_STL := ../dut-fixture-v1/build/pocketforge-smays-microb-hub-8152-shell.stl
FIXTURE_SMAYS_DARK_STL := ../dut-fixture-v1/build/pocketforge-smays-microb-hub-8152-dark.stl
FIXTURE_SMAYS_METAL_STL := ../dut-fixture-v1/build/pocketforge-smays-microb-hub-8152-metal.stl
FIXTURE_SMAYS_LED_STL := ../dut-fixture-v1/build/pocketforge-smays-microb-hub-8152-led.stl
FIXTURE_SMAYS_MARKINGS_STL := ../dut-fixture-v1/build/pocketforge-smays-microb-hub-8152-markings.stl
CRADLE_BODY_STL := ../dut-cradle-v1/build/trimui-smart-pro-family-carrier-body.stl
CRADLE_LABELS_STL := ../dut-cradle-v1/build/trimui-smart-pro-labels.stl
CRADLE_S_LABELS_STL := ../dut-cradle-v1/build/trimui-smart-pro-s-labels.stl
CRADLE_HOOKS_STL := ../dut-cradle-v1/build/trimui-smart-pro-family-installed-hooks.stl

PRESENTATION_IMPORT_DIR := $(BUILD)/imports
PRESENTATION_FIXTURE_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-v1.stl
PRESENTATION_FIXTURE_COMPONENTS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-components.stl
PRESENTATION_FIXTURE_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-dut-fixture-labels.stl
PRESENTATION_FIXTURE_RELAY_PCB_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-elegoo-relay-pcb.stl
PRESENTATION_FIXTURE_RELAY_BLUE_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-elegoo-relay-blue.stl
PRESENTATION_FIXTURE_RELAY_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-elegoo-relay-dark.stl
PRESENTATION_FIXTURE_RELAY_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-elegoo-relay-metal.stl
PRESENTATION_FIXTURE_RELAY_LED_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-elegoo-relay-led.stl
PRESENTATION_FIXTURE_RELAY_SILKSCREEN_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-elegoo-relay-silkscreen.stl
PRESENTATION_FIXTURE_BOOST_PCB_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-hiletgo-xl6009-pcb.stl
PRESENTATION_FIXTURE_BOOST_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-hiletgo-xl6009-dark.stl
PRESENTATION_FIXTURE_BOOST_ADJUSTER_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-hiletgo-xl6009-adjuster.stl
PRESENTATION_FIXTURE_BOOST_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-hiletgo-xl6009-metal.stl
PRESENTATION_FIXTURE_BOOST_SILKSCREEN_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-hiletgo-xl6009-silkscreen.stl
PRESENTATION_FIXTURE_MOSFET_PCB_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-ceksezx-mtsd001-pcb.stl
PRESENTATION_FIXTURE_MOSFET_BLUE_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-ceksezx-mtsd001-blue.stl
PRESENTATION_FIXTURE_MOSFET_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-ceksezx-mtsd001-dark.stl
PRESENTATION_FIXTURE_MOSFET_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-ceksezx-mtsd001-metal.stl
PRESENTATION_FIXTURE_MOSFET_LED_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-ceksezx-mtsd001-led.stl
PRESENTATION_FIXTURE_MOSFET_SILKSCREEN_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-ceksezx-mtsd001-silkscreen.stl
PRESENTATION_FIXTURE_DP100_SHELL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-shell.stl
PRESENTATION_FIXTURE_DP100_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-dark.stl
PRESENTATION_FIXTURE_DP100_CONTROLS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-controls.stl
PRESENTATION_FIXTURE_DP100_SCREEN_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-screen.stl
PRESENTATION_FIXTURE_DP100_ACCENT_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-accent.stl
PRESENTATION_FIXTURE_DP100_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-metal.stl
PRESENTATION_FIXTURE_DP100_MARKINGS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-alientek-dp100-markings.stl
PRESENTATION_FIXTURE_BPI_PCB_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-bpi-m2-zero-pcb.stl
PRESENTATION_FIXTURE_BPI_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-bpi-m2-zero-dark.stl
PRESENTATION_FIXTURE_BPI_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-bpi-m2-zero-metal.stl
PRESENTATION_FIXTURE_BPI_GOLD_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-bpi-m2-zero-gold.stl
PRESENTATION_FIXTURE_BPI_SILKSCREEN_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-bpi-m2-zero-silkscreen.stl
PRESENTATION_FIXTURE_ESP32_PCB_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-esp32-s3-supermini-pcb.stl
PRESENTATION_FIXTURE_ESP32_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-esp32-s3-supermini-dark.stl
PRESENTATION_FIXTURE_ESP32_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-esp32-s3-supermini-metal.stl
PRESENTATION_FIXTURE_ESP32_GOLD_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-esp32-s3-supermini-gold.stl
PRESENTATION_FIXTURE_ESP32_ANTENNA_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-esp32-s3-supermini-antenna.stl
PRESENTATION_FIXTURE_ESP32_SILKSCREEN_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-esp32-s3-supermini-silkscreen.stl
PRESENTATION_FIXTURE_C270_SHELL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-logitech-c270-shell.stl
PRESENTATION_FIXTURE_C270_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-logitech-c270-dark.stl
PRESENTATION_FIXTURE_C270_GLASS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-logitech-c270-glass.stl
PRESENTATION_FIXTURE_C270_LED_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-logitech-c270-led.stl
PRESENTATION_FIXTURE_C270_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-logitech-c270-labels.stl
PRESENTATION_FIXTURE_ANTENNA_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-eightwood-ewua0205-dark.stl
PRESENTATION_FIXTURE_ANTENNA_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-eightwood-ewua0205-metal.stl
PRESENTATION_FIXTURE_ANTENNA_MARKINGS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-eightwood-ewua0205-markings.stl
PRESENTATION_FIXTURE_VIENON_SHELL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-vienon-usb-001-shell.stl
PRESENTATION_FIXTURE_VIENON_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-vienon-usb-001-dark.stl
PRESENTATION_FIXTURE_VIENON_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-vienon-usb-001-metal.stl
PRESENTATION_FIXTURE_VIENON_BLUE_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-vienon-usb-001-blue.stl
PRESENTATION_FIXTURE_VIENON_LED_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-vienon-usb-001-led.stl
PRESENTATION_FIXTURE_SMAYS_SHELL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-smays-microb-hub-8152-shell.stl
PRESENTATION_FIXTURE_SMAYS_DARK_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-smays-microb-hub-8152-dark.stl
PRESENTATION_FIXTURE_SMAYS_METAL_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-smays-microb-hub-8152-metal.stl
PRESENTATION_FIXTURE_SMAYS_LED_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-smays-microb-hub-8152-led.stl
PRESENTATION_FIXTURE_SMAYS_MARKINGS_STL := $(PRESENTATION_IMPORT_DIR)/pocketforge-smays-microb-hub-8152-markings.stl
PRESENTATION_CRADLE_BODY_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-family-carrier-body.stl
PRESENTATION_CRADLE_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-labels.stl
PRESENTATION_CRADLE_S_LABELS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-s-labels.stl
PRESENTATION_CRADLE_HOOKS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-family-installed-hooks.stl

DEVICE_MODEL_COMMIT := 80662c40bd7d878a19127899760bdafb1f149173
DEVICE_MODEL_SHA256 := 0d5c8153639537d5e70941492ad2cc930f5fb1c93f3694e9a160f5770693224d
DEVICE_MODEL_URL := https://raw.githubusercontent.com/pocketforge-os/platform/$(DEVICE_MODEL_COMMIT)/device-models/trimui-smart-pro-s/trimui-smart-pro-s.scad
PRESENTATION_DEVICE_SCAD := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-s-device-model.scad
PRESENTATION_DEVICE_SHELL_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-s-device-shell.stl
PRESENTATION_DEVICE_CONTROLS_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-s-device-controls.stl
PRESENTATION_DEVICE_SCREEN_STL := $(PRESENTATION_IMPORT_DIR)/trimui-smart-pro-s-device-screen.stl

PRESENTATION_ASSETS := \
	$(PRESENTATION_FIXTURE_STL) \
	$(PRESENTATION_FIXTURE_COMPONENTS_STL) \
	$(PRESENTATION_FIXTURE_LABELS_STL) \
	$(PRESENTATION_FIXTURE_RELAY_PCB_STL) \
	$(PRESENTATION_FIXTURE_RELAY_BLUE_STL) \
	$(PRESENTATION_FIXTURE_RELAY_DARK_STL) \
	$(PRESENTATION_FIXTURE_RELAY_METAL_STL) \
	$(PRESENTATION_FIXTURE_RELAY_LED_STL) \
	$(PRESENTATION_FIXTURE_RELAY_SILKSCREEN_STL) \
	$(PRESENTATION_FIXTURE_BOOST_PCB_STL) \
	$(PRESENTATION_FIXTURE_BOOST_DARK_STL) \
	$(PRESENTATION_FIXTURE_BOOST_ADJUSTER_STL) \
	$(PRESENTATION_FIXTURE_BOOST_METAL_STL) \
	$(PRESENTATION_FIXTURE_BOOST_SILKSCREEN_STL) \
	$(PRESENTATION_FIXTURE_MOSFET_PCB_STL) \
	$(PRESENTATION_FIXTURE_MOSFET_BLUE_STL) \
	$(PRESENTATION_FIXTURE_MOSFET_DARK_STL) \
	$(PRESENTATION_FIXTURE_MOSFET_METAL_STL) \
	$(PRESENTATION_FIXTURE_MOSFET_LED_STL) \
	$(PRESENTATION_FIXTURE_MOSFET_SILKSCREEN_STL) \
	$(PRESENTATION_FIXTURE_DP100_SHELL_STL) \
	$(PRESENTATION_FIXTURE_DP100_DARK_STL) \
	$(PRESENTATION_FIXTURE_DP100_CONTROLS_STL) \
	$(PRESENTATION_FIXTURE_DP100_SCREEN_STL) \
	$(PRESENTATION_FIXTURE_DP100_ACCENT_STL) \
	$(PRESENTATION_FIXTURE_DP100_METAL_STL) \
	$(PRESENTATION_FIXTURE_DP100_MARKINGS_STL) \
	$(PRESENTATION_FIXTURE_BPI_PCB_STL) \
	$(PRESENTATION_FIXTURE_BPI_DARK_STL) \
	$(PRESENTATION_FIXTURE_BPI_METAL_STL) \
	$(PRESENTATION_FIXTURE_BPI_GOLD_STL) \
	$(PRESENTATION_FIXTURE_BPI_SILKSCREEN_STL) \
	$(PRESENTATION_FIXTURE_ESP32_PCB_STL) \
	$(PRESENTATION_FIXTURE_ESP32_DARK_STL) \
	$(PRESENTATION_FIXTURE_ESP32_METAL_STL) \
	$(PRESENTATION_FIXTURE_ESP32_GOLD_STL) \
	$(PRESENTATION_FIXTURE_ESP32_ANTENNA_STL) \
	$(PRESENTATION_FIXTURE_ESP32_SILKSCREEN_STL) \
	$(PRESENTATION_FIXTURE_C270_SHELL_STL) \
	$(PRESENTATION_FIXTURE_C270_DARK_STL) \
	$(PRESENTATION_FIXTURE_C270_GLASS_STL) \
	$(PRESENTATION_FIXTURE_C270_LED_STL) \
	$(PRESENTATION_FIXTURE_C270_LABELS_STL) \
	$(PRESENTATION_FIXTURE_ANTENNA_DARK_STL) \
	$(PRESENTATION_FIXTURE_ANTENNA_METAL_STL) \
	$(PRESENTATION_FIXTURE_ANTENNA_MARKINGS_STL) \
	$(PRESENTATION_FIXTURE_VIENON_SHELL_STL) \
	$(PRESENTATION_FIXTURE_VIENON_DARK_STL) \
	$(PRESENTATION_FIXTURE_VIENON_METAL_STL) \
	$(PRESENTATION_FIXTURE_VIENON_BLUE_STL) \
	$(PRESENTATION_FIXTURE_VIENON_LED_STL) \
	$(PRESENTATION_FIXTURE_SMAYS_SHELL_STL) \
	$(PRESENTATION_FIXTURE_SMAYS_DARK_STL) \
	$(PRESENTATION_FIXTURE_SMAYS_METAL_STL) \
	$(PRESENTATION_FIXTURE_SMAYS_LED_STL) \
	$(PRESENTATION_FIXTURE_SMAYS_MARKINGS_STL) \
	$(PRESENTATION_CRADLE_BODY_STL) \
	$(PRESENTATION_CRADLE_LABELS_STL) \
	$(PRESENTATION_CRADLE_S_LABELS_STL) \
	$(PRESENTATION_CRADLE_HOOKS_STL) \
	$(PRESENTATION_DEVICE_SHELL_STL) \
	$(PRESENTATION_DEVICE_CONTROLS_STL) \
	$(PRESENTATION_DEVICE_SCREEN_STL)

CHASSIS_CORE_BATCHES := \
	$(BUILD)/production-batch-01-ironed-interfaces.stl \
	$(BUILD)/production-batch-02-splice-collars.stl \
	$(BUILD)/production-batch-03-movable-mounts.stl \
	$(BUILD)/production-batch-04-frame-hardware.stl \
	$(BUILD)/production-batch-05-placard-holder.stl

DUALBAR_CORE_BATCHES := \
	$(DUALBAR_BUILD)/production-batch-01-ironed-interfaces.stl \
	$(DUALBAR_BUILD)/production-batch-02-fixture-links.stl \
	$(DUALBAR_BUILD)/production-batch-04-frame-hardware.stl \
	$(DUALBAR_BUILD)/production-batch-05-placard-holder.stl

DUALBAR_REPLACEMENT_PARTS := \
	$(DUALBAR_BUILD)/dualbar-fixture-link.stl \
	$(DUALBAR_BUILD)/dualbar-fixture-link-set.stl

DUALBAR_REVIEW := \
	$(DUALBAR_BUILD)/layout-assembly.png \
	$(DUALBAR_BUILD)/layout-front.png \
	$(DUALBAR_BUILD)/layout-suspension-detail.png \
	$(DUALBAR_BUILD)/layout-preload.png \
	$(DUALBAR_BUILD)/layout-ironed-interfaces.png \
	$(DUALBAR_BUILD)/layout-fixture-links.png

BRICK_DUALBAR_REVIEW := \
	$(BRICK_DUALBAR_BUILD)/layout-assembly.png \
	$(BRICK_DUALBAR_BUILD)/layout-front.png \
	$(BRICK_DUALBAR_BUILD)/layout-device-side.png

DEVICE_EXAMPLE_BATCHES := \
	$(BUILD)/production-batch-06-device-nameplate.stl \
	$(BUILD)/production-batch-07-wire-management.stl

PRODUCTION_BATCHES := $(CHASSIS_CORE_BATCHES) $(DEVICE_EXAMPLE_BATCHES)

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
	$(BUILD)/m3-slide-nut-fit-coupon.stl \
	$(BUILD)/cable-tie-anchor.stl \
	$(BUILD)/cable-tie-anchor-m3.stl \
	$(BUILD)/cable-tie-anchor-set.stl

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
	$(GUIDE_BUILD)/wire-management-anchor.png \
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
	$(GUIDE_BUILD)/detail-06-carrier-link-lengths-stack-clear.png \
	$(GUIDE_BUILD)/detail-07-fixture-spacers.png \
	$(GUIDE_BUILD)/detail-07-optical-axis.png \
	$(GUIDE_BUILD)/detail-08-placard.png \
	$(GUIDE_BUILD)/detail-08-power-strip.png \
	$(GUIDE_BUILD)/detail-08-stacking-corner.png

# Ordered, current-design stills for the novice assembly walkthrough. Keep
# these names stable: the handbook publishes one route per image and verifies
# the sequence byte-for-byte.
GUIDE_DUALBAR_ASSEMBLY_STEPS := \
	$(GUIDE_BUILD)/assembly-01-channel-bar.png \
	$(GUIDE_BUILD)/assembly-02-width-rails.png \
	$(GUIDE_BUILD)/assembly-03-depth-rails.png \
	$(GUIDE_BUILD)/assembly-04-fixture-bars.png \
	$(GUIDE_BUILD)/assembly-05-lower-frame.png \
	$(GUIDE_BUILD)/assembly-06-lower-fixture-bar.png \
	$(GUIDE_BUILD)/assembly-07-posts.png \
	$(GUIDE_BUILD)/assembly-08-upper-ring.png \
	$(GUIDE_BUILD)/assembly-09-upper-fixture-bar.png \
	$(GUIDE_BUILD)/assembly-10-close-frame.png \
	$(GUIDE_BUILD)/assembly-11-square-frame.png \
	$(GUIDE_BUILD)/assembly-12-dut-holder.png \
	$(GUIDE_BUILD)/assembly-13-fixture-board.png \
	$(GUIDE_BUILD)/assembly-14-placard.png \
	$(GUIDE_BUILD)/assembly-15-power-strip.png \
	$(GUIDE_BUILD)/assembly-16-stacking-tabs.png \
	$(GUIDE_BUILD)/assembly-17-final.png

GUIDE_BATCH_PREVIEWS := \
	$(GUIDE_BUILD)/batch-00-calibration.png \
	$(GUIDE_BUILD)/batch-01-ironed-interfaces.png \
	$(GUIDE_BUILD)/batch-02-fixture-links.png \
	$(GUIDE_BUILD)/batch-04-frame-hardware.png \
	$(GUIDE_BUILD)/batch-05-placard-holder.png \
	$(GUIDE_BUILD)/batch-06-device-nameplate.png \
	$(GUIDE_BUILD)/batch-07-wire-management.png \
	$(GUIDE_BUILD)/cable-anchor-m5.png \
	$(GUIDE_BUILD)/cable-anchor-m3.png

GUIDE_BATCH_MODELS := \
	$(GUIDE_BUILD)/batch-00-calibration.glb \
	$(GUIDE_BUILD)/batch-01-ironed-interfaces.glb \
	$(GUIDE_BUILD)/batch-02-fixture-links.glb \
	$(GUIDE_BUILD)/batch-04-frame-hardware.glb \
	$(GUIDE_BUILD)/batch-05-placard-holder.glb \
	$(GUIDE_BUILD)/batch-06-device-nameplate.glb \
	$(GUIDE_BUILD)/batch-07-wire-management.glb \
	$(GUIDE_BUILD)/cable-anchor-m5.glb \
	$(GUIDE_BUILD)/cable-anchor-m3.glb

GUIDE_LAYERS := \
	$(GUIDE_LAYER_BUILD)/aluminum.stl \
	$(GUIDE_LAYER_BUILD)/connectors.stl \
	$(GUIDE_LAYER_BUILD)/printed-hardware.stl \
	$(GUIDE_LAYER_BUILD)/fixture-plate.stl \
	$(GUIDE_LAYER_BUILD)/fixture-components.stl \
	$(GUIDE_LAYER_BUILD)/fixture-labels.stl \
	$(GUIDE_LAYER_BUILD)/fixture-relay-pcb.stl \
	$(GUIDE_LAYER_BUILD)/fixture-relay-blue.stl \
	$(GUIDE_LAYER_BUILD)/fixture-relay-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-relay-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-relay-led.stl \
	$(GUIDE_LAYER_BUILD)/fixture-relay-silkscreen.stl \
	$(GUIDE_LAYER_BUILD)/fixture-boost-pcb.stl \
	$(GUIDE_LAYER_BUILD)/fixture-boost-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-boost-adjuster.stl \
	$(GUIDE_LAYER_BUILD)/fixture-boost-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-boost-silkscreen.stl \
	$(GUIDE_LAYER_BUILD)/fixture-mosfet-pcb.stl \
	$(GUIDE_LAYER_BUILD)/fixture-mosfet-blue.stl \
	$(GUIDE_LAYER_BUILD)/fixture-mosfet-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-mosfet-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-mosfet-led.stl \
	$(GUIDE_LAYER_BUILD)/fixture-mosfet-silkscreen.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-shell.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-controls.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-screen.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-accent.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-dp100-markings.stl \
	$(GUIDE_LAYER_BUILD)/fixture-bpi-pcb.stl \
	$(GUIDE_LAYER_BUILD)/fixture-bpi-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-bpi-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-bpi-gold.stl \
	$(GUIDE_LAYER_BUILD)/fixture-bpi-silkscreen.stl \
	$(GUIDE_LAYER_BUILD)/fixture-esp32-pcb.stl \
	$(GUIDE_LAYER_BUILD)/fixture-esp32-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-esp32-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-esp32-gold.stl \
	$(GUIDE_LAYER_BUILD)/fixture-esp32-antenna.stl \
	$(GUIDE_LAYER_BUILD)/fixture-esp32-silkscreen.stl \
	$(GUIDE_LAYER_BUILD)/fixture-antenna-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-antenna-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-antenna-markings.stl \
	$(GUIDE_LAYER_BUILD)/fixture-vienon-shell.stl \
	$(GUIDE_LAYER_BUILD)/fixture-vienon-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-vienon-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-vienon-blue.stl \
	$(GUIDE_LAYER_BUILD)/fixture-vienon-led.stl \
	$(GUIDE_LAYER_BUILD)/fixture-smays-shell.stl \
	$(GUIDE_LAYER_BUILD)/fixture-smays-dark.stl \
	$(GUIDE_LAYER_BUILD)/fixture-smays-metal.stl \
	$(GUIDE_LAYER_BUILD)/fixture-smays-led.stl \
	$(GUIDE_LAYER_BUILD)/fixture-smays-markings.stl \
	$(GUIDE_LAYER_BUILD)/carrier-body.stl \
	$(GUIDE_LAYER_BUILD)/carrier-labels.stl \
	$(GUIDE_LAYER_BUILD)/carrier-hooks.stl \
	$(GUIDE_LAYER_BUILD)/device-shell.stl \
	$(GUIDE_LAYER_BUILD)/device-controls.stl \
	$(GUIDE_LAYER_BUILD)/device-screen.stl \
	$(GUIDE_LAYER_BUILD)/webcam-shell.stl \
	$(GUIDE_LAYER_BUILD)/webcam-dark.stl \
	$(GUIDE_LAYER_BUILD)/webcam-glass.stl \
	$(GUIDE_LAYER_BUILD)/webcam-led.stl \
	$(GUIDE_LAYER_BUILD)/webcam-labels.stl \
	$(GUIDE_LAYER_BUILD)/power-strip.stl \
	$(GUIDE_LAYER_BUILD)/placard-holder.stl \
	$(GUIDE_LAYER_BUILD)/placard-insert.stl \
	$(GUIDE_LAYER_BUILD)/placard-labels.stl \
	$(GUIDE_LAYER_BUILD)/camera-frustum.stl

GUIDE_CAMERA := --projection=ortho --camera=560,-650,470,173,179,184
GUIDE_IMAGE := --imgsize=1400,1100 --viewall $(GUIDE_CAMERA)
GUIDE_MESH_DEPS := $(SOURCE) lib/pf-2020.scad $(PRESENTATION_ASSETS)

# The public full-chassis scene is the current Smart Pro S dual-bar layout.
# `private` prevents these presentation-only selections from leaking into
# prerequisite production/device exports.
$(GUIDE_LAYERS): private OPENSCAD_FLAGS += $(GUIDE_SCENE_DEFINES)
$(GUIDE_BUILD)/hero.png: private OPENSCAD_FLAGS += $(GUIDE_SCENE_DEFINES)
$(GUIDE_DUALBAR_ASSEMBLY_STEPS): private OPENSCAD_FLAGS += $(GUIDE_SCENE_DEFINES)

.NOTPARALLEL:

.PHONY: all batches core-batches dualbar dualbar-batches dualbar-preview \
	brick-dualbar-preview \
	dualbar-replacements device-example-batches calibration \
	replacements fabrication-tools right-angle-checker lint preview \
	presentation-assets \
	guide-static guide-dualbar-assembly-steps guide-batch-models \
	guide-layers guide-model handbook-assets \
	cutlist refresh-cut-list dualbar-cutlist refresh-dualbar-cut-list \
	validate-cut-list-sync validate-dualbar-cut-list-sync \
	validate validate-right-angle-checker validate-margin-guard \
	validate-fov-guard validate-nut-carrier-guard \
	validate-gantry-travel-guard validate-registration-tab-guard \
	validate-power-strip-guard \
	validate-cable-anchor-guard \
	validate-cable-anchor-variants \
	validate-production-batches validate-dualbar-batches \
	validate-dualbar-guard validate-target-contract clean

all: batches replacements fabrication-tools cutlist

batches: core-batches

core-batches: $(CHASSIS_CORE_BATCHES)

dualbar: dualbar-batches dualbar-replacements dualbar-preview dualbar-cutlist

dualbar-batches: $(DUALBAR_CORE_BATCHES)

dualbar-replacements: $(DUALBAR_REPLACEMENT_PARTS)

dualbar-preview: $(DUALBAR_REVIEW)

brick-dualbar-preview: $(BRICK_DUALBAR_REVIEW)

device-example-batches: $(DEVICE_EXAMPLE_BATCHES)

calibration: $(CALIBRATION)

replacements: $(REPLACEMENT_PARTS)

fabrication-tools: right-angle-checker

right-angle-checker: $(RIGHT_ANGLE_CHECKER_STL) \
	$(RIGHT_ANGLE_CHECKER_PREVIEW)

$(BUILD) $(DUALBAR_BUILD) $(BRICK_DUALBAR_BUILD) $(GUIDE_BUILD) $(GUIDE_LAYER_BUILD) \
$(GUIDE_BATCH_LAYER_BUILD) \
$(GUIDE_MODEL_BUILD) $(PRESENTATION_IMPORT_DIR):
	mkdir -p $@

lint:
	cd ../.. && OPENSCAD='$(OPENSCAD)' scripts/lint-openscad.sh

$(RIGHT_ANGLE_CHECKER_STL): $(RIGHT_ANGLE_CHECKER_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $<

$(RIGHT_ANGLE_CHECKER_PREVIEW): $(RIGHT_ANGLE_CHECKER_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1000 \
		--projection=ortho --viewall \
		--camera=210,-240,220,75,75,0 $<

$(RIGHT_ANGLE_CHECKER_CUSTOM_TEST): $(RIGHT_ANGLE_CHECKER_SOURCE) | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'leg_length=100' -D 'arm_width=22' \
		-D 'thickness=4' -D 'inside_corner_relief_radius=3' \
		-D 'outside_corner_chamfer=1.5' -D 'show_label=false' $<

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

$(DUALBAR_BUILD)/dualbar-fixture-link.stl: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="dualbar_fixture_link"' $<

$(DUALBAR_BUILD)/dualbar-fixture-link-set.stl: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="dualbar_fixture_link_set"' $<

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
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="registration_tab"' $<

$(BUILD)/stacking-registration-tab-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="registration_tab_set"' $<

$(BUILD)/rail-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="rail_fit_coupon"' $<

$(BUILD)/m3-slide-nut-carrier.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_slide_nut"' $<

$(BUILD)/m3-slide-nut-carrier-set.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_slide_nut_set"' $<

$(BUILD)/m3-slide-nut-fit-coupon.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="m3_slide_nut_coupon"' $<

$(BUILD)/cable-tie-anchor.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="cable_tie_anchor"' $<

$(BUILD)/cable-tie-anchor-m3.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CABLE_ANCHOR_FASTENER="M3"' \
		-D 'PART="cable_tie_anchor"' $<

$(BUILD)/cable-tie-anchor-set.stl: \
		$(BUILD)/production-batch-07-wire-management.stl | $(BUILD)
	cp $< $@

$(BUILD)/production-batch-00-calibration.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_00_calibration"' $<

$(BUILD)/production-batch-01-ironed-interfaces.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_01_ironed_interfaces"' $<

$(BUILD)/production-batch-02-splice-collars.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_02_splice_collars"' $<

$(BUILD)/production-batch-03-movable-mounts.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_03_movable_mounts"' $<

$(DUALBAR_BUILD)/production-batch-01-ironed-interfaces.stl: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_dualbar_01_ironed_interfaces"' $<

$(DUALBAR_BUILD)/production-batch-02-fixture-links.stl: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_dualbar_02_fixture_links"' $<

$(DUALBAR_BUILD)/production-batch-04-frame-hardware.stl: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_04_frame_hardware"' $<

$(DUALBAR_BUILD)/production-batch-05-placard-holder.stl: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_05_placard_holder"' $<

$(BUILD)/production-batch-04-frame-hardware.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_04_frame_hardware"' $<

$(BUILD)/production-batch-05-placard-holder.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_05_placard_holder"' $<

$(BUILD)/production-batch-06-device-nameplate.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_06_device_nameplate"' $<

$(BUILD)/production-batch-07-wire-management.stl: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="production_batch_07_wire_management"' $<

$(FIXTURE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-v1.stl

$(FIXTURE_COMPONENTS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-components.stl

$(FIXTURE_LABELS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-dut-fixture-labels.stl

$(FIXTURE_RELAY_PCB_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-elegoo-relay-pcb.stl

$(FIXTURE_RELAY_BLUE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-elegoo-relay-blue.stl

$(FIXTURE_RELAY_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-elegoo-relay-dark.stl

$(FIXTURE_RELAY_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-elegoo-relay-metal.stl

$(FIXTURE_RELAY_LED_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-elegoo-relay-led.stl

$(FIXTURE_RELAY_SILKSCREEN_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-elegoo-relay-silkscreen.stl

$(FIXTURE_BOOST_PCB_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-hiletgo-xl6009-pcb.stl

$(FIXTURE_BOOST_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-hiletgo-xl6009-dark.stl

$(FIXTURE_BOOST_ADJUSTER_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-hiletgo-xl6009-adjuster.stl

$(FIXTURE_BOOST_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-hiletgo-xl6009-metal.stl

$(FIXTURE_BOOST_SILKSCREEN_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-hiletgo-xl6009-silkscreen.stl

$(FIXTURE_MOSFET_PCB_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-ceksezx-mtsd001-pcb.stl

$(FIXTURE_MOSFET_BLUE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-ceksezx-mtsd001-blue.stl

$(FIXTURE_MOSFET_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-ceksezx-mtsd001-dark.stl

$(FIXTURE_MOSFET_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-ceksezx-mtsd001-metal.stl

$(FIXTURE_MOSFET_LED_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-ceksezx-mtsd001-led.stl

$(FIXTURE_MOSFET_SILKSCREEN_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-ceksezx-mtsd001-silkscreen.stl

$(FIXTURE_DP100_SHELL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-shell.stl

$(FIXTURE_DP100_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-dark.stl

$(FIXTURE_DP100_CONTROLS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-controls.stl

$(FIXTURE_DP100_SCREEN_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-screen.stl

$(FIXTURE_DP100_ACCENT_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-accent.stl

$(FIXTURE_DP100_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-metal.stl

$(FIXTURE_DP100_MARKINGS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-alientek-dp100-markings.stl

$(FIXTURE_BPI_PCB_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-bpi-m2-zero-pcb.stl

$(FIXTURE_BPI_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-bpi-m2-zero-dark.stl

$(FIXTURE_BPI_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-bpi-m2-zero-metal.stl

$(FIXTURE_BPI_GOLD_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-bpi-m2-zero-gold.stl

$(FIXTURE_BPI_SILKSCREEN_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-bpi-m2-zero-silkscreen.stl

$(FIXTURE_ESP32_PCB_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-esp32-s3-supermini-pcb.stl

$(FIXTURE_ESP32_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-esp32-s3-supermini-dark.stl

$(FIXTURE_ESP32_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-esp32-s3-supermini-metal.stl

$(FIXTURE_ESP32_GOLD_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-esp32-s3-supermini-gold.stl

$(FIXTURE_ESP32_ANTENNA_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-esp32-s3-supermini-antenna.stl

$(FIXTURE_ESP32_SILKSCREEN_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-esp32-s3-supermini-silkscreen.stl

$(FIXTURE_C270_SHELL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-logitech-c270-shell.stl

$(FIXTURE_C270_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-logitech-c270-dark.stl

$(FIXTURE_C270_GLASS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-logitech-c270-glass.stl

$(FIXTURE_C270_LED_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-logitech-c270-led.stl

$(FIXTURE_C270_LABELS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-logitech-c270-labels.stl

$(FIXTURE_ANTENNA_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-eightwood-ewua0205-dark.stl

$(FIXTURE_ANTENNA_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-eightwood-ewua0205-metal.stl

$(FIXTURE_ANTENNA_MARKINGS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-eightwood-ewua0205-markings.stl

$(FIXTURE_VIENON_SHELL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-vienon-usb-001-shell.stl

$(FIXTURE_VIENON_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-vienon-usb-001-dark.stl

$(FIXTURE_VIENON_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-vienon-usb-001-metal.stl

$(FIXTURE_VIENON_BLUE_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-vienon-usb-001-blue.stl

$(FIXTURE_VIENON_LED_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-vienon-usb-001-led.stl

$(FIXTURE_SMAYS_SHELL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-smays-microb-hub-8152-shell.stl

$(FIXTURE_SMAYS_DARK_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-smays-microb-hub-8152-dark.stl

$(FIXTURE_SMAYS_METAL_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-smays-microb-hub-8152-metal.stl

$(FIXTURE_SMAYS_LED_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-smays-microb-hub-8152-led.stl

$(FIXTURE_SMAYS_MARKINGS_STL):
	$(MAKE) -C ../dut-fixture-v1 build/pocketforge-smays-microb-hub-8152-markings.stl

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

$(PRESENTATION_FIXTURE_RELAY_PCB_STL): $(FIXTURE_RELAY_PCB_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_RELAY_BLUE_STL): $(FIXTURE_RELAY_BLUE_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_RELAY_DARK_STL): $(FIXTURE_RELAY_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_RELAY_METAL_STL): $(FIXTURE_RELAY_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_RELAY_LED_STL): $(FIXTURE_RELAY_LED_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_RELAY_SILKSCREEN_STL): $(FIXTURE_RELAY_SILKSCREEN_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BOOST_PCB_STL): $(FIXTURE_BOOST_PCB_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BOOST_DARK_STL): $(FIXTURE_BOOST_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BOOST_ADJUSTER_STL): $(FIXTURE_BOOST_ADJUSTER_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BOOST_METAL_STL): $(FIXTURE_BOOST_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BOOST_SILKSCREEN_STL): $(FIXTURE_BOOST_SILKSCREEN_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_MOSFET_PCB_STL): $(FIXTURE_MOSFET_PCB_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_MOSFET_BLUE_STL): $(FIXTURE_MOSFET_BLUE_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_MOSFET_DARK_STL): $(FIXTURE_MOSFET_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_MOSFET_METAL_STL): $(FIXTURE_MOSFET_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_MOSFET_LED_STL): $(FIXTURE_MOSFET_LED_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_MOSFET_SILKSCREEN_STL): $(FIXTURE_MOSFET_SILKSCREEN_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_SHELL_STL): $(FIXTURE_DP100_SHELL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_DARK_STL): $(FIXTURE_DP100_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_CONTROLS_STL): $(FIXTURE_DP100_CONTROLS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_SCREEN_STL): $(FIXTURE_DP100_SCREEN_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_ACCENT_STL): $(FIXTURE_DP100_ACCENT_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_METAL_STL): $(FIXTURE_DP100_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_DP100_MARKINGS_STL): $(FIXTURE_DP100_MARKINGS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BPI_PCB_STL): $(FIXTURE_BPI_PCB_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BPI_DARK_STL): $(FIXTURE_BPI_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BPI_METAL_STL): $(FIXTURE_BPI_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BPI_GOLD_STL): $(FIXTURE_BPI_GOLD_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_BPI_SILKSCREEN_STL): $(FIXTURE_BPI_SILKSCREEN_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ESP32_PCB_STL): $(FIXTURE_ESP32_PCB_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ESP32_DARK_STL): $(FIXTURE_ESP32_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ESP32_METAL_STL): $(FIXTURE_ESP32_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ESP32_GOLD_STL): $(FIXTURE_ESP32_GOLD_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ESP32_ANTENNA_STL): $(FIXTURE_ESP32_ANTENNA_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ESP32_SILKSCREEN_STL): $(FIXTURE_ESP32_SILKSCREEN_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_C270_SHELL_STL): $(FIXTURE_C270_SHELL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_C270_DARK_STL): $(FIXTURE_C270_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_C270_GLASS_STL): $(FIXTURE_C270_GLASS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_C270_LED_STL): $(FIXTURE_C270_LED_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_C270_LABELS_STL): $(FIXTURE_C270_LABELS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ANTENNA_DARK_STL): $(FIXTURE_ANTENNA_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ANTENNA_METAL_STL): $(FIXTURE_ANTENNA_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_ANTENNA_MARKINGS_STL): $(FIXTURE_ANTENNA_MARKINGS_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_VIENON_SHELL_STL): $(FIXTURE_VIENON_SHELL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_VIENON_DARK_STL): $(FIXTURE_VIENON_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_VIENON_METAL_STL): $(FIXTURE_VIENON_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_VIENON_BLUE_STL): $(FIXTURE_VIENON_BLUE_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_VIENON_LED_STL): $(FIXTURE_VIENON_LED_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_SMAYS_SHELL_STL): $(FIXTURE_SMAYS_SHELL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_SMAYS_DARK_STL): $(FIXTURE_SMAYS_DARK_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_SMAYS_METAL_STL): $(FIXTURE_SMAYS_METAL_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_SMAYS_LED_STL): $(FIXTURE_SMAYS_LED_STL) | $(PRESENTATION_IMPORT_DIR)
	cp $< $@

$(PRESENTATION_FIXTURE_SMAYS_MARKINGS_STL): $(FIXTURE_SMAYS_MARKINGS_STL) | $(PRESENTATION_IMPORT_DIR)
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

$(DUALBAR_BUILD)/layout-assembly.png: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall \
		--camera=560,-650,470,173,179,184 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'EXAMPLE_DEVICE_VARIANT="smart_pro_s"' \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(DUALBAR_BUILD)/layout-front.png: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall \
		--camera=173,-600,184,173,179,184 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'EXAMPLE_DEVICE_VARIANT="smart_pro_s"' \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(BRICK_DUALBAR_BUILD)/layout-assembly.png: $(SOURCE) lib/pf-2020.scad | $(BRICK_DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall \
		--camera=560,-650,470,173,179,184 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'EXAMPLE_DEVICE_VARIANT="trimui_brick"' \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(BRICK_DUALBAR_BUILD)/layout-front.png: $(SOURCE) lib/pf-2020.scad | $(BRICK_DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall \
		--camera=173,-600,184,173,179,184 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'EXAMPLE_DEVICE_VARIANT="trimui_brick"' \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(BRICK_DUALBAR_BUILD)/layout-device-side.png: $(SOURCE) lib/pf-2020.scad | $(BRICK_DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,1200 \
		--projection=ortho --viewall \
		--camera=470,700,330,173,300,184 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'EXAMPLE_DEVICE_VARIANT="trimui_brick"' \
		-D 'PART="assembly"' -D 'PLATE_DETAIL="proxy"' $<

$(DUALBAR_BUILD)/layout-suspension-detail.png: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1300,1500 \
		--projection=ortho --viewall \
		--camera=260,-330,410,0,60,210 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="guide_dualbar_suspension_detail"' $<

$(DUALBAR_BUILD)/layout-preload.png: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,800 \
		--projection=ortho --autocenter --viewall \
		--camera=153,0,520,153,0,0 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="guide_dualbar_preload"' $<

$(DUALBAR_BUILD)/layout-ironed-interfaces.png: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,900 \
		--projection=ortho --viewall \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_dualbar_01_ironed_interfaces"' $<

$(DUALBAR_BUILD)/layout-fixture-links.png: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1000 \
		--projection=ortho --viewall \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_dualbar_02_fixture_links"' $<

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

$(BUILD)/layout-cable-tie-anchor.png: $(SOURCE) lib/pf-2020.scad | $(BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,800 \
		--projection=ortho --viewall --camera=70,-90,75,0,0,2 \
		-D 'PART="cable_tie_anchor"' $<

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

$(GUIDE_BUILD)/assembly-01-channel-bar.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,820 \
		--projection=ortho --camera=-70,-40,48,33,0,10 \
		-D 'PART="guide_dualbar_assembly_01_channel_bar"' $<

$(GUIDE_BUILD)/assembly-02-width-rails.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1800,700 \
		--projection=ortho --camera=352,20,850,352,20,0 \
		-D 'PART="guide_dualbar_assembly_02_width_rails"' $<

$(GUIDE_BUILD)/assembly-03-depth-rails.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,1200 \
		--projection=ortho --viewall --camera=185,175,1000,185,175,0 \
		-D 'PART="guide_dualbar_assembly_03_depth_rails"' $<

$(GUIDE_BUILD)/assembly-04-fixture-bars.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,800 \
		--projection=ortho --autocenter --viewall \
		--camera=153,0,520,153,0,0 \
		-D 'PART="guide_dualbar_assembly_04_fixture_bars"' $<

$(GUIDE_BUILD)/assembly-05-lower-frame.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_dualbar_assembly_05_lower_frame"' $<

$(GUIDE_BUILD)/assembly-06-lower-fixture-bar.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_dualbar_assembly_06_lower_fixture_bar"' $<

$(GUIDE_BUILD)/assembly-07-posts.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_dualbar_assembly_07_posts"' $<

$(GUIDE_BUILD)/assembly-08-upper-ring.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_dualbar_assembly_08_upper_ring"' $<

$(GUIDE_BUILD)/assembly-09-upper-fixture-bar.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_dualbar_assembly_09_upper_fixture_bar"' $<

$(GUIDE_BUILD)/assembly-10-close-frame.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_dualbar_assembly_10_close_frame"' $<

$(GUIDE_BUILD)/assembly-11-square-frame.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,1100 \
		--projection=ortho --viewall --camera=173,179,740,173,179,0 \
		-D 'PART="guide_dualbar_assembly_11_square_frame"' $<

$(GUIDE_BUILD)/assembly-12-dut-holder.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_dualbar_assembly_12_dut_holder"' $<

$(GUIDE_BUILD)/assembly-13-fixture-board.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ $(GUIDE_IMAGE) \
		-D 'PART="guide_dualbar_assembly_13_fixture_board"' $<

$(GUIDE_BUILD)/assembly-14-placard.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1500,800 \
		--projection=ortho --viewall --camera=520,-450,470,173,0,330 \
		-D 'PART="guide_dualbar_assembly_14_placard"' $<

$(GUIDE_BUILD)/assembly-15-power-strip.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --autocenter --viewall \
		--camera=650,-250,300,300,220,28 \
		-D 'PART="guide_dualbar_assembly_15_power_strip"' $<

$(GUIDE_BUILD)/assembly-16-stacking-tabs.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1000 \
		--projection=ortho --viewall --camera=-230,-240,510,20,20,370 \
		-D 'PART="guide_dualbar_assembly_16_stacking_tabs"' $<

$(GUIDE_BUILD)/assembly-17-final.png: $(GUIDE_MESH_DEPS) | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1800,1200 \
		--viewall $(GUIDE_CAMERA) \
		-D 'PART="guide_dualbar_assembly_17_final"' $<

$(GUIDE_BUILD)/prep-captive-nut.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,600 \
		--projection=ortho --camera=120,-135,95,0,0,0 \
		-D 'PART="guide_captive_nut_install"' $<

$(GUIDE_BUILD)/prep-captive-nut-count.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,620 \
		--projection=ortho --camera=165,25,675,165,25,0 \
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

$(GUIDE_BUILD)/wire-management-anchor.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1600,900 \
		--projection=ortho --camera=185,-235,170,0,0,18 \
		-D 'PART="guide_cable_tie_anchor_install"' $<

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

$(GUIDE_BUILD)/detail-06-carrier-link-lengths-stack-clear.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,760 \
		--projection=ortho --viewall --camera=0,-180,310,0,0,0 \
		-D 'CARRIER_LINK_REVISION="stack_clear_v2"' \
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
		--projection=ortho --autocenter --viewall \
		--camera=650,-250,300,300,220,28 \
		-D 'PART="guide_detail_08_power_strip"' $<

$(GUIDE_BUILD)/detail-08-stacking-corner.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1200,1000 \
		--projection=ortho --viewall --camera=-230,-240,510,20,20,370 \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="guide_detail_08_stacking_corner"' $<

$(GUIDE_BUILD)/batch-00-calibration.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,800 \
		--projection=ortho --viewall -D 'PART="production_batch_00_calibration"' $<

$(GUIDE_BUILD)/batch-01-ironed-interfaces.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,800 \
		--projection=ortho --viewall \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_dualbar_01_ironed_interfaces"' $<

$(GUIDE_BUILD)/batch-02-fixture-links.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --viewall \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_dualbar_02_fixture_links"' $<

$(GUIDE_BUILD)/batch-04-frame-hardware.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,900 \
		--projection=ortho --viewall \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="production_batch_04_frame_hardware"' $<

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

$(GUIDE_BUILD)/batch-07-wire-management.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1400,700 \
		--projection=ortho --viewall \
		--camera=78,-70,260,78,26,0 \
		-D 'PART="production_batch_07_wire_management"' $<

$(GUIDE_BUILD)/cable-anchor-m5.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,700 \
		--projection=ortho --viewall \
		-D 'PART="cable_tie_anchor"' $<

$(GUIDE_BUILD)/cable-anchor-m3.png: $(SOURCE) lib/pf-2020.scad | $(GUIDE_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ --imgsize=1000,700 \
		--projection=ortho --viewall \
		-D 'CABLE_ANCHOR_FASTENER="M3"' \
		-D 'PART="cable_tie_anchor"' $<

$(GUIDE_BUILD)/batch-00-calibration.glb: $(CALIBRATION) \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 00 calibration"

$(GUIDE_BUILD)/batch-01-ironed-interfaces.glb: \
		$(DUALBAR_BUILD)/production-batch-01-ironed-interfaces.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 01 ironed interfaces"

$(GUIDE_BUILD)/batch-02-fixture-links.glb: \
		$(DUALBAR_BUILD)/production-batch-02-fixture-links.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 02 fixture links"

$(GUIDE_BUILD)/batch-04-frame-hardware.glb: \
		$(DUALBAR_BUILD)/production-batch-04-frame-hardware.stl \
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

$(GUIDE_BUILD)/batch-07-wire-management.glb: \
		$(BUILD)/production-batch-07-wire-management.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "Batch 07 wire management"

$(GUIDE_BUILD)/cable-anchor-m5.glb: \
		$(BUILD)/cable-tie-anchor.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "M5 cable-tie anchor"

$(GUIDE_BUILD)/cable-anchor-m3.glb: \
		$(BUILD)/cable-tie-anchor-m3.stl \
		$(GUIDE_BATCH_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) | $(GUIDE_BUILD)
	$(PYTHON) $(GUIDE_BATCH_MODEL_SCRIPT) \
		--input $< --output $@ --name "M3 cable-tie anchor"

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

$(GUIDE_LAYER_BUILD)/fixture-relay-pcb.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_relay_pcb"' $<

$(GUIDE_LAYER_BUILD)/fixture-relay-blue.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_relay_blue"' $<

$(GUIDE_LAYER_BUILD)/fixture-relay-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_relay_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-relay-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_relay_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-relay-led.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_relay_led"' $<

$(GUIDE_LAYER_BUILD)/fixture-relay-silkscreen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_relay_silkscreen"' $<

$(GUIDE_LAYER_BUILD)/fixture-boost-pcb.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_boost_pcb"' $<

$(GUIDE_LAYER_BUILD)/fixture-boost-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_boost_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-boost-adjuster.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_boost_adjuster"' $<

$(GUIDE_LAYER_BUILD)/fixture-boost-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_boost_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-boost-silkscreen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_boost_silkscreen"' $<

$(GUIDE_LAYER_BUILD)/fixture-mosfet-pcb.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_mosfet_pcb"' $<

$(GUIDE_LAYER_BUILD)/fixture-mosfet-blue.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_mosfet_blue"' $<

$(GUIDE_LAYER_BUILD)/fixture-mosfet-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_mosfet_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-mosfet-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_mosfet_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-mosfet-led.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_mosfet_led"' $<

$(GUIDE_LAYER_BUILD)/fixture-mosfet-silkscreen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_mosfet_silkscreen"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-shell.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_shell"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-controls.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_controls"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-screen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_screen"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-accent.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_accent"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-dp100-markings.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_dp100_markings"' $<

$(GUIDE_LAYER_BUILD)/fixture-bpi-pcb.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_bpi_pcb"' $<

$(GUIDE_LAYER_BUILD)/fixture-bpi-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_bpi_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-bpi-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_bpi_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-bpi-gold.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_bpi_gold"' $<

$(GUIDE_LAYER_BUILD)/fixture-bpi-silkscreen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_bpi_silkscreen"' $<

$(GUIDE_LAYER_BUILD)/fixture-esp32-pcb.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_esp32_pcb"' $<

$(GUIDE_LAYER_BUILD)/fixture-esp32-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_esp32_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-esp32-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_esp32_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-esp32-gold.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_esp32_gold"' $<

$(GUIDE_LAYER_BUILD)/fixture-esp32-antenna.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_esp32_antenna"' $<

$(GUIDE_LAYER_BUILD)/fixture-esp32-silkscreen.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_esp32_silkscreen"' $<

$(GUIDE_LAYER_BUILD)/fixture-antenna-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_antenna_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-antenna-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_antenna_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-antenna-markings.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_antenna_markings"' $<

$(GUIDE_LAYER_BUILD)/fixture-vienon-shell.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_vienon_shell"' $<

$(GUIDE_LAYER_BUILD)/fixture-vienon-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_vienon_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-vienon-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_vienon_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-vienon-blue.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_vienon_blue"' $<

$(GUIDE_LAYER_BUILD)/fixture-vienon-led.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_vienon_led"' $<

$(GUIDE_LAYER_BUILD)/fixture-smays-shell.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_smays_shell"' $<

$(GUIDE_LAYER_BUILD)/fixture-smays-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_smays_dark"' $<

$(GUIDE_LAYER_BUILD)/fixture-smays-metal.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_smays_metal"' $<

$(GUIDE_LAYER_BUILD)/fixture-smays-led.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_smays_led"' $<

$(GUIDE_LAYER_BUILD)/fixture-smays-markings.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_fixture_smays_markings"' $<

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

$(GUIDE_LAYER_BUILD)/webcam-shell.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_webcam_shell"' $<

$(GUIDE_LAYER_BUILD)/webcam-dark.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_webcam_dark"' $<

$(GUIDE_LAYER_BUILD)/webcam-glass.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_webcam_glass"' $<

$(GUIDE_LAYER_BUILD)/webcam-led.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_webcam_led"' $<

$(GUIDE_LAYER_BUILD)/webcam-labels.stl: $(GUIDE_MESH_DEPS) | $(GUIDE_LAYER_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $@ -D 'PART="guide_layer_webcam_labels"' $<

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

guide-static: $(GUIDE_STEPS) $(GUIDE_DUALBAR_ASSEMBLY_STEPS) \
	$(GUIDE_BATCH_PREVIEWS)

guide-dualbar-assembly-steps: $(GUIDE_DUALBAR_ASSEMBLY_STEPS)

guide-batch-models: $(GUIDE_BATCH_MODELS)

guide-layers: $(GUIDE_LAYERS)

$(GUIDE_MODEL) $(GUIDE_MODEL_PROVENANCE) &: $(GUIDE_LAYERS) \
		$(GUIDE_MODEL_SCRIPT) $(GUIDE_MODEL_REQUIREMENTS) \
		$(GUIDE_DEVICE_REGISTRY) $(GUIDE_LAYOUT_RECORD) \
		$(PRESENTATION_DEVICE_SCAD) | $(GUIDE_MODEL_BUILD)
	$(PYTHON) $(GUIDE_MODEL_SCRIPT) \
		--layers $(GUIDE_LAYER_BUILD) \
		--output $(GUIDE_MODEL) \
		--provenance $(GUIDE_MODEL_PROVENANCE) \
		--repository-root ../.. \
		--source-repository $(SOURCE_REPOSITORY) \
		--device-slug $(GUIDE_DEVICE_SLUG) \
		--chassis-variant $(GUIDE_CHASSIS_VARIANT) \
		--device-registry $(GUIDE_DEVICE_REGISTRY) \
		--layout-record $(GUIDE_LAYOUT_RECORD) \
		--device-model-source $(PRESENTATION_DEVICE_SCAD) \
		--device-model-url $(DEVICE_MODEL_URL) \
		--device-model-commit $(DEVICE_MODEL_COMMIT) \
		--device-model-sha256 $(DEVICE_MODEL_SHA256)

guide-model: $(GUIDE_MODEL) $(GUIDE_MODEL_PROVENANCE)

handbook-assets: calibration dualbar-batches device-example-batches \
	guide-static guide-batch-models guide-model dualbar-cutlist

preview: $(BUILD)/layout-assembly.png $(BUILD)/layout-assembly-mesh.png \
	$(BUILD)/layout-front.png $(BUILD)/layout-stacked.png \
	$(BUILD)/layout-corner-joint.png $(BUILD)/layout-m3-slide-nut.png \
	$(BUILD)/layout-gantry-splice-installed.png \
	$(BUILD)/layout-placard-system.png \
	$(BUILD)/layout-power-strip-system.png \
	$(BUILD)/layout-cable-tie-anchor.png \
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

$(DUALBAR_BUILD)/cutlist.log: $(SOURCE) lib/pf-2020.scad | $(DUALBAR_BUILD)
	$(OPENSCAD) $(OPENSCAD_FLAGS) -o $(DUALBAR_BUILD)/cutlist.csg \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'PART="cutlist"' $< \
		>$(DUALBAR_BUILD)/cutlist.stdout 2>$@

$(DUALBAR_BUILD)/cut-list.csv $(DUALBAR_BUILD)/cut-list.md &: \
		$(DUALBAR_BUILD)/cutlist.log scripts/cutlist.py
	$(PYTHON) scripts/cutlist.py --input $(DUALBAR_BUILD)/cutlist.log \
		--csv $(DUALBAR_BUILD)/cut-list.csv \
		--markdown $(DUALBAR_BUILD)/cut-list.md

dualbar-cutlist: $(DUALBAR_BUILD)/cut-list.csv \
		$(DUALBAR_BUILD)/cut-list.md

refresh-dualbar-cut-list: dualbar-cutlist
	cp $(DUALBAR_BUILD)/cut-list.md $(DUALBAR_CUT_LIST)

validate-dualbar-cut-list-sync: dualbar-cutlist
	@cmp -s $(DUALBAR_BUILD)/cut-list.md $(DUALBAR_CUT_LIST) || { \
		echo 'ERROR: CUT_LIST_DUALBAR.md is stale; run make refresh-dualbar-cut-list' >&2; \
		diff -u $(DUALBAR_CUT_LIST) $(DUALBAR_BUILD)/cut-list.md || true; \
		exit 1; \
	}
	@echo 'dualbar_cut_list_sync=pass artifact=$(DUALBAR_CUT_LIST)'

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
	long_log=$(BUILD)/invalid-nut-carrier-long.log; \
	long_mesh=$(BUILD)/invalid-nut-carrier-long.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$long_mesh \
			-D 'PART="m3_slide_nut"' \
			-D 'm3_slide_nut_length=30' $(SOURCE) >$$long_log 2>&1; then \
		echo 'ERROR: overlong carrier was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'stay inside the fixture-upright landing envelope' $$long_log; \
	echo 'nut_carrier_guard=pass rejected_bearing_widths=6.7,12.2mm rejected_deep_width=8.7mm rejected_height=4.9mm rejected_length=30mm'

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

validate-registration-tab-guard: | $(BUILD)
	@set -eu; size_log=$(BUILD)/invalid-registration-tab-size.log; \
	size_mesh=$(BUILD)/invalid-registration-tab-size.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$size_mesh \
			-D 'PART="registration_tab"' \
			-D 'CHASSIS_VARIANT="dualbar_v1"' \
			-D 'registration_tab_size=[19,92,4]' \
			$(SOURCE) >$$size_log 2>&1; then \
		echo 'ERROR: 19 mm-wide registration tab was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'exactly 18 x 92 x 4 mm' $$size_log; \
	engagement_log=$(BUILD)/invalid-registration-tab-engagement.log; \
	engagement_mesh=$(BUILD)/invalid-registration-tab-engagement.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$engagement_mesh \
			-D 'PART="registration_tab"' \
			-D 'CHASSIS_VARIANT="dualbar_v1"' \
			-D 'registration_tab_size=[18,92,4]' \
			-D 'registration_lower_engagement=59' \
			$(SOURCE) >$$engagement_log 2>&1; then \
		echo 'ERROR: 59 mm registration engagement was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'require 60 mm lower engagement and 32 mm upper engagement' \
		$$engagement_log; \
	slot_log=$(BUILD)/invalid-registration-tab-slots.log; \
	slot_mesh=$(BUILD)/invalid-registration-tab-slots.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$slot_mesh \
			-D 'PART="registration_tab"' \
			-D 'CHASSIS_VARIANT="dualbar_v1"' \
			-D 'registration_lower_hole_y=[13,28]' \
			$(SOURCE) >$$slot_log 2>&1; then \
		echo 'ERROR: shifted registration lower slot was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'preserve the 12 and 28 mm screw datums' $$slot_log; \
	lock_log=$(BUILD)/invalid-registration-tab-upper-lock.log; \
	lock_mesh=$(BUILD)/invalid-registration-tab-upper-lock.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$lock_mesh \
			-D 'PART="registration_tab"' \
			-D 'CHASSIS_VARIANT="dualbar_v1"' \
			-D 'registration_upper_lock_y=70' \
			$(SOURCE) >$$lock_log 2>&1; then \
		echo 'ERROR: former 70 mm registration upper lock was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'preserve the owner-corrected 77 mm datum' $$lock_log; \
	web_log=$(BUILD)/invalid-registration-tab-upper-web.log; \
	web_mesh=$(BUILD)/invalid-registration-tab-upper-web.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$web_mesh \
			-D 'PART="registration_tab"' \
			-D 'CHASSIS_VARIANT="dualbar_v1"' \
			-D 'registration_upper_lock_y=88' \
			-D 'registration_upper_lock_corner_clearance=18' \
			$(SOURCE) >$$web_log 2>&1; then \
		echo 'ERROR: undersized registration upper-hole edge web was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'at least 4 mm of material above the hole' $$web_log; \
	count_log=$(BUILD)/invalid-registration-tab-count.log; \
	count_mesh=$(BUILD)/invalid-registration-tab-count.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$count_mesh \
			-D 'PART="registration_tab_set"' \
			-D 'CHASSIS_VARIANT="dualbar_v1"' \
			-D 'registration_tab_count=7' \
			$(SOURCE) >$$count_log 2>&1; then \
		echo 'ERROR: seven-tab frame batch was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'exactly eight registration tabs' $$count_log; \
	echo 'registration_tab_guard=pass variant=dualbar_v1 size=18x92x4mm lower=60mm upper=32mm lower_slots=12,28mm upper_lock=77mm corner_clearance_shift=7mm count=8'

validate-cable-anchor-guard: | $(BUILD)
	@set -eu; count_log=$(BUILD)/invalid-cable-anchor-count.log; \
	count_mesh=$(BUILD)/invalid-cable-anchor-count.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$count_mesh \
			-D 'PART="production_batch_07_wire_management"' \
			-D 'cable_anchor_count=7' $(SOURCE) >$$count_log 2>&1; then \
		echo 'ERROR: seven-anchor starter batch was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'must contain exactly eight anchors' $$count_log; \
	tunnel_log=$(BUILD)/invalid-cable-anchor-tunnel.log; \
	tunnel_mesh=$(BUILD)/invalid-cable-anchor-tunnel.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$tunnel_mesh \
			-D 'PART="cable_tie_anchor"' \
			-D 'cable_anchor_tie_passage=[4.8,2.0]' \
			$(SOURCE) >$$tunnel_log 2>&1; then \
		echo 'ERROR: undersized cable-tie tunnel was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'need 0.8 mm clearance' $$tunnel_log; \
	roof_log=$(BUILD)/invalid-cable-anchor-roof.log; \
	roof_mesh=$(BUILD)/invalid-cable-anchor-roof.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$roof_mesh \
			-D 'PART="cable_tie_anchor"' \
			-D 'cable_anchor_bridge_roof=0.8' \
			$(SOURCE) >$$roof_log 2>&1; then \
		echo 'ERROR: thin cable-anchor roof was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'need two 0.8 mm nozzle lines' $$roof_log; \
	wide_log=$(BUILD)/invalid-cable-anchor-width.log; \
	wide_mesh=$(BUILD)/invalid-cable-anchor-width.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$wide_mesh \
			-D 'PART="cable_tie_anchor"' \
			-D 'cable_anchor_size=[32,19]' \
			$(SOURCE) >$$wide_log 2>&1; then \
		echo 'ERROR: over-wide cable anchor was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'stay inside the 2020 rail face' $$wide_log; \
	fastener_log=$(BUILD)/invalid-cable-anchor-fastener.log; \
	fastener_mesh=$(BUILD)/invalid-cable-anchor-fastener.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$fastener_mesh \
			-D 'PART="cable_tie_anchor"' \
			-D 'CABLE_ANCHOR_FASTENER="M4"' \
			$(SOURCE) >$$fastener_log 2>&1; then \
		echo 'ERROR: unsupported cable-anchor fastener was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'fastener must be M5 or M3' $$fastener_log; \
	echo 'cable_anchor_guard=pass count=8 fasteners=M5,M3 max_tie=4.8x1.6mm min_wall=1.6mm rail_face=18mm'

validate-cable-anchor-variants: \
		$(BUILD)/cable-tie-anchor.stl \
		$(BUILD)/cable-tie-anchor-m3.stl
	$(PYTHON) $(FINGERPRINT) $(BUILD)/cable-tie-anchor.stl | \
		grep -q '"sha256":"fe1fad2cf300a4dbe6ee94395209fc40e8e118265f12c07000ab29d5cab933ec"'
	$(PYTHON) $(FINGERPRINT) $(BUILD)/cable-tie-anchor-m3.stl | \
		grep -q '"sha256":"14121c2a05192250a53125dfc31c7b43db2285736af5432d46807ae496eca3de"'
	@echo 'cable_anchor_variants=pass m5_baseline=preserved m3_baseline=locked'

validate-production-batches: $(CALIBRATION) $(PRODUCTION_BATCHES) \
		$(BUILD)/stacking-registration-tab.stl \
		$(BUILD)/stacking-registration-tab-set.stl \
		$(BUILD)/cable-tie-anchor.stl \
		$(BUILD)/cable-tie-anchor-m3.stl \
		$(BUILD)/cable-tie-anchor-set.stl
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
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 9 \
		$(BUILD)/production-batch-07-wire-management.stl
	$(PYTHON) $(BOUNDS) --max-x 18 --max-y 92 --max-z 4 \
		$(BUILD)/stacking-registration-tab.stl
	$(PYTHON) $(BOUNDS) --max-x 90 --max-y 190 --max-z 4 \
		$(BUILD)/stacking-registration-tab-set.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 1 \
		$(BUILD)/stacking-registration-tab.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 8 \
		$(BUILD)/stacking-registration-tab-set.stl
	$(PYTHON) $(BOUNDS) --max-x 32 --max-y 18 --max-z 8.8 \
		$(BUILD)/cable-tie-anchor.stl
	$(PYTHON) $(BOUNDS) --max-x 32 --max-y 18 --max-z 8.8 \
		$(BUILD)/cable-tie-anchor-m3.stl
	$(PYTHON) $(BOUNDS) \
		--equivalent-to $(BUILD)/production-batch-07-wire-management.stl \
		$(BUILD)/cable-tie-anchor-set.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 1 \
		$(BUILD)/cable-tie-anchor.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 1 \
		$(BUILD)/cable-tie-anchor-m3.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 8 \
		$(BUILD)/production-batch-07-wire-management.stl
	@echo 'production_batches=pass common_core=5 device_examples=2 optional_calibration=pass registration_tabs=8 cable_anchors=8'

validate-dualbar-batches: $(DUALBAR_CORE_BATCHES) \
		$(DUALBAR_REPLACEMENT_PARTS) \
		$(BUILD)/production-batch-04-frame-hardware.stl \
		$(BUILD)/production-batch-05-placard-holder.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 5 \
		$(DUALBAR_BUILD)/production-batch-01-ironed-interfaces.stl
	$(PYTHON) $(BOUNDS) --max-x 247 --max-y 207 --max-z 7 \
		$(DUALBAR_BUILD)/production-batch-02-fixture-links.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 28 \
		$(DUALBAR_BUILD)/production-batch-01-ironed-interfaces.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 8 \
		$(DUALBAR_BUILD)/production-batch-02-fixture-links.stl
	$(PYTHON) $(FINGERPRINT) \
		$(BUILD)/production-batch-04-frame-hardware.stl | \
		grep -q '"sha256":"911d249f2b8e7120b46d86c9a25f85a4a1edbf64944c05615911681a01e0cb25"'
	$(PYTHON) $(FINGERPRINT) \
		$(DUALBAR_BUILD)/production-batch-04-frame-hardware.stl | \
		grep -q '"sha256":"31ddea2c53c3d93cb6f64cca11c123b39d071879b9e172839c0ea87c75307601"'
	$(PYTHON) $(BOUNDS) \
		--equivalent-to $(BUILD)/production-batch-05-placard-holder.stl \
		$(DUALBAR_BUILD)/production-batch-05-placard-holder.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 1 \
		$(DUALBAR_BUILD)/dualbar-fixture-link.stl
	$(PYTHON) $(TOPOLOGY) --expected-components 4 \
		$(DUALBAR_BUILD)/dualbar-fixture-link-set.stl
	@echo 'dualbar_batches=pass core=4 captive_bars=28 fixture_links=4 printed_crossbar_joints=4 revised_batch=04 shared_batch=05'

validate-dualbar-guard: | $(DUALBAR_BUILD)
	@set -eu; variant_log=$(DUALBAR_BUILD)/invalid-variant.log; \
	variant_mesh=$(DUALBAR_BUILD)/invalid-variant.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$variant_mesh \
		-D 'CHASSIS_VARIANT="unknown"' \
		-D 'PART="dualbar_fixture_link"' $(SOURCE) \
		>$$variant_log 2>&1; then \
		echo 'ERROR: unknown chassis variant was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'Unknown chassis variant' $$variant_log; \
	carrier_log=$(DUALBAR_BUILD)/invalid-carrier-link-revision.log; \
	carrier_mesh=$(DUALBAR_BUILD)/invalid-carrier-link-revision.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$carrier_mesh \
		-D 'CARRIER_LINK_REVISION="unknown"' \
		-D 'PART="rear_carrier_link_set"' $(SOURCE) \
		>$$carrier_log 2>&1; then \
		echo 'ERROR: unknown carrier-link revision was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'Unknown carrier-link revision' $$carrier_log; \
	bed_log=$(DUALBAR_BUILD)/invalid-fixture-link-bed.log; \
	bed_mesh=$(DUALBAR_BUILD)/invalid-fixture-link-bed.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$bed_mesh \
		-D 'CHASSIS_VARIANT="dualbar_v1"' \
		-D 'dualbar_link_batch_gap=70' \
		-D 'PART="dualbar_fixture_link_set"' $(SOURCE) \
		>$$bed_log 2>&1; then \
		echo 'ERROR: overlong dual-bar fixture-link bed was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'Four-link dual-bar batch must fit the 247 x 207 mm print bed' $$bed_log; \
	echo 'dualbar_guard=pass rejected_unknown_variant=unknown rejected_unknown_carrier_revision=unknown rejected_overlong_link_bed=true'

validate-power-strip-guard: | $(BUILD)
	@set -eu; log=$(BUILD)/invalid-power-strip-position.log; \
	mesh=$(BUILD)/invalid-power-strip-position.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
		-D 'power_strip_device_y=500' \
		-D 'PART="power_strip_system_preview"' $(SOURCE) \
		>$$log 2>&1; then \
		echo 'ERROR: out-of-bounds power strip was not rejected' >&2; exit 1; \
	fi; \
	grep -q 'Power strip must fit between the operator/device corner posts' $$log; \
	echo 'power_strip_guard=pass rejected_device_y=500'

validate-target-contract:
	$(PYTHON) $(TARGET_CONTRACT_TEST)

validate-right-angle-checker: $(RIGHT_ANGLE_CHECKER_STL) \
		$(RIGHT_ANGLE_CHECKER_PREVIEW) \
		$(RIGHT_ANGLE_CHECKER_CUSTOM_TEST)
	@set -eu; \
	report=$$($(PYTHON) $(BOUNDS) --max-x 150 --max-y 150 --max-z 5 \
		--bed-x 247 --bed-y 207 $(RIGHT_ANGLE_CHECKER_STL)); \
	printf '%s\n' "$$report"; \
	printf '%s\n' "$$report" | grep -q 'size=150.000,150.000,5.000'
	$(PYTHON) $(TOPOLOGY) --expected-components 1 \
		$(RIGHT_ANGLE_CHECKER_STL)
	$(PYTHON) $(RIGHT_ANGLE_CHECKER_GEOMETRY) \
		--leg-length 150 --arm-width 25 --thickness 5 \
		--inside-relief 4 --outside-chamfer 2 \
		$(RIGHT_ANGLE_CHECKER_STL)
	@set -eu; \
	report=$$($(PYTHON) $(BOUNDS) --max-x 100 --max-y 100 --max-z 4 \
		--bed-x 247 --bed-y 207 $(RIGHT_ANGLE_CHECKER_CUSTOM_TEST)); \
	printf '%s\n' "$$report"; \
	printf '%s\n' "$$report" | grep -q 'size=100.000,100.000,4.000'
	$(PYTHON) $(TOPOLOGY) --expected-components 1 \
		$(RIGHT_ANGLE_CHECKER_CUSTOM_TEST)
	$(PYTHON) $(RIGHT_ANGLE_CHECKER_GEOMETRY) \
		--leg-length 100 --arm-width 22 --thickness 4 \
		--inside-relief 3 --outside-chamfer 1.5 \
		$(RIGHT_ANGLE_CHECKER_CUSTOM_TEST)
	@test -s $(RIGHT_ANGLE_CHECKER_PREVIEW)
	@set -eu; \
	log=$(BUILD)/invalid-right-angle-checker.log; \
	mesh=$(BUILD)/invalid-right-angle-checker.stl; \
	if $(OPENSCAD) $(OPENSCAD_FLAGS) -o $$mesh \
			-D 'leg_length=70' $(RIGHT_ANGLE_CHECKER_SOURCE) \
			>$$log 2>&1; then \
		echo 'ERROR: undersized right-angle checker was not rejected' >&2; \
		exit 1; \
	fi; \
	grep -q 'leg_length must be at least 80 mm' $$log; \
	echo 'right_angle_checker_guard=pass rejected_leg_length_mm=70'
	@echo 'right_angle_checker_validation=pass default=150x150x5 custom=100x100x4 angle_deg=90'

validate: lint all calibration preview validate-margin-guard \
	validate-fov-guard validate-nut-carrier-guard \
	validate-gantry-travel-guard validate-registration-tab-guard \
	validate-power-strip-guard \
	validate-cable-anchor-guard \
	validate-cable-anchor-variants \
	validate-production-batches validate-dualbar-batches \
	validate-dualbar-guard validate-target-contract \
	validate-right-angle-checker \
	validate-cut-list-sync validate-dualbar-cut-list-sync
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
	grep -q '^fixture_support_bar,2,306.00,612.00' $(DUALBAR_BUILD)/cut-list.csv
	! grep -q '^fixture_gantry_' $(DUALBAR_BUILD)/cut-list.csv
	grep -q 'Finished extrusion: 4548.00 mm' $(DUALBAR_BUILD)/cut-list.md
	grep -q 'Fixture-support savings: 656.00 mm (51.74%)' $(DUALBAR_BUILD)/cut-list.md
	grep -q 'three 306.00 mm fixture bars plus three kerfs consume \*\*927.60 mm\*\* and leave \*\*72.40 mm\*\*' $(DUALBAR_BUILD)/cut-list.md
	grep -q 'Bar 5: fixture_support_bar 306.00, fixture_support_bar 306.00; kerf-inclusive consumed 618.40 mm; remainder 381.60 mm' $(DUALBAR_BUILD)/cut-list.md
	@echo 'chassis_validation=pass legacy_core_batches=5 dualbar_qualified_core_batches=4 device_example_batches=2 legacy_stock_bars=6 dualbar_stock_bars=5 dualbar_savings_mm=656 handbook_major_steps=8 handbook_detail_panels=25 cable_anchors=8'

clean:
	rm -rf $(BUILD)
