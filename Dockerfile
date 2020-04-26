FROM python:3.8-slim-buster

MAINTAINER franziskus.nakajima@gmail.com

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bluez

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_APP=homectrl

ENV FLASK_ENV=development

EXPOSE 8000

CMD ["flask", "run"]
