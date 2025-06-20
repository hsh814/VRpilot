FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libjasper1

RUN mkdir -p /dataset/repos
# COPY repos/jasper /dataset/repos/jasper_EF27
# COPY repos/jasper /dataset/repos/jasper_EF28
# COPY repos/jasper /dataset/repos/jasper_testsuite_EF27
# COPY repos/jasper /dataset/repos/jasper_testsuite_EF28
# COPY testcases/EF27 /dataset/EF27
# COPY testcases/EF28 /dataset/EF28
COPY testcases /dataset

# WORKDIR /dataset/repos/jasper_EF27
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF27
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/jasper_EF28
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF28
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure CFLAGS="-fsanitize=undefined -g" LDFLAGS="-fsanitize=undefined -g"
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/jasper_testsuite_EF27
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF27
# RUN sed -i 's/inline bool/bool/' src/libjasper/base/jas_malloc.c
# RUN autoreconf -i
# RUN ./configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/jasper_testsuite_EF28
# RUN git clean -fdx
# RUN git reset --hard
# RUN git checkout EF28
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
