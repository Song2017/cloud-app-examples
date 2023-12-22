FROM python:3.9-buster

ARG PYPI_SOURCE='https://mirrors.aliyun.com/pypi/simple'
ARG AREA=china

RUN useradd -m -g 100 worker
USER worker
WORKDIR /home/worker
COPY --chown=worker:100 . .
ENV PATH="/home/worker/.local/bin:${PATH}"

RUN set -ex \
    # && if [ 'china' = "$AREA" ] ; then \
    #    sed -i "s@http://deb.debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list; \
    #    sed -i "s@http://security.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list; \
    # fi \
    && pip3 install -i "$PYPI_SOURCE" --upgrade pip \
    && pip3 install --user -i "$PYPI_SOURCE" -r requirements.txt --default-timeout=100 future 

ENTRYPOINT [""]