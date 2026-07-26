PYTHON ?= python3
OPENSCAD ?= openscad
DEVICE ?= trimui-smart-pro
MODE ?= coupon
PACK_FLAGS ?=
PACK := build/$(DEVICE)/$(MODE)

.PHONY: build verify test

build:
	cd ../.. && $(PYTHON) mechanical/device-packs/build_device_pack.py build \
		--device '$(DEVICE)' --mode '$(MODE)' \
		--openscad '$(OPENSCAD)' $(PACK_FLAGS)

verify:
	cd ../.. && $(PYTHON) mechanical/device-packs/build_device_pack.py verify \
		--pack 'mechanical/device-packs/$(PACK)'

test:
	$(PYTHON) test_device_pack.py
