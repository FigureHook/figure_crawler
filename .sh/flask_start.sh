#!/bin/bash

cd src/web
pybabel compile -d translations

gunicorn -w 2 -b 0.0.0.0:8000 src.wsgi:app
