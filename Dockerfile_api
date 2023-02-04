FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip 

RUN mkdir /project

COPY api /project/api

RUN pip3 install -r /project/api/requirements.txt

WORKDIR /project/api

EXPOSE 8000

ENTRYPOINT gunicorn --bind 0.0.0.0:8000 -w 1 app:api