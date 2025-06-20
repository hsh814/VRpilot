#!/bin/bash
cd /dataset/repos/coreutils
./bootstrap

mkdir -p /root/build
cd /root/build
FORCE_UNSAFE_CONFIGURE=1 /dataset/repos/coreutils/configure CFLAGS="-g -fsanitize=address" LDFLAGS="-g -fsanitize=address"
make -j 32

case "$1" in
    EF23)
        touch blah ; ./src/shred -n4 -s7 blah
        ;;
    EF24)
        touch blah ; ./src/split -n7/75 blah
        ;;
    EF25)
        echo a > a
        ./src/pr "-S$(printf "\t\t\t")" a -m a > /dev/null
        ;;
    EF26)
        gcc -Ilib -g -fsanitize=address /dataset/repos/coreutils/src/make-prime-list.c -o make-prime-list
        ./make-prime-list 5000
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
