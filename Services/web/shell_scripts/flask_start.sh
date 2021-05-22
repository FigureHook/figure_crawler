#!/bin/bash

/bin/sh shell_scripts/babel_compile.sh

gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
