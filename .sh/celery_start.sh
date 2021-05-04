#!/bin/bash
cd ${WORKDIR}/src/Services/celery
celery -A app worker -B --loglevel=INFO