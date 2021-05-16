#!/bin/bash

SUPPORT_LANGS=(ja zh)
cd src/web

for lang in ${SUPPORT_LANGS[@]};
    do
        pybabel init -i messages.pot -d translations -l $lang
    done