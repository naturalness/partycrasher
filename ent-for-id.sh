#!/bin/sh

report_id="$1"

# Extract the THIRD field from ent's terse output.
./recursion_info.py "$report_id" | ent -t | awk -F, 'NR == 2 { print $3 }'
