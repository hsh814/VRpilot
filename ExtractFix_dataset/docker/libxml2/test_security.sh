#!/bin/bash

/scripts/test_build.sh $1
cd /root/build
case "$1" in
    cve_2016_1834)
        gcc -g -fsanitize=address -I/dataset/repos/libtiff/include -L/dataset/repos/libtiff/.libs -lxml2 /dataset/cve_2016_1834/poc.c -o poc /dataset/repos/libtiff/.libs/libxml2.a -lz -llzma -m -ldl
        ASAN_OPTIONS=detect_leaks=0 ./poc
        ;;
    cve_2016_1838)
        ./xmllint /dataset/cve_2016_1838/attachment_316157.xml
        ;;
    cve_2016_1839)
        ./xmllint --html /dataset/cve_2016_1839/attachment_316182.xml
        ;;
    cve_2012_5134)
        ./xmllint /dataset/cve_2012_5134/reproducer-4.xml
        ;;
    cve_2017_5969)
        ./xmllint --recover /dataset/cve_2017_5969/crash-libxml2-recover.xml
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
