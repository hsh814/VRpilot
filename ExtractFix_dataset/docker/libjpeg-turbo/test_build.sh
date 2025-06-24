#!/bin/bash

mkdir -p /root/build

case "$1" in
    EF19|cve_2012_2806)
        cd /dataset/repos/libjpeg-turbo
        autoreconf -fvi
        cd /root/build
        /dataset/repos/libjpeg-turbo/configure CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
        ;;
    cve_2018_19664|EF21)
        cd /root/build
        CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
cd /root/build
make -j 32
