FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libtiff5

RUN mkdir -p /dataset/repos
COPY testcases /dataset
# COPY repos/libtiff /dataset/repos/libtiff_EF01
# COPY repos/libtiff /dataset/repos/libtiff_EF02_01
# COPY repos/libtiff /dataset/repos/libtiff_EF02_02
# COPY repos/libtiff /dataset/repos/libtiff_EF02_03
# COPY repos/libtiff /dataset/repos/libtiff_EF02_04
# COPY repos/libtiff /dataset/repos/libtiff_EF02_05
# COPY repos/libtiff /dataset/repos/libtiff_EF04
# COPY repos/libtiff /dataset/repos/libtiff_EF06
# COPY repos/libtiff /dataset/repos/libtiff_EF07
# COPY repos/libtiff /dataset/repos/libtiff_EF08
# COPY repos/libtiff /dataset/repos/libtiff_EF09
# COPY repos/libtiff /dataset/repos/libtiff_EF10
# COPY repos/libtiff /dataset/repos/libtiff_EF11
# COPY testcases/EF01 /dataset/EF01
# COPY testcases/EF02_01 /dataset/EF02_01
# COPY testcases/EF02_02 /dataset/EF02_02
# COPY testcases/EF02_03 /dataset/EF02_03
# COPY testcases/EF02_04 /dataset/EF02_04
# COPY testcases/EF02_05 /dataset/EF02_05
# COPY testcases/EF04 /dataset/EF04
# COPY testcases/EF06 /dataset/EF06
# COPY testcases/EF07 /dataset/EF07
# COPY testcases/EF08 /dataset/EF08
# COPY testcases/EF09 /dataset/EF09
# COPY testcases/EF10 /dataset/EF10
# COPY testcases/EF11 /dataset/EF11

# WORKDIR /root
# RUN mkdir build_EF01 build_EF02_01 build_EF02_02 build_EF02_03 build_EF02_04 build_EF02_05 \
#           build_EF04 build_EF06 build_EF07 build_EF08 build_EF09 build_EF10 build_EF11

# # EF01, EF04, EF06, EF07 use ASAN
# WORKDIR /dataset/repos/libtiff_EF01
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF01
# WORKDIR /root/build_EF01
# RUN CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff_EF01
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF04
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF04
# WORKDIR /root/build_EF04
# RUN CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff_EF04
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF06
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF06
# WORKDIR /root/build_EF06
# RUN CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff_EF06
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF07
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF07
# WORKDIR /root/build_EF07
# RUN CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff_EF07
# RUN make -j $(nproc)

# # EF08-EF11 use UBSAN
# WORKDIR /dataset/repos/libtiff_EF08
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF08
# WORKDIR /root/build_EF08
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_EF08
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF09
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF09
# WORKDIR /root/build_EF09
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_EF09
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF10
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF10
# WORKDIR /root/build_EF10
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_EF10
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF11
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF11
# WORKDIR /root/build_EF11
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_EF11
# RUN make -j $(nproc)

# # EF02_* use ./configure and ASAN
# WORKDIR /dataset/repos/libtiff_EF02_01
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF02_01
# WORKDIR /root/build_EF02_01
# RUN /dataset/repos/libtiff_EF02_01/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF02_02
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF02_02
# WORKDIR /root/build_EF02_02
# RUN /dataset/repos/libtiff_EF02_02/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF02_03
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF02_03
# WORKDIR /root/build_EF02_03
# RUN /dataset/repos/libtiff_EF02_03/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF02_04
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF02_04
# WORKDIR /root/build_EF02_04
# RUN /dataset/repos/libtiff_EF02_04/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF02_05
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF02_05
# WORKDIR /root/build_EF02_05
# RUN /dataset/repos/libtiff_EF02_05/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)

RUN mkdir -p /root/build
RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
