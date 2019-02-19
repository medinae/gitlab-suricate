FROM python:3.7-alpine3.9

RUN apk add --no-cache bash

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .