FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libxml2

RUN mkdir -p /dataset/repos
# COPY repos/libxml2 /dataset/repos/libxml2_EF15
# COPY repos/libxml2 /dataset/repos/libxml2_EF16
# COPY repos/libxml2 /dataset/repos/libxml2_EF17
# COPY repos/libxml2 /dataset/repos/libxml2_EF18
# COPY testcases/EF15 /dataset/EF15
# COPY testcases/EF16 /dataset/EF16
# COPY testcases/EF17 /dataset/EF17
# COPY testcases/EF18 /dataset/EF18
COPY testcases /dataset

# WORKDIR /root
# RUN mkdir -p build_EF15 build_testsuite_EF15 build_EF16 build_testsuite_EF16 build_EF17 build_testsuite_EF17 build_EF18 build_testsuite_EF18

# WORKDIR /dataset/repos/libxml2_EF15
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF15
# WORKDIR /root/build_EF15
# RUN /dataset/repos/libxml2_EF15/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF15
# RUN /dataset/repos/libxml2_EF15/autogen.sh
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libxml2_EF16
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF16
# WORKDIR /root/build_EF16
# RUN /dataset/repos/libxml2_EF16/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF16
# RUN /dataset/repos/libxml2_EF16/autogen.sh
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libxml2_EF17
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF17
# WORKDIR /root/build_EF17
# RUN /dataset/repos/libxml2_EF17/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF17
# RUN /dataset/repos/libxml2_EF17/autogen.sh
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libxml2_EF18
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF18
# WORKDIR /root/build_EF18
# RUN /dataset/repos/libxml2_EF18/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF18
# RUN /dataset/repos/libxml2_EF18/autogen.sh
# RUN make -j $(nproc)

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
