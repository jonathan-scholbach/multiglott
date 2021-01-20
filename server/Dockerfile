FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /server/
COPY requirements.txt /server/

WORKDIR /server

RUN pip install -r requirements.txt