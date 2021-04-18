#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Load djantimat initial_data"
python manage.py loaddata --app djantimat initial_data # для добавления существующей базы слов

echo "Start server"
gunicorn -b 0.0.0.0:8000 -w 1 backend.wsgi