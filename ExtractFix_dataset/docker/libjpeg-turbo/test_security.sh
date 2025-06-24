#!/bin/bash

/scripts/test_build.sh $1
cd /dataset/repos/libjpeg-turbo
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    EF19)
        ./cjpeg -outfile /dev/null /dataset/EF19/hbo_rdbmp.c:209_1.bmp
        ;;
    cve_2018_19664)
        ./djpeg -colors 256 -bmp /dataset/cve_2018_19664/49065782-f0ebfd00-f216-11e8-9e9b-a86f3d5ea58a.jpg
        ;;
    cve_2017_15232)
        ./djpeg -crop "1x1+16+16" -onepass -dither ordered -dct float -colors 8 -targa -grayscale -outfile o /dataset/cve_2017_15232/001-mozjpeg-quantize_ord_dither-536.crash
        ;;
    cve_2012_2806)
        ./djpeg /dataset/cve_2012_2806/cnode0006-heap-buffer-overflow-796.jpg
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
