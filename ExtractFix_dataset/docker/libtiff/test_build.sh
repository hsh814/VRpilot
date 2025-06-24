#!/bin/bash

cd /root/build

case "$1" in
    cve_2016_5321|EF04|EF06|cve_2016_10094)
        CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    cve_2017_7601|cve_2016_3623|cve_2017_7595|EF11)
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
