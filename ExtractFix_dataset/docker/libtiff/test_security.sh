#!/bin/bash

/scripts/test_build.sh $1
cd /root/build

case "$1" in
    cve_2016_5321)
        tools/tiffcrop /dataset/cve_2016_5321/cve_2016_5321.tif tmp.tif
        ;;
    EF04)
        tools/rgb2ycbcr /dataset/EF04/CVE-2016-5314.tif tmp.tif
        ;;
    EF06)
        tools/tiff2ps /dataset/EF06/00107-libtiff-heapoverflow-PSDataColorContig
        ;;
    cve_2016_10094)
        tools/tiff2pdf /dataset/cve_2016_10094/00112-libtiff-heapoverflow-_TIFFmemcpy -o foo
        ;;
    cve_2017_7601)
        tools/tiffcp -i /dataset/cve_2017_7601/00119-libtiff-shift-long-tif_jpeg /tmp/foo
        ;;
    cve_2016_3623)
        tools/rgb2ycbcr -c zip -r 0 -h 2 -v 0 /dataset/cve_2016_3623/autumn.tif 1.tif
        ;;
    cve_2017_7595)
        tools/tiffcp -i /dataset/cve_2017_7595/00123-libtiff-fpe-JPEGSetupEncode /tmp/foo
        ;;
    EF11)
        tools/tiffmedian /dataset/EF11/00083-libtiff-fpe-OJPEGDecodeRaw /tmp/foo
        ;;
    cve_2014_8128)
        tools/thumbnail /dataset/cve_2014_8128/03_thumbnail.tiff out.tiff
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
