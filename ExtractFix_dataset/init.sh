#!/bin/bash
pushd docker

  git clone https://sourceware.org/git/binutils-gdb.git binutils-gdb/repos/binutils-gdb

  git clone https://github.com/coreutils/coreutils.git coreutils/repos/coreutils
  git clone https://github.com/coreutils/gnulib.git coreutils/repos/coreutils/gnulib

  git clone https://github.com/jasper-software/jasper.git jasper/repos/jasper

  git clone https://github.com/libarchive/libarchive.git libarchive/repos/libarchive

  git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git libjpeg-turbo/repos/libjpeg-turbo
  cd libjpeg-turbo/repos/libjpeg-turbo
  git fetch --all
  git fetch origin 1ecd9a5729d78518397889a630e3534bd9d963a8
  cd ../../../

  git clone https://github.com/libming/libming.git libming/repos/libming

  git clone https://github.com/vadz/libtiff.git libtiff/repos/libtiff

  curl -L -o libtiff/CVE-2016-3186.patch https://git.fortiss.org/toki/build‑systems/yocto/poky/-/raw/jethro-14.0.3/meta/recipes-multimedia/libtiff/files/CVE-2016-3186.patch

  git clone https://gitlab.gnome.org/GNOME/libxml2.git libxml2/repos/libxml2

  git clone https://github.com/gdraheim/zziplib.git zziplib/repos/zziplib
  pushd zziplib/repos/zziplib/docs
    wget https://github.com/LuaDist/libzzip/raw/master/docs/zziplib-manpages.tar
  popd

popd