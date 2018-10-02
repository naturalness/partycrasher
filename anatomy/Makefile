.PHONY: all

all: packagesfzm.svg packages.svg bucketsfzm.svg buckets.svg date_ranges.svg \
	date_v_size.svg signals.svg architectures.svg reclengths.svg \
	stacklengths.svg fnlengths.svg firstfzm.svg

# Downloads the bugkets
bugkets.txz:
		@if curl -o $@ https://pizza.cs.ualberta.ca/bugkets.txz ;\
		then	echo "Downloaded bugkets.txz" ;\
		else	echo "Failed to download bugkets.txz" ;\
			echo "Try downloading it from https://archive.org/details/bugkets-2016-07-22" ;\
			false ;\
		fi

bugkets: | bugkets.txz
	@echo "Decompressing bugkets... warning: this takes 2.3GiB"
	tar -xaf $<

venv: setup.py requirements.txt
	-rm -rf venv
	python3 -m virtualenv $@ -p python3
	. venv/bin/activate ; pip install -e .
	
.INTERMEDIATE: 2json
lp.json packages.csv buckets_dist.csv date_ranges.csv architectures.csv: 2json
signals.csv lengths.csv length_counts.csv unique_lengths.csv top_libs.csv: 2json

2json: bugkets venv
	@echo "Analyzing bugkets... warning: this takes lots of RAM"
	. venv/bin/activate ; python3 lp_files_to_json.py $< >lp.json

.INTERMEDIATE: plot2
packagesfzm.svg packages.svg bucketsfzm.svg buckets.svg date_ranges.svg: plot2
date_v_size.svg signals.svg architectures.svg reclengths.svg: plot2
stacklengths.svg fnlengths.svg firstfzm.svg: plot2

plot2: packages.csv buckets_dist.csv signals-filtered.csv \
	archives-filtered.csv length.csv stack_length.csv \
	unique_lengths.csv date_ranges.csv first-functions-full.4zipfR.csv \
	top_libs.csv

