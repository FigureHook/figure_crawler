#!/bin/bash
cd ${WORKDIR}
gunicorn wsgi:app