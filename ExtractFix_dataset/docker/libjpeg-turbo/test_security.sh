#!/bin/bash

case "$1" in
    EF19)
        cd /root/build_EF19
        ./cjpeg -outfile /dev/null /dataset/EF19/hbo_rdbmp.c:209_1.bmp
        ;;
    EF20)
        cd /root/build_EF20
        ./djpeg -colors 256 -bmp /dataset/EF20/49065782-f0ebfd00-f216-11e8-9e9b-a86f3d5ea58a.jpg
        ;;
    EF21)
        cd /root/build_EF21
        ./djpeg -crop "1x1+16+16" -onepass -dither ordered -dct float -colors 8 -targa -grayscale -outfile o /dataset/EF21/001-mozjpeg-quantize_ord_dither-536.crash
        ;;
    EF22)
        cd /root/build_EF22
        ./djpeg /dataset/EF22/cnode0006-heap-buffer-overflow-796.jpg
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
