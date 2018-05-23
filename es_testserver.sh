#!/bin/bash -e

ES_HOME="/usr/share/elasticsearch/bin/"
LOG_DIR="$(pwd)/es/log"
mkdir -p "$LOG_DIR"
DATA_DIR="$(pwd)/es/data"
mkdir -p "$DATA_DIR"
WORK_DIR="$(pwd)/es/work"
mkdir -p "$WORK_DIR"
CONF_DIR="$(pwd)/es"
CONF_FILE="es/elasticsearch.yml"
export ES_HEAP_SIZE=10g

"$ES_HOME/elasticsearch" -Epath.conf=$CONF_DIR \
 -Epath.logs=$LOG_DIR \
 -Epath.data=$DATA_DIR
