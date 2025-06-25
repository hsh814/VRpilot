FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y build-essential 
RUN apt-get install -y git vim unzip python-dev python-pip ipython zlib1g-dev

RUN mkdir -p /dataset/repos
COPY testcases /dataset

RUN mkdir /scripts
COPY test_security.sh /scripts
COPY test_functionality.sh /scripts
COPY test_build.sh /scripts
RUN chmod +x /scripts/*.sh

WORKDIR /root
