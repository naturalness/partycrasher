#!/bin/sh

filename="$1"

if [ ! -x "$filename" ]; then
    echo "could not read $filename..."
    return 1
fi

tail -n +2 "$filename" | xargs -n 1 ./ent-for-id.sh
