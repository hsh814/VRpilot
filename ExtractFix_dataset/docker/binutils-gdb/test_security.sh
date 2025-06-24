#!/bin/bash
/scripts/test_build.sh $1
cd /root/build
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    cve_2017_14745)
        ./binutils/objdump -D /dataset/cve_2017_14745/exploit
        ;;
    cve_2017_6965)
        ./binutils/readelf -w /dataset/cve_2017_6965/exploit
        ;;
    cve_2018_10372)
        ./binutils/readelf -w /dataset/cve_2018_10372/bug3
        ;;
    cve_2017_15025)
        ./binutils/nm-new -A -a -l -S -s --special-syms --synthetic --with-symbol-versions -D /dataset/cve_2017_15025/3899.crashes.bin
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
