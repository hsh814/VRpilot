#!/bin/bash
pushd docker

  git clone https://sourceware.org/git/binutils-gdb.git binutils-gdb/repos/binutils-gdb

  git clone https://github.com/coreutils/coreutils.git coreutils/repos/coreutils
  git clone https://github.com/coreutils/gnulib.git coreutils/repos/coreutils/gnulib

  git clone https://github.com/jasper-software/jasper.git jasper/repos/jasper

  git clone https://github.com/libarchive/libarchive.git libarchive/repos/libarchive

  git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git libjpeg-turbo/repos/libjpeg-turbo

  git clone https://github.com/libming/libming.git libming/repos/libming

  git clone https://github.com/vadz/libtiff.git libtiff/repos/libtiff

  git clone https://gitlab.gnome.org/GNOME/libxml2.git libxml2/repos/libxml2

  git clone https://github.com/gdraheim/zziplib.git zziplib/repos/zziplib

popd