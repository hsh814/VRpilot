FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libxml2

RUN mkdir -p /dataset/repos
# COPY repos/libxml2 /dataset/repos/libxml2_cve_2016_1838
# COPY repos/libxml2 /dataset/repos/libxml2_EF16
# COPY repos/libxml2 /dataset/repos/libxml2_cve_2012_5134
# COPY repos/libxml2 /dataset/repos/libxml2_cve_2017_5969
# COPY testcases/cve_2016_1838 /dataset/cve_2016_1838
# COPY testcases/EF16 /dataset/EF16
# COPY testcases/cve_2012_5134 /dataset/cve_2012_5134
# COPY testcases/cve_2017_5969 /dataset/cve_2017_5969
COPY testcases /dataset

# WORKDIR /root
# RUN mkdir -p build_cve_2016_1838 build_testsuite_cve_2016_1838 build_EF16 build_testsuite_EF16 build_cve_2012_5134 build_testsuite_cve_2012_5134 build_cve_2017_5969 build_testsuite_cve_2017_5969

# WORKDIR /dataset/repos/libxml2_cve_2016_1838
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_1838
# WORKDIR /root/build_cve_2016_1838
# RUN /dataset/repos/libxml2_cve_2016_1838/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2016_1838
# RUN /dataset/repos/libxml2_cve_2016_1838/autogen.sh
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

# WORKDIR /dataset/repos/libxml2_cve_2012_5134
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2012_5134
# WORKDIR /root/build_cve_2012_5134
# RUN /dataset/repos/libxml2_cve_2012_5134/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2012_5134
# RUN /dataset/repos/libxml2_cve_2012_5134/autogen.sh
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libxml2_cve_2017_5969
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2017_5969
# WORKDIR /root/build_cve_2017_5969
# RUN /dataset/repos/libxml2_cve_2017_5969/autogen.sh CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2017_5969
# RUN /dataset/repos/libxml2_cve_2017_5969/autogen.sh
# RUN make -j $(nproc)

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
