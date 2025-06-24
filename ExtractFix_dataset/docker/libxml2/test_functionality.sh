#!/bin/bash

mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/libxml2/autogen.sh
make -j 32

case "$1" in
    cve_2016_1838|EF16|cve_2012_5134|cve_2017_5969)
        cd /root/build_testsuite
        make check
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
