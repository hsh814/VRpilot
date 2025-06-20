#!/bin/bash
cd /dataset/repos/coreutils
./bootstrap
mkdir -p /root/build_testsuite
cd /root/build_testsuite
FORCE_UNSAFE_CONFIGURE=1 /dataset/repos/coreutils/configure
make -j 32

case "$1" in
    EF23)
        ;;
    EF24)
        ;;
    EF25)
        ;;
    EF26)
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) SUBDIRS=. check
