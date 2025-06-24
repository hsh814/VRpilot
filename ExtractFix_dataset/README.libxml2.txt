Bugs: cve_2016_1838, EF16, cve_2012_5134, cve_2017_5969

Build:

mkdir build ; cd build
( cd /dataset/repos/libxml2/ ; git clean -fdx ; git reset --hard ; git checkout EFXX )
/dataset/repos/libxml2/autogen.sh CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
make -j $(nproc)

Test:

The test suite fails when ASAN is enabled. So build it without ASAN.

mkdir build_dir_noasan && cd build_dir_noasan
/dataset/repos/libxml2/autogen.sh
make -j $(nproc)
make check

How well each patch matches our repair system:

========== cve_2016_1838 =========
 *  parser.c: 6 lines added, 2 lines removed, spans 12 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/libxml2/error.c:192 xmlParserPrintFileContextInternal
ASAN report: 1/1 source files match, 0/2 hunks match
========== EF16 =========
 *  HTMLparser.c: 8 lines added, 0 lines removed, spans 46 lines
    runtest.c: 2 lines added, 2 lines removed, spans 18 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 __asan_memcpy
ASAN report: 1/2 source files match, 4/4 hunks match
========== cve_2012_5134 =========
 *  parser.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/libxml2/parser.c:4079 xmlParseAttValueComplex
ASAN report: 1/1 source files match, 1/1 hunks match
========== cve_2017_5969 =========
 *  valid.c: 14 lines added, 10 lines removed, spans 13 lines
SUMMARY: AddressSanitizer: SEGV /dataset/repos/libxml2/valid.c:1181 xmlDumpElementContent
ASAN report: 1/1 source files match, 1/1 hunks match
