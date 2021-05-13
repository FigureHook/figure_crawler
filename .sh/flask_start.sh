#!/bin/bash

gunicorn src.wsgi:app
