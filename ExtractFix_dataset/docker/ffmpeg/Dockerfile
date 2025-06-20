FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake clang-8 libfuzzer-8-dev
RUN apt-get -y build-dep ffmpeg

RUN mkdir -p /dataset/repos
COPY repos/FFmpeg /dataset/repos/FFmpeg_EF29
COPY repos/FFmpeg /dataset/repos/FFmpeg_EF30
COPY testcases/EF29 /dataset/EF29
COPY testcases/EF30 /dataset/EF30

WORKDIR /root
RUN mkdir build_EF29 build_EF30 build_testsuite_EF29 build_testsuite_EF30

WORKDIR /dataset/repos/FFmpeg_EF29
RUN git clean -fdx
RUN git reset --hard
RUN git checkout EF29
WORKDIR /root/build_EF29
RUN /dataset/repos/FFmpeg_EF29/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
RUN make -j $(nproc)
RUN mkdir tools
RUN make tools/target_dec_dfa_fuzzer
WORKDIR /root/build_testsuite_EF29
RUN /dataset/repos/FFmpeg_EF29/configure
RUN make -j $(nproc)

WORKDIR /dataset/repos/FFmpeg_EF30
RUN git clean -fdx
RUN git reset --hard
RUN git checkout EF30
WORKDIR /root/build_EF30
RUN /dataset/repos/FFmpeg_EF30/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
RUN make -j $(nproc)
RUN mkdir tools
RUN make tools/target_dec_cavs_fuzzer
WORKDIR /root/build_testsuite_EF30
RUN /dataset/repos/FFmpeg_EF30/configure
RUN make -j $(nproc)

WORKDIR /root/build_EF29
RUN make fate-rsync SAMPLES=/root/fate-suite

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
