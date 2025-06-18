FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake autoconf automake gettext autopoint
RUN apt-get -y build-dep coreutils

# Coreutils really doesn't like building as root, so do everything as a normal user.
RUN adduser --gecos "" --disabled-password extractfix
RUN echo "extractfix:extractfix" | chpasswd 
RUN mkdir -p /dataset/repos
RUN chown -R extractfix:extractfix /dataset
USER extractfix

COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_EF23
COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_EF24
COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_EF25
COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_EF26
COPY --chown=extractfix:extractfix testcases/EF23 /dataset/EF23
COPY --chown=extractfix:extractfix testcases/EF24 /dataset/EF24
COPY --chown=extractfix:extractfix testcases/EF25 /dataset/EF25
COPY --chown=extractfix:extractfix testcases/EF26 /dataset/EF26

WORKDIR /home/extractfix
RUN mkdir -p build_EF23 build_EF24 build_EF25 build_EF26 build_testsuite_EF23 build_testsuite_EF24 build_testsuite_EF25 build_testsuite_EF26

WORKDIR /dataset/repos/coreutils_EF23
RUN git checkout EF23
RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
RUN ./bootstrap
WORKDIR /home/extractfix/build_EF23
RUN /dataset/repos/coreutils_EF23/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
RUN make -j $(nproc)
WORKDIR /home/extractfix/build_testsuite_EF23 
RUN /dataset/repos/coreutils_EF23/configure
RUN make -j $(nproc)

WORKDIR /dataset/repos/coreutils_EF24
RUN git checkout EF24
RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
RUN ./bootstrap
WORKDIR /home/extractfix/build_EF24
RUN /dataset/repos/coreutils_EF24/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
RUN make -j $(nproc)
WORKDIR /home/extractfix/build_testsuite_EF24
RUN /dataset/repos/coreutils_EF24/configure
RUN make -j $(nproc)

WORKDIR /dataset/repos/coreutils_EF25
RUN git checkout EF25
RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
RUN ./bootstrap
WORKDIR /home/extractfix/build_EF25
RUN /dataset/repos/coreutils_EF25/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
RUN make -j $(nproc)
WORKDIR /home/extractfix/build_testsuite_EF25 
RUN /dataset/repos/coreutils_EF25/configure
RUN make -j $(nproc)

WORKDIR /dataset/repos/coreutils_EF26
RUN git checkout EF26
RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
RUN ./bootstrap
WORKDIR /home/extractfix/build_EF26
RUN /dataset/repos/coreutils_EF26/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
WORKDIR /home/extractfix/build_testsuite_EF26
RUN /dataset/repos/coreutils_EF26/configure --enable-gcc-warnings=no
RUN make -j $(nproc)

# Disable tests that fail in docker
RUN sed -i '/print_ver_/a skip_ "does not work in docker"' \
    /dataset/repos/coreutils_EF23/tests/tail-2/inotify-dir-recreate.sh \
    /dataset/repos/coreutils_EF23/tests/rm/deep-2.sh \
    /dataset/repos/coreutils_EF23/tests/du/long-from-unreadable.sh \
    /dataset/repos/coreutils_EF24/tests/rm/deep-2.sh \
    /dataset/repos/coreutils_EF24/tests/du/long-from-unreadable.sh \
    /dataset/repos/coreutils_EF25/tests/rm/deep-2.sh \
    /dataset/repos/coreutils_EF25/tests/du/long-from-unreadable.sh \
    /dataset/repos/coreutils_EF26/tests/rm/deep-2.sh \
    /dataset/repos/coreutils_EF26/tests/tail-2/wait.sh \
    /dataset/repos/coreutils_EF26/tests/tail-2/retry.sh \
    /dataset/repos/coreutils_EF26/tests/tail-2/symlink.sh \
    /dataset/repos/coreutils_EF26/tests/df/df-output.sh \
    /dataset/repos/coreutils_EF26/tests/du/long-from-unreadable.sh \
    /dataset/repos/coreutils_EF26/tests/tail-2/follow-stdin.sh

USER root
RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
RUN chmod +x /scripts/*.sh

USER extractfix

WORKDIR /home/extractfix
