#!/bin/bash

/scripts/test_build.sh $1
cd /dataset/repos/jasper
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    cve_2016_8691)
        src/appl/imginfo -f /dataset/cve_2016_8691/sample1.jp2
        ;;
    cve_2016_9387)
        src/appl/imginfo -f /dataset/cve_2016_9387/00003-jasper-assert-jas_matrix_t
        ;;
    cve_2016_9557)
        src/appl/imginfo -f /dataset/cve_2016_9557/exploit
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
