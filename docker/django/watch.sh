#!/usr/bin/env bash

echo "Run django"

rm blogs/migrations/0001_initial.py

# cool method check available
sleep 3

python manage.py makemigrations

python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000