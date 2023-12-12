FROM python:3.11-slim-buster
LABEL maintainer="den.prislipskyi@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
