#!/bin/bash
/scripts/test_build.sh $1
cd /root/build
export ASAN_OPTIONS=detect_leaks=0

case "$1" in
    gnubug_26545)
        touch blah ; ./src/shred -n4 -s7 blah
        ;;
    gnubug_25003)
        touch blah ; ./src/split -n7/75 blah
        ;;
    gnubug_25023)
        echo a > a
        ./src/pr "-S$(printf "\t\t\t")" a -m a > /dev/null
        ;;
    gnubug_19784)
        gcc -Ilib -g -fsanitize=address /dataset/repos/coreutils/src/make-prime-list.c -o make-prime-list
        ./make-prime-list 5000
        ;;
    *)
        echo "No such bug: $1"
        ;;
esac
