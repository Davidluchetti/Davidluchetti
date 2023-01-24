#!/bin/bash
export SCRIPT_DIR=`dirname "$0"`
echo $SCRIPT_DIR
cd "$SCRIPT_DIR"

export PRG_DIR="$(pwd)"

CLASSPATH="$PRG_DIR"
CLASSPATH="$CLASSPATH:$PRG_DIR/com.activee.rt.hub.tf.paramset.cli.jar"

java -cp "$CLASSPATH" -Duser.dir="$PRG_DIR" com.activee.rt.hub.tf.paramset.cli.AeParamSetCliApp "$@"

