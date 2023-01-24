#!/bin/sh
export SCRIPT_DIR=`dirname "$0"`
cd "$SCRIPT_DIR"
export AGENT_HOME=../../
export RUNJOBUTIL_HOME=${AGENT_HOME}/apps/runAJobCli
# echo base-- $BASE_DIR   -- strip $stripped -- dirname $dirName -- RUNJOBUTIL_HOME $RUNJOBUTIL_HOME -- pwd mypwd
#  Coping existing run a job cli folder for data backup
if [ -e "$RUNJOBUTIL_HOME/runAJobCli" ]
then cp -rf "$RUNJOBUTIL_HOME/runAJobCli" "$RUNJOBUTIL_HOME/runAJobCli_bak"
else echo "$RUNJOBUTIL_HOME/runAJobCli" "File doesn't exist:"
fi
echo "Done"
