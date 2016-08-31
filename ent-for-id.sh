#!/bin/sh

# Prints the ID and the stack trace entropy on a single line.

report_id="$1"

# Extract the THIRD field from ent's terse output.
./recursion_info.py "$report_id" \
    | ent -t \
    | awk -F, 'NR == 2 { print "'"$report_id"'," $3 }'
