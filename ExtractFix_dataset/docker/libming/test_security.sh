#!/bin/bash
/scripts/test_build.sh $1
cd /root/build
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    cve_2016_9264)
        ./util/listmp3 /dataset/cve_2016_9264/exploit
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
