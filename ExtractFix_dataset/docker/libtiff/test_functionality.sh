#!/bin/bash

case "$1" in
    EF01|EF04|EF06|EF07|EF08|EF09|EF10|EF11)
        cd /root/build_"$1"
        make -j $(nproc) test
        ;;
    EF02_*)
        cd /root/build_"$1"
        make -j $(nproc) check
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
