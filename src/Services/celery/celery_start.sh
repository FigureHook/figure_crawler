#!/bin/bash
celery -A basic_task worker -B --loglevel=INFO