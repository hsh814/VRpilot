#!/bin/bash

/scripts/test_build.sh $1
cd /root/build
export ASAN_OPTIONS=detect_leaks=0
case "$1" in
    cve_2016_1834)
        gcc -g -fsanitize=address -I/dataset/repos/libxml2/include -I${PWD}/include -L${PWD}/.libs -lxml2 /dataset/cve_2016_1834/poc.c -o poc ${PWD}/.libs/libxml2.a -lz -llzma -lm -ldl
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
