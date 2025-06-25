#!/bin/bash
cd /dataset/repos/coreutils
./bootstrap

mkdir -p /root/build
cd /root/build
export ASAN_OPTIONS=detect_leaks=0
FORCE_UNSAFE_CONFIGURE=1 /dataset/repos/coreutils/configure CFLAGS="-Wno-error -g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 32