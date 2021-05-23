#!/bin/bash
FILE=requirements-top.txt
pip install --upgrade pip
if test -f "$FILE"; then
    pip install -r $FILE
else
    pip install -r requirements.txt
fi

pip install -e libs/figure_hook
pip install -e libs/figure_parser
pip install -e Services/celery
