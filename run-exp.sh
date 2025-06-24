#!/bin/bash

source env/bin/activate
export PYTHONPATH=$(pwd)/src

projects=(
  "binutils-gdb"
  "coreutils"
  "jasper"
  "libjpeg-turbo"
  "libming"
  "libtiff"
  "libxml2"
  "zziplib"
)

mkdir -p tmp/log
for project in "${projects[@]}"; do
  (
    python3 src/main/rqs/rq2.py $project --model='o3-2025-04-16' >tmp/log/$project.log 2>&1
  ) &
done

wait
echo "Done"