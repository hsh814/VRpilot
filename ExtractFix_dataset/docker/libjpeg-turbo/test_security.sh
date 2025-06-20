#!/bin/bash

/scripts/test_build.sh $1
cd /root/build

case "$1" in
    EF19)
        ./cjpeg -outfile /dev/null /dataset/EF19/hbo_rdbmp.c:209_1.bmp
        ;;
    EF20)
        ./djpeg -colors 256 -bmp /dataset/EF20/49065782-f0ebfd00-f216-11e8-9e9b-a86f3d5ea58a.jpg
        ;;
    EF21)
        ./djpeg -crop "1x1+16+16" -onepass -dither ordered -dct float -colors 8 -targa -grayscale -outfile o /dataset/EF21/001-mozjpeg-quantize_ord_dither-536.crash
        ;;
    EF22)
        ./djpeg /dataset/EF22/cnode0006-heap-buffer-overflow-796.jpg
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
