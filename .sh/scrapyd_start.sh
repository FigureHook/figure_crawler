#!/bin/bash
EGGS_DIR=eggs
SPIDER_PROJECT_DIR=src/Services/crawler
# if [[ ! ${SERVICE_DIR+x} ]]; then
#     echo "envrionment variable SPIDER_APP_DIR is unset."
#     exit 1
# fi

# clean old stuffs
cd ${SPIDER_PROJECT_DIR} || exit 1
rm -r ${EGGS_DIR}/$p

SPIDER_PROJECTS=$(python get_deployable_project.py)
for p in $SPIDER_PROJECTS;
    do
        mkdir -p ${EGGSDIR}/$p
        scrapyd-deploy --build-egg ${EGGSDIR}/$p/$(date +%s).egg
    done

scrapyd
