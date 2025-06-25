#!/bin/bash
cd /dataset/repos/coreutils
./bootstrap
mkdir -p /root/build_testsuite
cd /root/build_testsuite
FORCE_UNSAFE_CONFIGURE=1 CFLAGS="-Wno-error" /dataset/repos/coreutils/configure
make -j 32

case "$1" in
    gnubug_26545)
        ;;
    gnubug_25003)
        ;;
    gnubug_25023)
        ;;
    gnubug_19784)
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

make -j $(nproc) SUBDIRS=. check
