FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libtiff5

RUN mkdir -p /dataset/repos
COPY testcases /dataset
# COPY repos/libtiff /dataset/repos/libtiff_cve_2016_5321
# COPY repos/libtiff /dataset/repos/libtiff_cve_2014_8128
# COPY repos/libtiff /dataset/repos/libtiff_EF02_02
# COPY repos/libtiff /dataset/repos/libtiff_EF02_03
# COPY repos/libtiff /dataset/repos/libtiff_EF02_04
# COPY repos/libtiff /dataset/repos/libtiff_EF02_05
# COPY repos/libtiff /dataset/repos/libtiff_EF04
# COPY repos/libtiff /dataset/repos/libtiff_EF06
# COPY repos/libtiff /dataset/repos/libtiff_cve_2016_10094
# COPY repos/libtiff /dataset/repos/libtiff_cve_2017_7601
# COPY repos/libtiff /dataset/repos/libtiff_cve_2016_3623
# COPY repos/libtiff /dataset/repos/libtiff_cve_2017_7595
# COPY repos/libtiff /dataset/repos/libtiff_EF11
# COPY testcases/cve_2016_5321 /dataset/cve_2016_5321
# COPY testcases/cve_2014_8128 /dataset/cve_2014_8128
# COPY testcases/EF02_02 /dataset/EF02_02
# COPY testcases/EF02_03 /dataset/EF02_03
# COPY testcases/EF02_04 /dataset/EF02_04
# COPY testcases/EF02_05 /dataset/EF02_05
# COPY testcases/EF04 /dataset/EF04
# COPY testcases/EF06 /dataset/EF06
# COPY testcases/cve_2016_10094 /dataset/cve_2016_10094
# COPY testcases/cve_2017_7601 /dataset/cve_2017_7601
# COPY testcases/cve_2016_3623 /dataset/cve_2016_3623
# COPY testcases/cve_2017_7595 /dataset/cve_2017_7595
# COPY testcases/EF11 /dataset/EF11

# WORKDIR /root
# RUN mkdir build_cve_2016_5321 build_cve_2014_8128 build_EF02_02 build_EF02_03 build_EF02_04 build_EF02_05 \
#           build_EF04 build_EF06 build_cve_2016_10094 build_cve_2017_7601 build_cve_2016_3623 build_cve_2017_7595 build_EF11

# # cve_2016_5321, EF04, EF06, cve_2016_10094 use ASAN
# WORKDIR /dataset/repos/libtiff_cve_2016_5321
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_5321
# WORKDIR /root/build_cve_2016_5321
# RUN CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff_cve_2016_5321
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

# WORKDIR /dataset/repos/libtiff_cve_2016_10094
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_10094
# WORKDIR /root/build_cve_2016_10094
# RUN CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address" cmake /dataset/repos/libtiff_cve_2016_10094
# RUN make -j $(nproc)

# # cve_2017_7601-EF11 use UBSAN
# WORKDIR /dataset/repos/libtiff_cve_2017_7601
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2017_7601
# WORKDIR /root/build_cve_2017_7601
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_cve_2017_7601
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_cve_2016_3623
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_3623
# WORKDIR /root/build_cve_2016_3623
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_cve_2016_3623
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_cve_2017_7595
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2017_7595
# WORKDIR /root/build_cve_2017_7595
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_cve_2017_7595
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libtiff_EF11
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF11
# WORKDIR /root/build_EF11
# RUN CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined" cmake /dataset/repos/libtiff_EF11
# RUN make -j $(nproc)

# # EF02_* use ./configure and ASAN
# WORKDIR /dataset/repos/libtiff_cve_2014_8128
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2014_8128
# WORKDIR /root/build_cve_2014_8128
# RUN /dataset/repos/libtiff_cve_2014_8128/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
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
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
