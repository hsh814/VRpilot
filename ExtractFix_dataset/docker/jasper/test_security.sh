#!/bin/bash

/scripts/test_build.sh $1
cd /root/build

case "$1" in
    EF27)
        src/appl/imginfo -f /dataset/EF27/sample1.jp2
        ;;
    EF28)
        src/appl/imginfo -f /dataset/EF28/00003-jasper-assert-jas_matrix_t
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
