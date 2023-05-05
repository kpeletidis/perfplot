#!/bin/bash
## Script to split a dbench log file that includes multiple runs
## to one file per run.
## Kostas Peletidis, 2023-05-02
##
## Configuration (global) variables go here
MULTIRUN_PATTERN="PACKAGE"
TEST_RUN_PREFIX="test_run_"
DATA_PATTERN="execute"

## Helper global variables go here
flag_multirun=""

function is_multirun_log() {
  if [[ `grep "$MULTIRUN_PATTERN" $1 | wc -l` -gt 1 ]]; then
    echo "This log includes multiple runs. Splitting to individual logs..."
    return 0
  elif  [[ `grep "$MULTIRUN_PATTERN" $1 | wc -l` -eq 1 ]]; then
    return 1
  else
    echo "is_multirun_log: Log doesn't include "$MULTIRUN_PATTERN""
    return -1
  fi
}

function split_data() {
  echo "extract_data: infile=$1"
  is_multirun_log $1
  rv=$?
  echo "extract_data: rv: $rv"
  if [[ $rv -eq 0 ]]; then
    echo "extract_data: multirun log found!"
    flag_multirun=1
    csplit -z -b "%02d.dat" -f "$TEST_RUN_PREFIX" $1 /"$MULTIRUN_PATTERN"/ '{*}'
    echo "Detecting number of threads..."
    ## TODO: Consider moving the data extraction to another script or
    ## rename this file.
    # TODO: Either use a temp file or a dictionary to store thread numbers.
    # A temp file should be easier to process e.g. sort by thread number.
    for i in `ls "$TEST_RUN"*.dat`; do
      tnum=`grep -m 1 "$DATA_PATTERN" $i | awk '{print $1}'`
      echo "$i: $tnum"
    done
  else
    echo "This is NOT a multirun log"
    flag_multirun=0
  fi
  # Call data extractor for dbench tool
  ##echo [CALLING] extract_data_dbench "$1"
}

## TODO: Test that $1 is an existing file
split_data $1

