#!/bin/sh

filename="$1"

if [ ! -f "$filename" ]; then
    echo "could not read $filename..."
    exit 1
fi

tail -n +2 "$filename" | xargs -n 1 ./ent-for-id.sh
