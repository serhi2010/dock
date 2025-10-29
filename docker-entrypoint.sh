#!/usr/bin/env bash
set -e

python manage.py migrate --noinput

exec gunicorn diary.wsgi -b 0.0.0.0:8000 --workers 3