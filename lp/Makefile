.PHONY: all
all: top-functions.txt top-first-functions.txt

K = 10

# Create the top text files using Unix legos.
# awk 'NR>1' skips the header.
top-%.txt %.txt: %.csv
	<$< awk 'NR>1'|sort|uniq -c|sort -nr|tee $*.full.txt|head -n$(K) > $@


# Pasting this here to document that it exists...
DUMMY:
	awk 'BEGIN { print "count,id" } {print $$1 "," NR}' < first-functions.full.txt > first-functions-full.4zipfR.csv
