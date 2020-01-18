#!/usr/bin/env bash
set -o errexit
set -o pipefail

start() { echo travis_fold':'start:$1; echo $1; }
end() { echo travis_fold':'end:$1; }
die() { set +v; echo "$*" 1>&2 ; sleep 1; exit 1; }

CWL_NAME=workflow.cwl
OUTPUT_NAME=test-output-actual
for CWL_PATH in $PWD/workflows/cwl/*/workflow.cwl; do
  cd `dirname $CWL_PATH`
  LABEL=`basename $PWD`
  start $LABEL
  rm -rf $OUTPUT_NAME
  mkdir $OUTPUT_NAME
  cd $OUTPUT_NAME
  ../$CWL_NAME ../test-job.yml
  cd ..
  diff -w -r test-output-expected $OUTPUT_NAME -x .DS_Store | head -n100 | cut -c 1-100
  end $LABEL
done
