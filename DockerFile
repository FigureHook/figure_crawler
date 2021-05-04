FROM python:3.9-buster

WORKDIR /workspace

COPY requirements*.txt .
COPY .sh/python_init.sh .
RUN sh python_init.sh
