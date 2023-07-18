#!/bin/bash
source activate moondiff

if ! [ -f /app/db/db.sqlite3 ]
then
  # If the database doesn't exist yet, create it
  python manage.py migrate
  python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput

  python manage.py loaddata apollo14 apollo12 alphonsus examples forum
fi
python manage.py collectstatic --noinput
gunicorn moondiff.wsgi:application --bind 0.0.0.0:8000