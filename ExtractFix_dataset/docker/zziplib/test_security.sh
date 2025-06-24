#!/bin/bash

/scripts/test_build.sh $1
cd /root/build
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    cve_2017_5974|cve_2017_5975|cve_2017_5976)
        ./bins/unzzipcat-mem /dataset/$1/exploit
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
