#!/bin/bash
EGGSDIR=eggs
cd ${SCRAPYDIR}

if [[ ! ${SCRAPYDIR+x} ]]; then
    echo "envrionment variable SCAPYDIR is unset."
    exit 1
fi

SPIDER_PROJECTS=$(python get_deployable_project.py)
for p in $SPIDER_PROJECTS;
    do
        mkdir -p ${EGGSDIR}/$p
        scrapyd-deploy --build-egg ./${EGGSDIR}/$p/$(date +%s).egg
    done

scrapyd
