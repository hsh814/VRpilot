#!/bin/bash
mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/binutils-gdb/configure

case "$1" in
    EF12)
        make -j $(nproc) -C bfd check && make -j $(nproc) -C binutils check
        ;;
    EF13)
        make -j $(nproc) -C bfd check && make -j $(nproc) -C binutils check
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
