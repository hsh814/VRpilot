#!/bin/bash

mkdir -p /root/build
cd /root/build

/dataset/repos/ffmpeg/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
make -j 32
mkdir tools

case "$1" in
    cve_2017_9992)
        make tools/target_dec_dfa_fuzzer
        ;;
    bugzilla_1404)
        make tools/target_dec_cavs_fuzzer
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac

