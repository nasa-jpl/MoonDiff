#!/bin/bash
source activate moondiff
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput
python manage.py collectstatic

python manage.py loaddata apollo14.yaml
python manage.py loaddata apollo12.yaml

gunicorn moondiff.wsgi:application --bind 0.0.0.0:8000