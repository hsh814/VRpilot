#!/bin/bash

cd /dataset/repos/libarchive
autoreconf -i

mkdir -p /root/build
cd /root/build
ASAN_OPTIONS=detect_leaks=0 CFLAGS="-fsanitize=address -fsanitize=signed-integer-overflow -g" LDFLAGS="-fsanitize=address -fsanitize=signed-integer-overflow -g" /dataset/repos/libarchive/configure --without-openssl
make -j 32