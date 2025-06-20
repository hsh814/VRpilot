#!/bin/bash

mkdir -p /root/build
cd /root/build
/dataset/repos/libxml2/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 32

case "$1" in
    EF15)
        ./xmllint /dataset/EF15/attachment_316157.xml
        ;;
    EF16)
        ./xmllint --html /dataset/EF16/attachment_316182.xml
        ;;
    EF17)
        ./xmllint /dataset/EF17/reproducer-4.xml
        ;;
    EF18)
        ./xmllint --recover /dataset/EF18/crash-libxml2-recover.xml
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
