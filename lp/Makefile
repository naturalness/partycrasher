.PHONY: all
all: top-functions.tex top-first-functions.tex

K = 10

# Create the top text files using Unix legos.
# awk 'NR>1' skips the header.
# The last awk command generates a LaTeX table row.
top-%.tex %.full.txt: %.csv
	<$< awk -F, 'NR>1 {} {print $$1}'|sort|uniq -c|sort -nr|tee $*.full.txt|\
		head -n$(K) |\
		awk '{ gsub("_", "\\_", $$2); print "    " ++i " & " $$1 " & \\texttt{" $$2 "} \\\\" }'  > $@

# Pasting this here to document that it exists...
DUMMY:
	awk 'BEGIN { print "count,id" } {print $$1 "," NR}' < first-functions.full.txt > first-functions-full.4zipfR.csv
