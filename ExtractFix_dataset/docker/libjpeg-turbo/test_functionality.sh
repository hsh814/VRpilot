#!/bin/bash

case "$1" in
    EF19)
        cd /root/build_testsuite_EF19
        ;;
    EF20)
        cd /root/build_testsuite_EF20
        ;;
    EF21)
        cd /root/build_testsuite_EF21
        ;;
    EF22)
        cd /root/build_testsuite_EF22
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) test
