#!/bin/bash
mkdir -p /root/build
cd /root/build
case "$1" in
    cve_2017_14745|cve_2017_6965|cve_2018_10372)
        /dataset/repos/binutils-gdb/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
        make -j 32
        ;;
    cve_2017_15025)
        /dataset/repos/binutils-gdb/configure CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined"
        make -j 32
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
