FROM crpi-4b5m1drruxllpt5o.cn-hangzhou.personal.cr.aliyuncs.com/mt-cloud/python:3.12-slim

ARG PYPI_SOURCE='https://mirrors.aliyun.com/pypi/simple'
ARG AREA=china

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN set -ex \
    && mkdir -p .pip  \
    && if [ 'china' = "$AREA" ] ; then \
      pip3 install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r requirements.txt; \
    else \
      pip3 install -r --no-cache-dir requirements.txt; \
    fi

COPY . /app

EXPOSE 8080

CMD ["python3", "/app/main.py"]