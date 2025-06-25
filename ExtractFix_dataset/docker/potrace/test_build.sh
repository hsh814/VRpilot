#!/bin/bash

mkdir -p /root/build
cd /root/build

/dataset/repos/potrace/configure CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
make -j 32
