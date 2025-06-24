#!/bin/bash
mkdir -p /root/build
cd /root/build
export ASAN_OPTIONS=detect_leaks=0
case "$1" in
    cve_2017_14745|cve_2017_6965|cve_2018_10372)
        /dataset/repos/binutils-gdb/configure --disable-shared --disable-gdb --disable-libdecnumber --disable-readline --disable-sim LIBS='-g -fsanitize=address -ldl -lutil' CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address -ldl -lutil"
        make -j 32
        ;;
    cve_2017_15025)
        /dataset/repos/binutils-gdb/configure --disable-shared --disable-gdb --disable-libdecnumber --disable-readline --disable-sim LIBS='-g -fsanitize=undefined -ldl -lutil' CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined -ldl -lutil"
        make -j 32
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
