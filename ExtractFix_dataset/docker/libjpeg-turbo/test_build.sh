#!/bin/bash
export ASAN_OPTIONS=detect_leaks=0
cd /dataset/repos/libjpeg-turbo
case "$1" in
    EF19|cve_2012_2806|cve_2017_15232)
        autoreconf -fvi
        ./configure --without-simd CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
        ;;
    cve_2018_19664)
        CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" .
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
make -j 32
