#!/bin/bash

case "$1" in
    EF15|EF16|EF17|EF18)
        cd /root/build_testsuite_"$1"
        make check
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
