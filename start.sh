#!/usr/bin/env bash

if [ -z "${DJANGO_SETTINGS_MODULE}" ]; then
    export DJANGO_SETTINGS_MODULE=student_explorer.settings.env
fi

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=2
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

set -x

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    student_explorer.wsgi:application