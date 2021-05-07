#!/bin/bash
cd src/Services/celery
celery -A basic_task worker -B --loglevel=INFO