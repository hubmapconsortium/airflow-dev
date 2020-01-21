#!/usr/bin/env bash
set -o errexit

start() { echo travis_fold':'start:$1; echo $1; }
end() { echo travis_fold':'end:$1; }
die() { set +v; echo "$*" 1>&2 ; sleep 1; exit 1; }

pushd .

CWL_NAME=workflow.cwl
OUTPUT_NAME=test-output-actual
for CWL_PATH in workflows/cwl/*/workflow.cwl; do
  cd `dirname $CWL_PATH`
  LABEL=`basename $PWD`
  start $LABEL
  mkdir $OUTPUT_NAME || echo 'Output directory already exists...'
  cd $OUTPUT_NAME
  ../$CWL_NAME ../test-job.yml
  cd ..
  diff -w -r test-output-expected $OUTPUT_NAME -x .DS_Store | head -n100 | cut -c 1-100
  end $LABEL
done

popd
