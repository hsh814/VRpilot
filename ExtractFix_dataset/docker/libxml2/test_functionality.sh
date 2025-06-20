#!/bin/bash

mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/libxml2/autogen.sh
make -j 32

case "$1" in
    EF15|EF16|EF17|EF18)
        cd /root/build_testsuite
        make check
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
