IMAGE_NAME = partycrasher:latest
EXTERNAL_PORT = 5000

SQLITE = sqlite3 -csv -header
CORPUS_NAME = lp_big

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
# 	gunicorn --access-logfile gunicorn-access.log \
# 		--error-logfile gunicorn-error.log \
# 		--log-level debug \
# 		--workers 32 \
# 		--worker-class sync \
# 		--bind localhost:5000 \
# 		--timeout 60 \
# 		--pid gunicorn.pid \
# 		--capture-output \
# 		--daemon partycrasher.rest_service_validator
# 	sleep 1
# 	echo "Gunicorn started on: " `cat gunicorn.pid`
# 	sleep 1
	python lp/buckettest.py $< http://localhost:$(EXTERNAL_PORT)/
# 	echo kill `cat gunicorn.pid`
# 	kill `cat gunicorn.pid`


# Output summaries
.PHONY:
summary: recursion.R $(CORPUS_NAME).sqlite
	Rscript $<

# Create the pickled corpus file.
$(CORPUS_NAME).sqlite: recursion_info.py $(CORPUS_NAME).json
	python $<

# Downloads the crashes.
%.json.xz:
	curl --fail --remote-name https://pizza.cs.ualberta.ca/$@

# How to decompress any xz file.
%: %.xz
	xz --decompress --keep $<

CSVS = $(addsuffix .csv,$(basename $(wildcard recursion_results/*.sql)))

.PHONY: csvs
csvs: $(CSVS) lp/functions.csv lp/first-functions.csv

lp/functions.csv: recursion_info.py $(CORPUS_NAME).sqlite
	./$< functions $@

lp/first-functions.csv: recursion_info.py $(CORPUS_NAME).sqlite
	./$< first-functions $@


# Create a CSV from an SQL query over the crashes database.
%.csv: %.sql $(CORPUS_NAME).sqlite
	sqlite3 -header -csv $(CORPUS_NAME).sqlite < $< > $@

recursion_results/entropy_with_recursion.csv: recursion_results/2000_with_recursion.csv
	echo "id,entropy" > $@
	./get-ent.sh $< >> $@

recursion_results/entropy_without_recursion.csv: recursion_results/2000_without_recursion.csv
	echo "id,entropy" > $@
	./get-ent.sh $< >> $@
