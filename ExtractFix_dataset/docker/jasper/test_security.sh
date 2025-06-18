#!/bin/bash

case "$1" in
    EF27)
        cd /dataset/repos/jasper_EF27
        src/appl/imginfo -f /dataset/EF27/sample1.jp2
        ;;
    EF28)
        cd /dataset/repos/jasper_EF28
        src/appl/imginfo -f /dataset/EF28/00003-jasper-assert-jas_matrix_t
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
