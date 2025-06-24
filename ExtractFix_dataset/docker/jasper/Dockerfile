FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libjasper1

RUN mkdir -p /dataset/repos
# COPY repos/jasper /dataset/repos/jasper_cve_2016_8691
# COPY repos/jasper /dataset/repos/jasper_cve_2016_9387
# COPY repos/jasper /dataset/repos/jasper_testsuite_cve_2016_8691
# COPY repos/jasper /dataset/repos/jasper_testsuite_cve_2016_9387
# COPY testcases/cve_2016_8691 /dataset/cve_2016_8691
# COPY testcases/cve_2016_9387 /dataset/cve_2016_9387
COPY testcases /dataset

# WORKDIR /dataset/repos/jasper_cve_2016_8691
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_8691
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/jasper_cve_2016_9387
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_9387
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/jasper_testsuite_cve_2016_8691
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_8691
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/jasper_testsuite_cve_2016_9387
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout cve_2016_9387
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure
# RUN make -j $(nproc)

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

COPY jasper_newtests /dataset/jasper_newtests

WORKDIR /root
