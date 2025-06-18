#!/bin/bash

DOCKER_DIR=`pwd`/data
set -x
if [ ! -d "${DOCKER_DIR}" ] 
then
    echo "Downloading dataset with Dockerfiles"
    FILEID=1w6bC-iX1zTd7SVm5tvSFfbT4vddCT2YC
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=$FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$FILEID" -O data.zip && rm -rf /tmp/cookies.txt
    unzip -qq -o data.zip
    # rm data.zip

else
    echo "skipping"
fi
