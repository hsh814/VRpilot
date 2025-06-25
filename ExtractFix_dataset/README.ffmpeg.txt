Bugs: cve_2017_9992, bugzilla_1404

Build:

mkdir build; cd build
( cd /dataset/repos/FFmpeg/ ; git clean -fdx ; git reset --hard ; git checkout EFXX )
/dataset/repos/FFmpeg/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
make -j $(nproc)
mkdir tools

cve_2017_9992:
make tools/target_dec_dfa_fuzzer

bugzilla_1404:
make tools/target_dec_cavs_fuzzer

Test:

Test suite does not run correctly with the oss-fuzz configuration above. So:

mkdir build_testsuite; cd build_testsuite
/dataset/repos/FFmpeg/configure
make -j $(nproc)
# Get the samples needed for the test suite. They're ~1.2GB
make fate-rsync SAMPLES=fate-samples/
# Run the tests
make -j $(nproc) fate SAMPLES=/root/fate-suite

How well each patch matches our repair system:

========== cve_2017_9992 ========== 
 *  libavcodec/dfa.c: 1 lines added, 1 lines removed, spans 0 lines
SUMMARY: AddressSanitizer: heap-buffer-overflow /root/src/libavcodec/dfa.c:184:45 in decode_dds1
ASAN report: 1/1 source files match, 1/1 hunks match
========== bugzilla_1404 ========== 
 *  libavcodec/cavsdec.c: 4 lines added, 0 lines removed, spans 3 lines
SUMMARY: runtime error: signed integer overflow: 25984 * 130560 cannot be represented in type 'int' in libavcodec/cavsdec.c:489
UBSAN report: 1/1 source files match, 0/1 hunks match
