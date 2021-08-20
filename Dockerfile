FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip3 install -r requirements.txt

COPY ./src /src
