#!/bin/bash

if [ ! -f /dataset/repos/zziplib/docs/zziplib-manpages.tar ]; then
  cd /dataset/repos/zziplib/docs
  wget https://github.com/LuaDist/libzzip/raw/master/docs/zziplib-manpages.tar
fi
mkdir -p /root/build_testsuite
cd /root/build_testsuite
/dataset/repos/zziplib/configure
make -j 32
exit 0
case "$1" in
    *)
        ;;
esac
