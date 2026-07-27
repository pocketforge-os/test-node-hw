PYTHON ?= python3
OPENSCAD ?= openscad
DEVICE ?= trimui-smart-pro
MODE ?= coupon
PROFILE_ID ?= trimui-smart-pro-family
PACK_FLAGS ?=
PACK := build/$(DEVICE)/$(MODE)

.PHONY: build verify release release-verify test

build:
	cd ../.. && $(PYTHON) mechanical/device-packs/build_device_pack.py build \
		--device '$(DEVICE)' --mode '$(MODE)' \
		--openscad '$(OPENSCAD)' $(PACK_FLAGS)

verify:
	cd ../.. && $(PYTHON) mechanical/device-packs/build_device_pack.py verify \
		--pack 'mechanical/device-packs/$(PACK)'

release:
	cd ../.. && $(PYTHON) mechanical/device-packs/release_print_pack.py build \
		--profile-id '$(PROFILE_ID)' --openscad '$(OPENSCAD)'

release-verify:
	cd ../.. && tag="$$($(PYTHON) \
		mechanical/device-packs/release_print_pack.py identity \
		--profile-id '$(PROFILE_ID)')" && \
		$(PYTHON) mechanical/device-packs/release_print_pack.py verify \
		--bundle "mechanical/device-packs/build/releases/$$tag"

test:
	$(PYTHON) -m unittest discover -p 'test_*.py' -v
