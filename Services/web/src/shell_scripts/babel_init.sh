#!/bin/bash

SUPPORT_LANGS=(ja zh)

for lang in ${SUPPORT_LANGS[@]};
    do
        pybabel init -i messages.pot -d translations -l $lang
    done