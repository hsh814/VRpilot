#!/bin/bash
/scripts/test_build.sh $1
cd /root/build

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
