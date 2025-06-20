#!/bin/bash

cd /root/build

case "$1" in
    EF01|EF04|EF06|EF07)
        CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    EF08|EF09|EF10|EF11)
        CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    EF02_*)
        /dataset/repos/libtiff/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
        make -j 32
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
