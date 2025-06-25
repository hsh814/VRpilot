#!/bin/bash

mkdir -p /root/build
if [ ! -f /dataset/repos/zziplib/docs/zziplib-manpages.tar ]; then
  cd /dataset/repos/zziplib/docs
  wget https://github.com/LuaDist/libzzip/raw/master/docs/zziplib-manpages.tar
fi
  
cd /root/build
export ASAN_OPTIONS=detect_leaks=0
/dataset/repos/zziplib/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 32

