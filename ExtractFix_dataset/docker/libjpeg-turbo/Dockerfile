FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake git unzip python-dev python-pip ipython autoconf libtool nasm
RUN apt-get -y build-dep libjpeg-turbo

RUN mkdir -p /dataset/repos
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_EF19
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_cve_2018_19664
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_cve_2017_15232
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_cve_2012_2806
# COPY testcases/EF19 /dataset/EF19
# COPY testcases/cve_2018_19664 /dataset/cve_2018_19664
# COPY testcases/cve_2017_15232 /dataset/cve_2017_15232
# COPY testcases/cve_2012_2806 /dataset/cve_2012_2806
COPY testcases /dataset

# WORKDIR /root
# RUN mkdir build_EF19 build_cve_2018_19664 build_cve_2017_15232 build_cve_2012_2806
# RUN mkdir build_testsuite_EF19 build_testsuite_cve_2018_19664 build_testsuite_cve_2017_15232 build_testsuite_cve_2012_2806

# # EF19, cve_2012_2806

# WORKDIR /dataset/repos/libjpeg-turbo_EF19
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout EF19
# RUN autoreconf -fvi
# WORKDIR /root/build_EF19
# RUN /dataset/repos/libjpeg-turbo_EF19/configure CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF19
# RUN /dataset/repos/libjpeg-turbo_EF19/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libjpeg-turbo_cve_2012_2806
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout cve_2012_2806
# RUN autoreconf -fvi
# WORKDIR /root/build_cve_2012_2806
# RUN /dataset/repos/libjpeg-turbo_cve_2012_2806/configure CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2012_2806
# RUN /dataset/repos/libjpeg-turbo_cve_2012_2806/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libjpeg-turbo_cve_2018_19664
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout cve_2018_19664
# WORKDIR /root/build_cve_2018_19664
# RUN CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_cve_2018_19664/
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2018_19664
# RUN cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_cve_2018_19664/
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libjpeg-turbo_cve_2017_15232
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout cve_2017_15232
# WORKDIR /root/build_cve_2017_15232
# RUN CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_cve_2017_15232/
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_cve_2017_15232
# RUN cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_cve_2017_15232/
# RUN make -j $(nproc)

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
