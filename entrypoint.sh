#!/bin/bash
source activate moondiff
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput

gunicorn moondiff.wsgi:application --bind 0.0.0.0:8000