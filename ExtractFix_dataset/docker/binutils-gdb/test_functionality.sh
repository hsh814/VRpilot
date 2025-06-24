#!/bin/bash
mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/binutils-gdb/configure --disable-shared --disable-gdb --disable-libdecnumber --disable-readline --disable-sim LDFLAGS='-g -ldl -lutil'

case "$1" in
    cve_2017_14745|cve_2017_6965|cve_2018_10372|cve_2017_15025)
        make -j $(nproc) -C bfd check && make -j $(nproc) -C binutils check
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
