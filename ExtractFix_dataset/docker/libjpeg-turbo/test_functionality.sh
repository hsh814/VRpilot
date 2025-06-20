#!/bin/bash

mkdir -p /root/build_testsuite
case "$1" in
    EF19|EF22)
        cd /dataset/repos/libjpeg-turbo
        autoreconf -fvi
        cd /root/build
        /dataset/repos/libjpeg-turbo/configure
        ;;
    EF20|EF21)
        cd /root/build
        cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
make -j 32

case "$1" in
    EF19)
        ;;
    EF20)
        ;;
    EF21)
        ;;
    EF22)
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) test
