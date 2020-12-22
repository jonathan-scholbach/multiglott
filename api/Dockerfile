FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /api/
COPY requirements.txt /api/

WORKDIR /api

RUN pip install -r requirements.txt