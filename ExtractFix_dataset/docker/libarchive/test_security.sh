#!/bin/bash

/scripts/test_build.sh $1
cd /root/build
case "$1" in
    cve_2016_5844)
        ./bsdtar -tf /dataset/cve_2016_5844/libarchive-signed-int-overflow.iso
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
