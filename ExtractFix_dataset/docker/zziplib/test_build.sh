#!/bin/bash

mkdir -p /root/build
cd /root/build
/dataset/repos/zziplib/configure CFLAGS="-static -g -fsanitize=address" LDFLAGS="-static -g -fsanitize=address"
make -j 32

