#!/bin/bash
cd /dataset/repos/coreutils
./bootstrap

mkdir -p /root/build
cd /root/build
FORCE_UNSAFE_CONFIGURE=1 /dataset/repos/coreutils/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 32