#!/bin/bash

mkdir -p /root/build_testsuite
case "$1" in
    EF19|cve_2012_2806)
        cd /dataset/repos/libjpeg-turbo
        autoreconf -fvi
        cd /root/build
        /dataset/repos/libjpeg-turbo/configure
        ;;
    cve_2018_19664|cve_2017_15232)
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
    cve_2018_19664)
        ;;
    cve_2017_15232)
        ;;
    cve_2012_2806)
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) test
