Bugs: gnubug_26545, gnubug_25003, gnubug_25023, gnubug_19784

Build:

mkdir build ; cd build
( cd /dataset/repos/coreutils/ ; git checkout gnubug_25003 ; git clean -xffd && git submodule foreach --recursive git clean -xffd ; git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive )
( cd /dataset/repos/coreutils/ ; ./bootstrap )
/dataset/repos/coreutils/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j $(nproc)

Test:

One of the tests fails in docker, so disable it:
sed -i '/print_ver_/a skip_ "does not work in docker"' /dataset/repos/coreutils/tests/tail-2/inotify-dir-recreate.sh

make -j $(nproc) check

How well each patch matches our repair system:

========== gnubug_26545 =========
 *  src/shred.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: memcpy-param-overlap ??:0 __asan_memcpy
ASAN report: 1/1 source files match, 1/1 hunks match
========== gnubug_25003 =========
 *  src/split.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: negative-size-param ??:0 __asan_memmove
ASAN report: 1/1 source files match, 1/1 hunks match
========== gnubug_25023 =========
 *  src/pr.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: global-buffer-overflow /dataset/repos/coreutils/src/pr.c:2241 print_sep_string
ASAN report: 1/1 source files match, 0/1 hunks match
========== gnubug_19784 =========
 *  src/make-prime-list.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/coreutils/src/make-prime-list.c:214 main
ASAN report: 1/1 source files match, 1/1 hunks match

