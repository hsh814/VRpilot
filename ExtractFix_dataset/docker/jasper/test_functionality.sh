#!/bin/bash

set -e

case "$1" in
    EF27)
        cd /dataset/repos/jasper_testsuite_EF27
        for f in data/images/*.mif data/images/*.jpg data/images/*.pnm /dataset/jasper_newtests/* ; do
            echo "$f"
            src/appl/imginfo -f "$f"
        done
        ;;
    EF28)
        cd /dataset/repos/jasper_testsuite_EF27
        for f in data/images/*.mif data/images/*.jpg data/images/*.pnm /dataset/jasper_newtests/* ; do
            echo "$f"
            src/appl/imginfo -f "$f"
        done
        ;;
    *)
        echo "No such bug: $1"
        exit 1
        ;;
esac
