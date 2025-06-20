#!/bin/bash

cd /dataset/repos/jasper
sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
autoreconf -i

mkdir -p /root/build
/dataset/repos/jasper/configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
make -j 32

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
