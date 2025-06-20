#!/bin/bash

cd /dataset/repos/libarchive
autoreconf -i

mkdir -p /root/build_testsuite
cd /root/build_testsuite
ASAN_OPTIONS=detect_leaks=0 /dataset/repos/libarchive/configure --without-openssl
make -j 32

case "$1" in
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
