#!/bin/bash

/bin/sh .sh/babel_compile.sh

cd src
gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
