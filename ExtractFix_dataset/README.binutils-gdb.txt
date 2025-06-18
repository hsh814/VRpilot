Bugs: EF12, EF13

Build:

EF12:

mkdir build ; cd build
( cd /dataset/repos/binutils-gdb/ ; git clean -fdx ; git reset --hard ; git checkout EF12 )
/dataset/repos/binutils-gdb/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j $(nproc)

EF13:

mkdir build ; cd build
( cd /dataset/repos/binutils-gdb/ ; git clean -fdx ; git reset --hard ; git checkout EF13 )
/dataset/repos/binutils-gdb/configure CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined"
make -j $(nproc)

Test:

Test suite fails with ASAN, so we need to build without it:

mkdir build_noasan ; cd build_noasan
/dataset/repos/binutils-gdb/configure
make -j $(nproc)
make -C binutils check

How well each patch matches our repair system:

========== EF12 =========
 *  binutils/dwarf.c: 12 lines added, 1 lines removed, spans 11 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /dataset/repos/binutils-gdb/binutils/dwarf.c:9290 process_cu_tu_index
ASAN report: 1/1 source files match, 1/1 hunks match
========== EF13 =========
    bfd/dwarf2.c: 2 lines added, 0 lines removed, spans 1 lines
SUMMARY: runtime error: shift exponent 70 is too large for 64-bit type 'long unsigned int' in bfd/libbfd.c:1023
UBSAN report: 0/1 source files match, 0/1 hunks match
 *  bfd/dwarf2.c: 2 lines added, 0 lines removed, spans 1 lines
SUMMARY: runtime error: division by zero in bfd/dwarf2.c:2442
UBSAN report: 1/1 source files match, 1/1 hunks match
