FROM alpine:3.18

RUN set -x; \
        apk add terraform --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community \
        # for gitlab base image
        && apk add bash \ 
        && rm -rf /var/cache/apk/*

COPY ./alicloud.terraformrc /root