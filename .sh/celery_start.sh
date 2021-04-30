#!/bin/bash
cd /app/src/Services/celery
celery -A app worker -B --loglevel=INFO