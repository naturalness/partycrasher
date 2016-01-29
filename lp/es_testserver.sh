#!/bin/bash -e
ES_HOME="/usr/share/elasticsearch/bin/"
LOG_DIR="$(pwd)/es/log"
mkdir -p "$LOG_DIR"
DATA_DIR="$(pwd)/es/data"
mkdir -p "$LOG_DIR"
WORK_DIR="$(pwd)/es/work"
mkdir -p "$WORK_DIR"
CONF_DIR="$(pwd)/es"
CONF_FILE="es/elasticsearch.yml"

"$ES_HOME/elasticsearch" \
    -Des.default.config=$CONF_FILE\
    -Des.default.path.home=$ES_HOME\
    -Des.default.path.logs=$LOG_DIR\
    -Des.default.path.data=$DATA_DIR\
    -Des.default.path.work=$WORK_DIR\
    -Des.default.path.conf=$CONF_DIR
