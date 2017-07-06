FROM alpine:latest

MAINTAINER waylybaye <baye@wayly.net>

ENV DOCKER_HOST unix:///var/run/docker.sock

RUN apk --no-cache --update add openssh-client git python py-pip \
    && rm -rf /var/cache/apk/*  \
    && pip install docker

ADD . /opt/git-agent/

WORKDIR /opt/git-agent/
VOLUME /rootfs/

CMD python main.py /rootfs
