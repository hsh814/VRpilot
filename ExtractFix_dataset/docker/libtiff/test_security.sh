#!/bin/bash

/scripts/test_build.sh $1
cd /root/build
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    bugzilla_2633)
        tools/tiff2ps /dataset/bugzilla_2633/00107-libtiff-heapoverflow-PSDataColorContig
        ;;
    cve_2014_8128)
        tools/thumbnail /dataset/cve_2014_8128/03_thumbnail.tiff out.tiff
        ;;
    cve_2016_10094)
        tools/tiff2pdf /dataset/cve_2016_10094/00112-libtiff-heapoverflow-_TIFFmemcpy -o foo
        ;;
    cve_2016_3186)
        tools/gif2tiff /dataset/cve_2016_3186/exploit.gif tmp.tif
        ;;
    cve_2016_3623)
        tools/rgb2ycbcr -c zip -r 0 -h 2 -v 0 /dataset/cve_2016_3623/autumn.tif 1.tif
        ;;
    cve_2016_5314)
        tools/rgb2ycbcr /dataset/cve_2016_5314/CVE-2016-5314.tif tmp.tif
        ;;
    cve_2016_5321)
        tools/tiffcrop /dataset/cve_2016_5321/EF01.tif tmp.tif
        ;;
    cve_2016_9532)
        tools/tiffcrop /dataset/cve_2016_9532/exploit tmp.tif
        ;;
    cve_2017_7595)
        tools/tiffcp -i /dataset/cve_2017_7595/00123-libtiff-fpe-JPEGSetupEncode /tmp/foo
        ;;
    cve_2017_7601)
        tools/tiffcp -i /dataset/cve_2017_7601/00119-libtiff-shift-long-tif_jpeg /tmp/foo
        ;;
    EF11)
        tools/tiffmedian /dataset/EF11/00083-libtiff-fpe-OJPEGDecodeRaw /tmp/foo
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
