IMAGE_NAME = partycrasher:latest
EXTERNAL_PORT = 5000

# Stolen from:
# https://gist.github.com/rcmachado/af3db315e31383502660#gistcomment-1585632
.PHONY: help
help: ## Prints this message and exits
	$(info Available targets)
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		replaced = sub( /^## /, "", helpMsg ); \
		if (replaced == 0) { \
			helpMsg = $$0; \
			replaced = sub( /^[^:]*:.* ## /, "", helpMsg ); \
		} \
		if (replaced) \
			print  $$1 helpMsg; \
	} \
	{ helpMsg = $$0 }' \
	$(MAKEFILE_LIST) | column -ts:

.PHONY: start
start: ## Starts the server locally (does not use Docker).
	python partycrasher/rest_service.py \
		--port=$(EXTERNAL_PORT) \
		--debug \
		--allow-delete-all

.PHONY: build
build: ## Builds the `partycrasher` Docker image
	docker build --tag $(IMAGE_NAME) .

.PHONY: run
run: ## Runs the `partycrasher` Docker container.
	docker run -d -p $(EXTERNAL_PORT):5000/tcp --name partycrasher $(IMAGE_NAME)

.PHONY: kill
kill: ## Stops and removes the `partycrasher` container.
	docker rm -f partycrasher

.PHONY: test
test: kill build ## Runs the unit tests within a **new** `partycrasher` container.
	docker run -t -i --name partycrasher $(IMAGE_NAME) python setup.py test

.PHONY: reset
reset: build kill run ## Rebuilds the `partycrasher` container and runs it.

.PHONY: buckettest
buckettest: lp.json ## Destroys the database, uploads, and evaluates data from Launchpad.
	python lp/buckettest.py $< http://localhost:$(EXTERNAL_PORT)/

# Downloads the crashes.
lp.json.xz:
	curl --fail --remote-name https://pizza.cs.ualberta.ca/$@

%: %.xz
	xz --decompress --keep $<

