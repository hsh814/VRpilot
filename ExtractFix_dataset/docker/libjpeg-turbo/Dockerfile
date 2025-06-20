FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake
RUN apt-get -y build-dep libjpeg-turbo

RUN mkdir -p /dataset/repos
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_EF19
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_EF20
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_EF21
# COPY repos/libjpeg-turbo /dataset/repos/libjpeg-turbo_EF22
# COPY testcases/EF19 /dataset/EF19
# COPY testcases/EF20 /dataset/EF20
# COPY testcases/EF21 /dataset/EF21
# COPY testcases/EF22 /dataset/EF22
COPY testcases /dataset

# WORKDIR /root
# RUN mkdir build_EF19 build_EF20 build_EF21 build_EF22
# RUN mkdir build_testsuite_EF19 build_testsuite_EF20 build_testsuite_EF21 build_testsuite_EF22

# # EF19, EF22

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

# WORKDIR /dataset/repos/libjpeg-turbo_EF22
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout EF22
# RUN autoreconf -fvi
# WORKDIR /root/build_EF22
# RUN /dataset/repos/libjpeg-turbo_EF22/configure CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g"
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF22
# RUN /dataset/repos/libjpeg-turbo_EF22/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libjpeg-turbo_EF20
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout EF20
# WORKDIR /root/build_EF20
# RUN CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_EF20/
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF20
# RUN cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_EF20/
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/libjpeg-turbo_EF21
# RUN git clean -fdx
# RUN git reset --hard
# run git checkout EF21
# WORKDIR /root/build_EF21
# RUN CFLAGS="-fsanitize=address -g" LDFLAGS="-fsanitize=address -g" cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_EF21/
# RUN make -j $(nproc)
# WORKDIR /root/build_testsuite_EF21
# RUN cmake -G"Unix Makefiles" /dataset/repos/libjpeg-turbo_EF21/
# RUN make -j $(nproc)

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
