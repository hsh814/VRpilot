#!/bin/bash

cd /dataset/repos/libming
./autogen.sh

mkdir -p /root/build
cd /root/build
export ASAN_OPTIONS=detect_leaks=0
/dataset/repos/libming/configure --disable-freetype CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 1 # Use single process to prevent race condition
