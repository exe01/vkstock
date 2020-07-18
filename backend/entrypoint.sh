#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Start server"
gunicorn -b 0.0.0.0:8000 -w 1 backend.wsgi