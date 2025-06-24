FROM ubuntu:16.04

RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install build-essential vim git cmake autoconf automake gettext autopoint
RUN apt-get -y build-dep coreutils

RUN mkdir -p /dataset/repos

# COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_gnubug_26545
# COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_gnubug_25003
# COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_gnubug_25023
# COPY --chown=extractfix:extractfix repos/coreutils /dataset/repos/coreutils_gnubug_19784
# COPY --chown=extractfix:extractfix testcases/gnubug_26545 /dataset/gnubug_26545
# COPY --chown=extractfix:extractfix testcases/gnubug_25003 /dataset/gnubug_25003
# COPY --chown=extractfix:extractfix testcases/gnubug_25023 /dataset/gnubug_25023
# COPY --chown=extractfix:extractfix testcases/gnubug_19784 /dataset/gnubug_19784
COPY testcases /dataset

# WORKDIR /home/extractfix
# RUN mkdir -p build_gnubug_26545 build_gnubug_25003 build_gnubug_25023 build_gnubug_19784 build_testsuite_gnubug_26545 build_testsuite_gnubug_25003 build_testsuite_gnubug_25023 build_testsuite_gnubug_19784

# WORKDIR /dataset/repos/coreutils_gnubug_26545
# RUN git checkout gnubug_26545
# RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
# RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
# RUN ./bootstrap
# WORKDIR /home/extractfix/build_gnubug_26545
# RUN /dataset/repos/coreutils_gnubug_26545/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /home/extractfix/build_testsuite_gnubug_26545 
# RUN /dataset/repos/coreutils_gnubug_26545/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/coreutils_gnubug_25003
# RUN git checkout gnubug_25003
# RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
# RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
# RUN ./bootstrap
# WORKDIR /home/extractfix/build_gnubug_25003
# RUN /dataset/repos/coreutils_gnubug_25003/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /home/extractfix/build_testsuite_gnubug_25003
# RUN /dataset/repos/coreutils_gnubug_25003/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/coreutils_gnubug_25023
# RUN git checkout gnubug_25023
# RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
# RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
# RUN ./bootstrap
# WORKDIR /home/extractfix/build_gnubug_25023
# RUN /dataset/repos/coreutils_gnubug_25023/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# RUN make -j $(nproc)
# WORKDIR /home/extractfix/build_testsuite_gnubug_25023 
# RUN /dataset/repos/coreutils_gnubug_25023/configure
# RUN make -j $(nproc)

# WORKDIR /dataset/repos/coreutils_gnubug_19784
# RUN git checkout gnubug_19784
# RUN git clean -xffd && git submodule foreach --recursive git clean -xffd
# RUN git reset --hard && git submodule foreach --recursive git reset --hard && git submodule update --init --recursive
# RUN ./bootstrap
# WORKDIR /home/extractfix/build_gnubug_19784
# RUN /dataset/repos/coreutils_gnubug_19784/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
# WORKDIR /home/extractfix/build_testsuite_gnubug_19784
# RUN /dataset/repos/coreutils_gnubug_19784/configure --enable-gcc-warnings=no
# RUN make -j $(nproc)

# # Disable tests that fail in docker
# RUN sed -i '/print_ver_/a skip_ "does not work in docker"' \
#     /dataset/repos/coreutils_gnubug_26545/tests/tail-2/inotify-dir-recreate.sh \
#     /dataset/repos/coreutils_gnubug_26545/tests/rm/deep-2.sh \
#     /dataset/repos/coreutils_gnubug_26545/tests/du/long-from-unreadable.sh \
#     /dataset/repos/coreutils_gnubug_25003/tests/rm/deep-2.sh \
#     /dataset/repos/coreutils_gnubug_25003/tests/du/long-from-unreadable.sh \
#     /dataset/repos/coreutils_gnubug_25023/tests/rm/deep-2.sh \
#     /dataset/repos/coreutils_gnubug_25023/tests/du/long-from-unreadable.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/rm/deep-2.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/tail-2/wait.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/tail-2/retry.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/tail-2/symlink.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/df/df-output.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/du/long-from-unreadable.sh \
#     /dataset/repos/coreutils_gnubug_19784/tests/tail-2/follow-stdin.sh

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
