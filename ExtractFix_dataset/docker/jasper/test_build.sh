#!/bin/bash

cd /dataset/repos/jasper
sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
autoreconf -i

mkdir -p /root/build
cd /root_build
/dataset/repos/jasper/configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
make -j 32
