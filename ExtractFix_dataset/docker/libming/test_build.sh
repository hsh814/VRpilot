#!/bin/bash

cd /dataset/repos/libming
./autogen.sh

mkdir -p /root/build
cd /root/build
/dataset/repos/libming/configure CFLAGS="-static -g -fsanitize=address" LDFLAGS="-static -g -fsanitize=address"
make -j 1 # Use single process to prevent race condition
