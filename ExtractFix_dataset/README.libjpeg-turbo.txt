Bugs: EF19, cve_2018_19664, cve_2017_15232, cve_2012_2806

Build:

libjpeg switched build systems at some point, so some use autoconf and some use cmake.

EF19, cve_2012_2806:

mkdir build ; cd build
( cd /dataset/repos/libjpeg-turbo/ ; git clean -fdx ; git reset --hard ; git checkout EFXX )
( cd /dataset/repos/libjpeg-turbo ; autoreconf -fvi )
/dataset/repos/libjpeg-turbo/configure CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
make -j $(nproc)

cve_2018_19664, cve_2017_15232:

mkdir build ; cd build
( cd /dataset/repos/libjpeg-turbo/ ; git clean -fdx ; git reset --hard ; git checkout EFXX )
CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo/
make -j $(nproc)

Test:

make test

How well each patch matches our repair system:

========== EF19 =========
    cderror.h: 3 lines added, 2 lines removed, spans 73 lines
 *  rdbmp.c: 6 lines added, 1 lines removed, spans 398 lines
    rdppm.c: 6 lines added, 6 lines removed, spans 215 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/libjpeg-turbo/rdbmp.c:145 get_8bit_row
ASAN report: 1/3 source files match, 2/12 hunks match
========== cve_2018_19664 =========
 *  wrbmp.c: 3 lines added, 2 lines removed, spans 2 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/libjpeg-turbo/wrbmp.c:145 put_pixel_rows
ASAN report: 1/1 source files match, 0/1 hunks match
========== cve_2017_15232 =========
 *  jdpostct.c: 5 lines added, 0 lines removed, spans 4 lines
 *  jquant1.c: 4 lines added, 0 lines removed, spans 3 lines
SUMMARY: AddressSanitizer: SEGV ??:0 ??
ASAN report: 2/2 source files match, 2/2 hunks match
========== cve_2012_2806 =========
 *  jdmarker.c: 3 lines added, 2 lines removed, spans 2 lines
SUMMARY: AddressSanitizer: stack-buffer-overflow /dataset/repos/libjpeg-turbo/jdmarker.c:327 get_sos
ASAN report: 1/1 source files match, 1/1 hunks match
