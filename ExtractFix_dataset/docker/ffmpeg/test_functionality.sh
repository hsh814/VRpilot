#!/bin/bash
mkdir -p /root/build_testsuite
cd /root/build_testsuite

/dataset/repos/ffmpeg/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
make -j 32
mkdir tools
make tools/target_dec_dfa_fuzzer

case "$1" in
    cve_2017_9992)
        make -j $(nproc) fate SAMPLES=/root/fate-suite
        ;;
    bugzilla_1404)
        make -j $(nproc) fate SAMPLES=/root/fate-suite
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
