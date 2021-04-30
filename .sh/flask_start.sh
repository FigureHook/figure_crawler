#!/bin/bash
cd /app
gunicorn wsgi:app