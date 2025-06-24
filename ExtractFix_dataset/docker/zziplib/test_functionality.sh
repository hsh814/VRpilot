#!/bin/bash

mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/zziplib/configure
make -j 32
exit 0
case "$1" in
    *)
        ;;
esac
