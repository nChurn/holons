# syntax=docker/dockerfile:1
# FROM python:3.8.6-slim-buster
FROM nikolaik/python-nodejs:python3.8-nodejs14
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 8000

RUN echo deb http://deb.debian.org/debian buster contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
    && apt-get update \
    && apt-get --no-install-recommends install -y gettext locales-all wget imagemagick tzdata \
    curl build-essential libxml2-dev libxslt1-dev \
    libjpeg62-turbo-dev libjpeg-dev libfreetype6-dev libtiff5-dev liblcms2-dev libwebp-dev tk8.6-dev \
    libffi-dev libcgraph6 libgraphviz-dev libmagic-dev \
    libpq-dev gcc\
    && pip install psycopg2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY ./website/holons/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
