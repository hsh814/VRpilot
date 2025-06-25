#!/bin/bash

/scripts/test_build.sh $1
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    cve_2013_7437)
        ./potrace /dataset/cve_2013_7437/exploit
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
