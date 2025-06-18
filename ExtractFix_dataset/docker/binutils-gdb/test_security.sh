#!/bin/bash

case "$1" in
    EF12)
        cd /root/build_EF12
        ./binutils/readelf -w /dataset/EF12/bug3
        ;;
    EF13)
        cd /root/build_EF13
        ./binutils/nm-new -A -a -l -S -s --special-syms --synthetic --with-symbol-versions -D /dataset/EF13/3899.crashes.bin
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
