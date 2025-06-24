#!/bin/bash

set -e

cd /dataset/repos/jasper
sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
autoreconf -i

mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/jasper/configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
make -j 32

case "$1" in
    cve_2016_8691)
        for f in data/images/*.mif data/images/*.jpg data/images/*.pnm /dataset/jasper_newtests/* ; do
            echo "$f"
            src/appl/imginfo -f "$f"
        done
        ;;
    cve_2016_9387)
        for f in data/images/*.mif data/images/*.jpg data/images/*.pnm /dataset/jasper_newtests/* ; do
            echo "$f"
            src/appl/imginfo -f "$f"
        done
        ;;
    cve_2016_9557)
        for f in data/images/*.mif data/images/*.jpg data/images/*.pnm /dataset/jasper_newtests/* ; do
            echo "$f"
            src/appl/imginfo -f "$f"
        done
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
