FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential git vim unzip python-dev python-pip ipython zip libtool bison texinfo flex
RUN apt-get -y build-dep binutils

RUN mkdir -p /dataset/repos
COPY testcases /dataset

# COPY repos/binutils-gdb /dataset/repos/binutils-gdb_cve_2018_10372
# COPY repos/binutils-gdb /dataset/repos/binutils-gdb_cve_2017_15025


# WORKDIR /root
# RUN mkdir build_cve_2018_10372 build_cve_2017_15025 build_testsuite_cve_2018_10372 build_testsuite_cve_2017_15025

# WORKDIR /dataset/repos/binutils-gdb_cve_2018_10372
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2018_10372
# WORKDIR /root/build_cve_2018_10372
# RUN /dataset/repos/binutils-gdb_cve_2018_10372/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2018_10372 
# RUN /dataset/repos/binutils-gdb_cve_2018_10372/configure
# RUN make -j $(nproc)
# RUN make -C bfd check
# RUN make -C binutils check

# WORKDIR /dataset/repos/binutils-gdb_cve_2017_15025
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2017_15025
# WORKDIR /root/build_cve_2017_15025
# RUN /dataset/repos/binutils-gdb_cve_2017_15025/configure CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2017_15025 
# RUN /dataset/repos/binutils-gdb_cve_2017_15025/configure
# RUN make -j $(nproc)
# RUN make -C bfd check
# RUN make -C binutils check

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
