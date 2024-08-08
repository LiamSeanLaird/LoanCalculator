#!/bin/sh

echo "Generating database migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
