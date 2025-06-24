#!/bin/bash

cd /dataset/repos/jasper
sed -i 's/inline bool/inline static bool/' src/libjasper/base/jas_malloc.c
autoreconf -i

./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
make -j 32
