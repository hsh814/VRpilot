#!/bin/bash
cd /dataset/repos/libming
./autogen.sh

mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/libming/configure
make -j 32
exit 0

case "$1" in
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
