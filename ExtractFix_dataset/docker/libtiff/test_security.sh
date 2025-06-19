#!/bin/bash

cd /root/build

case "$1" in
    EF01|EF04|EF06|EF07)
        CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    EF08|EF09|EF10|EF11)
        CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff
        make -j 32
        ;;
    EF02_*)
        /dataset/repos/libtiff/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
        make -j 32
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac

case "$1" in
    EF01)
        tools/tiffcrop /dataset/EF01/EF01.tif tmp.tif
        ;;
    EF04)
        tools/rgb2ycbcr /dataset/EF04/CVE-2016-5314.tif tmp.tif
        ;;
    EF06)
        tools/tiff2ps /dataset/EF06/00107-libtiff-heapoverflow-PSDataColorContig
        ;;
    EF07)
        tools/tiff2pdf /dataset/EF07/00112-libtiff-heapoverflow-_TIFFmemcpy -o foo
        ;;
    EF08)
        tools/tiffcp -i /dataset/EF08/00119-libtiff-shift-long-tif_jpeg /tmp/foo
        ;;
    EF09)
        tools/rgb2ycbcr -c zip -r 0 -h 2 -v 0 /dataset/EF09/autumn.tif 1.tif
        ;;
    EF10)
        tools/tiffcp -i /dataset/EF10/00123-libtiff-fpe-JPEGSetupEncode /tmp/foo
        ;;
    EF11)
        tools/tiffmedian /dataset/EF11/00083-libtiff-fpe-OJPEGDecodeRaw /tmp/foo
        ;;
    EF02_01)
        tools/thumbnail /dataset/EF02_01/03_thumbnail.tiff out.tiff
        ;;
    EF02_02)
        tools/tiff2pdf /dataset/EF02_02/05_tiff2pdf.tiff
        ;;
    EF02_03)
        tools/thumbnail /dataset/EF02_03/02_thumbnail.tiff out.tiff
        ;;
    EF02_04)
        tools/thumbnail /dataset/EF02_04/17_thumbnail.tiff out.tiff
        ;;
    EF02_05)
        tools/tiffdither /dataset/EF02_05/20_tiffdither.tiff out.tiff
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
