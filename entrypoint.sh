#!/bin/sh


python manage.py makemigrations \
    user \
    chat_app \
    django_q \
    --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input --clear

exec "$@"