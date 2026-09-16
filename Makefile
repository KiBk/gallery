SLUG ?= gallery
IMAGE ?= registry.kibk.net/apps/$(SLUG):latest
DOMAIN ?= $(SLUG).apps.kibk.net
PLATFORM ?= linux/amd64
PORT ?= 8080
HEBE_ROOT ?= /Users/kibk/hebe
HEBE_PUBLISH ?= $(HEBE_ROOT)/bin/hebe-publish
HEBE_REGISTRY ?= $(HEBE_ROOT)/bin/hebe-registry

.PHONY: check serve login build push push-crane publish verify release logout

check:
	python3 scripts/check_site.py --root .

serve: check
	python3 -m http.server $(PORT) --directory public

login:
	$(HEBE_REGISTRY) login

build: check
	docker build --platform $(PLATFORM) -t $(IMAGE) .

push:
	docker push $(IMAGE)

push-crane: check
	IMAGE=$(IMAGE) PLATFORM=$(PLATFORM) ./scripts/build-and-push-crane.sh

publish:
	$(HEBE_PUBLISH) app $(SLUG) --image $(IMAGE) --port 80 --health-path /healthz --private

verify:
	python3 scripts/verify_live.py --root . --url https://$(DOMAIN)

logout:
	$(HEBE_REGISTRY) logout

release: push-crane publish verify
