#!/bin/bash

mkdir -p /root/build
cd /root/build
export ASAN_OPTIONS=detect_leaks=0
/dataset/repos/libxml2/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 32

