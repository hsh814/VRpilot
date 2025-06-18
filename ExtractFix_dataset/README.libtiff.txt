Bugs: EF01, EF02_01, EF02_02, EF02_03, EF02_04, EF04, EF06, EF07, EF08, EF09, EF10, EF11


Note: EF02 is a single CVE but actually 5 separate bugs, so was split into EF02_{01..05}

Build:

EF01, EF04, EF06, EF07:

mkdir build ; cd build
( cd /dataset/repos/libtiff/ ; git clean -fdx ; git reset --hard ; git checkout EFXX )
CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff
make -j $(nproc)

EF08, EF09, EF10, EF11:

mkdir build ; cd build
( cd /dataset/repos/libtiff/ ; git clean -fdx ; git reset --hard ; git checkout EFXX )
CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff
make -j $(nproc)

EF02_01, EF02_02, EF02_03, EF02_04:

mkdir build ; cd build
( cd /dataset/repos/libtiff/ ; git clean -fdx ; git reset --hard ; git checkout EF02_XX )
/dataset/repos/libtiff/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j $(nproc)

Test:

EF01, EF04, EF06-EF11:

make test

EF02:

make check

How well each patch matches our repair system:

========== EF01 =========
 *  tools/tiffcrop.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: stack-buffer-overflow /dataset/repos/libtiff/tools/tiffcrop.c:994 readSeparateTilesIntoBuffer
ASAN report: 1/1 source files match, 1/1 hunks match
========== EF02_01 =========
 *  tools/thumbnail.c: 7 lines added, 1 lines removed, spans 6 lines
SUMMARY: AddressSanitizer: stack-buffer-overflow /dataset/repos/libtiff/tools/thumbnail.c:552 setImage1
ASAN report: 1/1 source files match, 0/1 hunks match
========== EF02_02 =========
 *  libtiff/tif_next.c: 17 lines added, 0 lines removed, spans 16 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/libtiff/libtiff/tif_next.c:124 NeXTDecode
ASAN report: 1/1 source files match, 0/1 hunks match
========== EF02_03 =========
 *  tools/thumbnail.c: 20 lines added, 1 lines removed, spans 19 lines
    tools/tiffcmp.c: 15 lines added, 2 lines removed, spans 29 lines
SUMMARY: AddressSanitizer: SEGV /dataset/repos/libtiff/libtiff/tif_dir.c:1056 _TIFFVGetField
ASAN report: 1/2 source files match, 1/3 hunks match
========== EF02_04 =========
    libtiff/tif_dir.h: 1 lines added, 0 lines removed, spans 0 lines
    libtiff/tif_dirinfo.c: 103 lines added, 0 lines removed, spans 102 lines
    libtiff/tif_dirread.c: 4 lines added, 0 lines removed, spans 3 lines
SUMMARY: AddressSanitizer: SEGV /dataset/repos/libtiff/libtiff/tif_dir.c:1056 _TIFFVGetField
ASAN report: 0/3 source files match, 0/3 hunks match
========== EF06 =========
 *  tools/tiff2ps.c: 6 lines added, 1 lines removed, spans 252 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/libtiff/tools/tiff2ps.c:2470 PSDataColorContig
ASAN report: 1/1 source files match, 2/2 hunks match
========== EF07 =========
 *  tools/tiff2pdf.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 __asan_memcpy
ASAN report: 1/1 source files match, 1/1 hunks match
========== EF08 =========
 *  libtiff/tif_jpeg.c: 7 lines added, 0 lines removed, spans 6 lines
SUMMARY: runtime error: shift exponent 136 is too large for 64-bit type 'long int' in libtiff/tif_jpeg.c:1646
ASAN report: 1/1 source files match, 1/1 hunks match
========== EF09 =========
 *  tools/rgb2ycbcr.c: 4 lines added, 0 lines removed, spans 3 lines
SUMMARY: runtime error: division by zero in tools/rgb2ycbcr.c:257
ASAN report: 1/1 source files match, 0/1 hunks match
========== EF10 =========
 *  libtiff/tif_jpeg.c: 7 lines added, 0 lines removed, spans 6 lines
SUMMARY: runtime error: division by zero in libtiff/tif_jpeg.c:1687
ASAN report: 1/1 source files match, 0/1 hunks match
========== EF11 =========
 *  libtiff/tif_ojpeg.c: 8 lines added, 0 lines removed, spans 545 lines
SUMMARY: runtime error: division by zero in libtiff/tif_ojpeg.c:816
ASAN report: 1/1 source files match, 0/3 hunks match
