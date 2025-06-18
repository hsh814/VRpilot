#!/bin/bash

case "$1" in
    EF29)
        cd /root/build_testsuite_EF29
        make -j $(nproc) fate SAMPLES=/root/fate-suite
        ;;
    EF30)
        cd /root/build_testsuite_EF30
        make -j $(nproc) fate SAMPLES=/root/fate-suite
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
