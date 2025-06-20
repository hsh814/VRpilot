#!/bin/bash
mkdir -p /root/build
cd /root/build
case "$1" in
    EF12)
        /dataset/repos/binutils-gdb/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
        make -j 32
        ;;
    EF13)
        /dataset/repos/binutils-gdb/configure CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined"
        make -j 32
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
