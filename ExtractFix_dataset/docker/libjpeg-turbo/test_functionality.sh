#!/bin/bash

export ASAN_OPTIONS=detect_leaks=0
/scripts/test_build.sh $1

case "$1" in
    EF19)
        ;;
    cve_2018_19664)
        ;;
    cve_2017_15232)
        ;;
    cve_2012_2806)
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) test
