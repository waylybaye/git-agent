FROM alpine:latest

MAINTAINER waylybaye <baye@wayly.net>

RUN apk --no-cache --update add git python py-pip \
    && rm -rf /var/cache/apk/*  \
    && pip install docker

ADD . /opt/git-agent/

WORKDIR /opt/git-agent/
VOLUME /rootfs/

CMD python main.py
