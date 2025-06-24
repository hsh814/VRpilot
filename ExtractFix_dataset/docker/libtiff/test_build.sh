#!/bin/bash

cd /root/build

case "$1" in
    bugzilla_2633|cve_2016_3186|cve_2016_5321|cve_2016_5314|cve_2016_9532|cve_2016_10094)
        CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    cve_2017_7601|cve_2016_3623|cve_2017_7595|cve_2017_7601|EF11)
        CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    cve_2014_8128)
        /dataset/repos/libtiff/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
        make -j 32
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
