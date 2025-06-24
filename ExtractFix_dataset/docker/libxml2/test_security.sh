#!/bin/bash

/scripts/test_build.sh $1
cd /root/build
case "$1" in
    cve_2016_1838)
        ./xmllint /dataset/cve_2016_1838/attachment_316157.xml
        ;;
    EF16)
        ./xmllint --html /dataset/EF16/attachment_316182.xml
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
