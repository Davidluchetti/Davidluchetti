#!/bin/bash
export SCRIPT_DIR=`dirname "$0"`
cd "$SCRIPT_DIR"

export PRG_DIR="$(pwd)"

CLASSPATH="$PRG_DIR"
CLASSPATH="$CLASSPATH:$PRG_DIR/runAJobCli.jar"
CLASSPATH="$CLASSPATH:$PRG_DIR/lib/*"

java -cp "$CLASSPATH" -Duser.dir="$PRG_DIR" com.informatica.saas.RestClient "$@"

