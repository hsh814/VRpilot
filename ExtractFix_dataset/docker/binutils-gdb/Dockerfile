FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep binutils

RUN mkdir -p /dataset/repos
COPY repos/binutils-gdb /dataset/repos/binutils-gdb_EF12
COPY repos/binutils-gdb /dataset/repos/binutils-gdb_EF13
COPY testcases/EF12 /dataset/EF12
COPY testcases/EF13 /dataset/EF13

WORKDIR /root
RUN mkdir build_EF12 build_EF13 build_testsuite_EF12 build_testsuite_EF13

WORKDIR /dataset/repos/binutils-gdb_EF12
RUN git clean -fdx
RUN git reset --hard
RUN git checkout EF12
WORKDIR /root/build_EF12
RUN /dataset/repos/binutils-gdb_EF12/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
RUN make -j $(nproc)
WORKDIR /root/build_testsuite_EF12 
RUN /dataset/repos/binutils-gdb_EF12/configure
RUN make -j $(nproc)
RUN make -C bfd check
RUN make -C binutils check

WORKDIR /dataset/repos/binutils-gdb_EF13
RUN git clean -fdx
RUN git reset --hard
RUN git checkout EF13
WORKDIR /root/build_EF13
RUN /dataset/repos/binutils-gdb_EF13/configure CFLAGS="-g -fsanitize=undefined" LDFLAGS="-g -fsanitize=undefined"
RUN make -j $(nproc)
WORKDIR /root/build_testsuite_EF13 
RUN /dataset/repos/binutils-gdb_EF13/configure
RUN make -j $(nproc)
RUN make -C bfd check
RUN make -C binutils check

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
