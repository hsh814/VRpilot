Bugs: cve_2016_8691, cve_2016_9387

Build:

cve_2016_8691:

Has to be built in-tree.

cd /dataset/repos/jasper/ ; git clean -fdx ; git reset --hard ; git checkout cve_2016_8691
# Using inline causes a linker error, so just remove it
sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
autoreconf -i
./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
make -j $(nproc)

cve_2016_9387:

cd /dataset/repos/jasper/ ; git clean -fdx ; git reset --hard ; git checkout cve_2016_9387
# Using inline causes a linker error, so just remove it
sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
autoreconf -i
./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
make -j $(nproc)

Test:

No test suite! :(

Maybe a workaround:

for f in data/images/*.mif data/images/*.jpg data/images/*.pnm ; do src/appl/imginfo -f $f >/dev/null && echo PASS $f || echo FAIL $f ; done

How well each patch matches our repair system:

========== cve_2016_8691 =========
    jpc_cs.c: 10 lines added, 0 lines removed, spans 9 lines
SUMMARY: runtime error: division by zero in jpc_dec.c:1196
UBSAN report: 0/1 source files match, 0/1 hunks match
    jpc_cs.c: 10 lines added, 0 lines removed, spans 9 lines
SUMMARY: runtime error: division by zero in jpc_dec.c:1197
UBSAN report: 0/1 source files match, 0/1 hunks match
========== cve_2016_9387 =========
 *  jpc_dec.c: 5 lines added, 1 lines removed, spans 39 lines
SUMMARY: runtime error: signed integer overflow: 210 * -2147483646 cannot be represented in type 'int' in jpc_dec.c:1234
UBSAN report: 1/1 source files match, 1/2 hunks match
