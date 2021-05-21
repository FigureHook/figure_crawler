FROM python:3.9.5-slim

COPY requirements-deploy.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    pip --no-cache-dir install -r requirements.txt && \
    apt-get autoremove -y git
