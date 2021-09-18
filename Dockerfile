FROM python:3.8-slim-buster

LABEL maintainer="mjfakler"

COPY beanbot /beanbot/

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r /beanbot/requirements.txt \
    && chmod u+x /beanbot/service.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends vim \
    && rm -rf /var/lib/apt/lists/*

VOLUME /beanbot/config /beanbot/logs

ENTRYPOINT /beanbot/service.sh
