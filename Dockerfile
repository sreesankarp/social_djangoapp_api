FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /social_app_api
WORKDIR /social_app_api

COPY . .
RUN pip install -r req.txt

