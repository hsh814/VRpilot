#!/bin/bash

case "$1" in
    EF23)
        cd /home/extractfix/build_testsuite_EF23
        ;;
    EF24)
        cd /home/extractfix/build_testsuite_EF24
        ;;
    EF25)
        cd /home/extractfix/build_testsuite_EF25
        ;;
    EF26)
        cd /home/extractfix/build_testsuite_EF26
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) SUBDIRS=. check
