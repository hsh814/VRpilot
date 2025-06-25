FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake clang-8 libfuzzer-8-dev
RUN apt-get -y build-dep ffmpeg

RUN mkdir -p /dataset/repos
COPY testcases /dataset
# COPY repos/FFmpeg /dataset/repos/FFmpeg_cve_2017_9992
# COPY repos/FFmpeg /dataset/repos/FFmpeg_bugzilla_1404
# COPY testcases/cve_2017_9992 /dataset/cve_2017_9992
# COPY testcases/bugzilla_1404 /dataset/bugzilla_1404

# WORKDIR /root
# RUN mkdir build_cve_2017_9992 build_bugzilla_1404 build_testsuite_cve_2017_9992 build_testsuite_bugzilla_1404

# WORKDIR /dataset/repos/FFmpeg_cve_2017_9992
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2017_9992
# WORKDIR /root/build_cve_2017_9992
# RUN /dataset/repos/FFmpeg_cve_2017_9992/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
# RUN make -j $(nproc)
# RUN mkdir tools
# RUN make tools/target_dec_dfa_fuzzer
# WORKDIR /root/build_testsuite_cve_2017_9992
# RUN /dataset/repos/FFmpeg_cve_2017_9992/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/FFmpeg_bugzilla_1404
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout bugzilla_1404
# WORKDIR /root/build_bugzilla_1404
# RUN /dataset/repos/FFmpeg_bugzilla_1404/configure --cc=clang-8 --cxx=clang++-8 --ld="clang++-8 -std=c++11" --enable-ossfuzz --optflags=-O1 --enable-gpl --enable-libass --enable-libfreetype --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-nonfree --disable-muxers --disable-protocols --disable-demuxer=rtp,rtsp,sdp --disable-devices --disable-shared --libfuzzer=/usr/lib/llvm-8/lib/libFuzzer.a
# RUN make -j $(nproc)
# RUN mkdir tools
# RUN make tools/target_dec_cavs_fuzzer
# WORKDIR /root/build_testsuite_bugzilla_1404
# RUN /dataset/repos/FFmpeg_bugzilla_1404/configure
# RUN make -j $(nproc)

# WORKDIR /root/build_cve_2017_9992
# RUN make fate-rsync SAMPLES=/root/fate-suite

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
