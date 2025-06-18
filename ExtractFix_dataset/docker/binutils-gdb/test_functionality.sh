#!/bin/bash

case "$1" in
    EF12)
        cd /root/build_testsuite_EF12
        make -j $(nproc) -C bfd check && make -j $(nproc) -C binutils check
        ;;
    EF13)
        cd /root/build_testsuite_EF13
        make -j $(nproc) -C bfd check && make -j $(nproc) -C binutils check
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
